"""Offline evidence audit; never launches a model."""
import json
from pathlib import Path
import sys
from collections import defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workload.fixtures import grade
from construct_runtime.records import read_json, file_hash, write_json
from construct_runtime.state import resolve_state

out=Path(sys.argv[1]).resolve()
case_list=read_json(out/'controller-cases.json')
if (out/'evaluation-cases.json').exists(): case_list+=read_json(out/'evaluation-cases.json')
cases={c['id']:c for c in case_list}
checks=[]; costs=defaultdict(lambda:defaultdict(float)); outcome=defaultdict(lambda:defaultdict(int))
base_config=resolve_state(out/'states/base',None)
identities=[]
for path in sorted((out/'runs').glob('*/*/grade.json')):
    row=read_json(path);work=path.parent/'work';c=cases[row['case_id']]
    artifact=read_json(work/'reconciled.json') if (work/'reconciled.json').exists() else {}
    result=read_json(work/'result.json')
    assert grade(c,artifact,result['status'])==row['grade']
    assert read_json(path.parent/'public-task.json')==c['task']
    ev=[json.loads(s) for s in (work/'events.jsonl').read_text().splitlines()]
    start=next(e for e in ev if e['kind']=='execution_started')
    assert start['task']==c['task'] and set(start['task'])=={'job','contract','rows','accounts'}
    assert ev[-1]['kind']=='execution_finished'
    identity=next(e['identity'] for e in ev if e['kind']=='model_loaded')
    identities.append(identity)
    cfg=resolve_state(out/'states'/row['state'],None)
    base_config=resolve_state(out/'states'/('compiled-v2-base' if row['state'].startswith('compiled-v2-') else 'compiled-base' if row['state'].startswith('compiled-') else 'base'),None)
    comparable=lambda x:{k:v for k,v in x.items() if k not in ['adapter','adapter_manifest_sha256','state','experience','environment','model_manifest','model_path','inherited_artifacts']}
    # Compare content hashes as resolved state paths naturally differ.
    assert comparable(cfg)==comparable(base_config)
    assert cfg['environment']['sha256']==base_config['environment']['sha256']
    assert cfg['experience_sha256']==base_config['experience_sha256']
    assert cfg['inherited_artifact_hashes']==base_config['inherited_artifact_hashes']
    assert identity['base']['files']==read_json(base_config['model_manifest'])['files']
    if row['state'].endswith('base'): assert identity['adapter'] is None
    else: assert identity['adapter']['weights_sha256']==read_json(out/row['state'].removeprefix('compiled-v2-').removeprefix('compiled-')/'manifest.json')['weights_sha256']
    key=row['stage']
    costs[key]['tasks']+=1
    costs[key]['worker_seconds']+=result['elapsed_seconds']
    costs[key]['controller_seconds']+=row['controller_seconds']
    for k,v in result['usage'].items():costs[key][k]+=v
    outcome[key]['complete']+=int(row['grade']['complete']);outcome[key]['tasks']+=1
    if c['changed']:
        outcome[key]['changed_complete']+=int(row['grade']['complete']);outcome[key]['changed_tasks']+=1
        for component in ['quarantine','excluded','records','total_minor']:
            outcome[key]['changed_'+component]+=int(row['grade']['components'][component])
    checks.append(str(path.relative_to(out)))
assert len({x['base_digest'] for x in identities})==1
training=[]
if (out/'training-data/training.json').exists():
    rows=read_json(out/'training-data/training.json')
    assert all(r['split']=='source' and r['case_id'].startswith('source-') for r in rows)
    for r in rows:assert file_hash(out/'training-data'/r['source_events'])==r['source_events_sha256']
    for p in sorted(out.glob('adapter-*/manifest.json')):
        m=read_json(p);assert m['base_unchanged'] and m['initial_tensor_digest']!=m['final_tensor_digest']
        assert m['training_data_sha256']==file_hash(out/'training-data/training.json')
        assert m['weights_sha256']==file_hash(p.parent/'adapter.safetensors')
        training.append({'candidate':p.parent.name,'steps':m['steps'],'usage':m['usage'],'elapsed_seconds':m['elapsed_seconds'],'peak_mlx_bytes':m['peak_mlx_bytes']})
sequence=[json.loads(s) for s in (out/'sequence.jsonl').read_text().splitlines()]
if (out/'decision.json').exists():
    decision=read_json(out/'decision.json')
    for e in sequence:
        if e['kind']=='evaluation_generated':
            assert decision['time_ns']<e['time_ns']
            assert e['decision_sha256']==file_hash(out/'decision.json')
reset=[]
for c in case_list:
    a=out/'runs/baseline'/c['id']/'work/reconciled.json';b=out/'runs/reset'/c['id']/'work/reconciled.json'
    if a.exists() and b.exists():assert read_json(a)==read_json(b);reset.append(c['id'])
report={'audited_runs':len(checks),'outcomes':outcome,'costs':costs,'training':training,'reset_cases':reset,
        'unknown_costs':['investigator/authoring model tokens and labor','energy','FLOPs','unmeasured setup overhead'],
        'limitations':['single synthetic history','one training seed','no OS sandbox claim','wall times not controlled performance measurements']}
write_json(out/'audit.json',report)
print(json.dumps(report,indent=2))
