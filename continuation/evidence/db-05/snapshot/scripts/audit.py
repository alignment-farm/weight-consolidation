"""Read-only audit of frozen histories, runtime/adapter identities and paired tools."""
import argparse,json
from pathlib import Path
from construct_runtime.records import file_hash,read_json,write_json
from construct_runtime.state import resolve_state
from validate_environment import access_checks
import run

p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output).resolve();run.configure(out)
report={'states':{},'pairs':{},'training':{},'runtime_pin':'9ffb10a66180626b80127fb1892b2cf71e39d946'}
for path in sorted((out/'states').iterdir()):
    cfg=resolve_state(path,run.MODEL)
    report['states'][path.name]={'assets_verified':True,'environment':cfg['environment']['sha256'],'inherited':cfg['inherited_artifact_hashes']}
for point in [0,1]:
    data=out/f'training-data{point}/training.json'
    if not data.exists():continue
    eligible={f'q{i}' for k in range(point+1) for i in run.PARTS[f'source{k}']}
    rows=read_json(data)
    assert {r['case_id'] for r in rows}==eligible
    assert all(r['origin']=='authored-correction' for r in rows)
    for path in sorted(out.glob(f'adapter{point}-*/manifest.json')):
        m=read_json(path);recipe=read_json(path.parent/'recipe.json')
        assert m['training_data_sha256']==file_hash(data)
        assert m['base_unchanged'] and m['initial_tensor_digest']!=m['final_tensor_digest']
        assert not recipe['optimizer_continuation']
        assert m['weights_sha256']==file_hash(path.parent/'adapter.safetensors')
        report['training'][path.parent.name]={'base_unchanged':True,'weights_changed':True,'fresh_optimizer':True,'data_verified':True}
    candidates=[f'base{point}']+[p.name for p in (out/'states').glob(f'adapter{point}-*')]
    if point and (out/'states/stale1').exists():candidates+=['stale1']
    cfgs={name:resolve_state(out/'states'/name,run.MODEL) for name in candidates}
    for name,cfg in cfgs.items():
        base=cfgs[f'base{point}']
        for key in ['inherited_artifact_hashes','experience_sha256','guidance','max_steps','mode','model_manifest_sha256']:
            assert cfg[key]==base[key],(name,key)
        assert cfg['environment']['sha256']==base['environment']['sha256']
        access_checks(out,name,point,run.MODEL)
    report['pairs'][str(point)]={'arms':candidates,'identical_external_assets_and_controls':True,'source_cases':sorted(eligible),'exact_records':len(rows)}
identities=[]
for path in sorted(out.glob('runs/*/q*/work/events.jsonl')):
    events=[json.loads(line) for line in path.read_text().splitlines()]
    start=next(e for e in events if e['kind']=='execution_started')
    assert start['source']['git_head']==report['runtime_pin']
    for e in events:
        if e['kind']=='model_loaded':
            identity=e['identity'];identities.append(identity)
            adapter=identity['adapter'];cfg=start['config']
            assert (adapter is not None)==('adapter' in cfg)
            if adapter:assert adapter['weights_sha256']==read_json(Path(cfg['adapter'])/'manifest.json')['weights_sha256']
            assert identity['generation']['max_tokens']==512
            assert identity['database_binding']['sha256']==read_json(out/f"database-{start['task']['revision']}.json")['sha256']
    assert set(start['task'])=={'job','question','revision'}
report['verified_model_loads']=len(identities)
report['base_digests']=sorted({i['base_digest'] for i in identities})
assert len(report['base_digests'])==1
report['note']='Loader verifies actual base/tokenizer hashes, adapter tensor names/shapes/values per process; state resolution verifies assets. This audit checks recorded boundaries, not absence of model pretraining contamination.'
write_json(out/'audit.json',report);print(json.dumps(report,indent=2))
