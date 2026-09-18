"""Fixed-candidate confirmation with complete source evidence available to both arms."""
import json
import shutil
import sys
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from study import ROOT,MODEL,run_case,log,read_json,write_json,file_hash,create_state,resolve_state,case,grade,reconcile,compile_contract

out=Path(sys.argv[2]).resolve();old=ROOT/'evidence/pilot-02'

def prepare():
    out.mkdir(parents=True,exist_ok=False)
    for name in ['training-data','adapter-32']:
        shutil.copytree(old/name,out/name)
    for name in ['controller-cases.json','experience.json','runtime-source.json']:
        shutil.copyfile(old/name,out/name)
    for folder in ['scripts','workload','methods']:
        shutil.copytree(ROOT/folder,out/'snapshot'/folder,ignore=shutil.ignore_patterns('__pycache__'))
    rows=read_json(out/'training-data/training.json')
    assets={}
    for i in range(8):
        sid=f'source-{i}'
        collector=[json.loads(x) for x in (old/'runs/baseline'/sid/'work/events.jsonl').read_text().splitlines()]
        path=out/'source-access'/f'{sid}.json'
        write_json(path,{'training':[r for r in rows if r['case_id']==sid],'collector':collector})
        assets[path.name]=str(path)
    for arm in ['base','adapter-32','compiled-base','compiled-adapter-32']:
        template='compiled-v2-base' if arm.startswith('compiled-') else 'base'
        cfg=resolve_state(old/'states'/template,MODEL)
        parent=cfg.pop('state',None)
        env=ROOT/'workload'/('environment_compiled_parity.py' if arm.startswith('compiled-') else 'environment_parity.py')
        cfg['environment']={'path':str(env),'sha256':file_hash(env)}
        cfg['experience']=str(out/'experience.json')
        cfg['inherited_artifacts'].update(assets)
        cfg.pop('inherited_artifact_hashes',None)
        if arm.endswith('adapter-32'):cfg['adapter']=str(out/'adapter-32')
        create_state(cfg,out/'states'/arm,arm,parent=parent,
                     decision={'reason':'Protocol02 full source access; fixed previously selected adapter; no tuning','source':str(old/'decision.json')})
    # Prove every exact learning row is readable through each public environment.
    from construct_runtime.environment import load_environment
    for arm in ['base','adapter-32','compiled-base','compiled-adapter-32']:
        cfg=resolve_state(out/'states'/arm,MODEL);env=load_environment(cfg)
        ws=out/'access-checks'/arm;(ws/'inherited').mkdir(parents=True)
        for name,path in cfg['inherited_artifacts'].items():shutil.copyfile(path,ws/'inherited'/name)
        got=[]
        for i in range(8):
            for j in range(2):got.append(env.dispatch({}, {'tool':'read_source','source_id':f'source-{i}','kind':'training','index':j},ws)['record'])
        assert got==rows
    log(out,'source_access_verified',arms=4,exact_training_rows=16,collector_histories=8,
        protocol_sha256=file_hash(ROOT/'methods/PROTOCOL-02.md'))
    write_json(out/'decision.json',{'time_ns':time.time_ns(),'selected_steps':32,'deployment_promotion':False,
        'reason':'fixed confirmation of candidate selected before pilot fresh outcomes; no reselection',
        'protocol_sha256':file_hash(ROOT/'methods/PROTOCOL-02.md'),'source_access_verified':True})

def recheck():
    cases=read_json(out/'controller-cases.json')
    for c in cases:
        for arm in ['base','adapter-32']:
            run_case(out,arm,c,'recheck-'+arm)
        if c['split']=='development':
            for arm in ['compiled-base','compiled-adapter-32']:
                run_case(out,arm,c,'recheck-'+arm)

def evaluate():
    assert not (out/'evaluation-cases.json').exists()
    cases=[case('confirmation',i) for i in range(12)]
    write_json(out/'evaluation-cases.json',cases)
    log(out,'evaluation_generated',cases_sha256=file_hash(out/'evaluation-cases.json'),decision_sha256=file_hash(out/'decision.json'))
    for c in cases:
        tick=time.monotonic();direct=reconcile(c['task'],compile_contract(c['task']['contract']));elapsed=time.monotonic()-tick
        write_json(out/'direct-compiler'/c['id']/'artifact.json',direct)
        write_json(out/'direct-compiler'/c['id']/'grade.json',{'case_id':c['id'],'grade':grade(c,direct,'succeeded'),'execution_seconds':elapsed})
        arms=['base','adapter-32','compiled-base','compiled-adapter-32']
        if int(c['id'].split('-')[-1])%2:arms.reverse()
        for arm in arms:run_case(out,arm,c,'evaluation-'+arm)
    run_case(out,'base',read_json(out/'controller-cases.json')[0],'reset')
    assert read_json(out/'runs/recheck-base/source-0/work/reconciled.json')==read_json(out/'runs/reset/source-0/work/reconciled.json')
    log(out,'reset_artifact_check',identical=True)

if sys.argv[1]=='prepare':prepare()
elif sys.argv[1]=='recheck':recheck()
elif sys.argv[1]=='evaluate':evaluate()
else:raise ValueError('unknown phase')
