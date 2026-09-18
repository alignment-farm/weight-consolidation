"""Controller. Evaluator truth remains in this process; workers receive public tasks only."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from workload.fixtures import case, grade
from workload.transform import reconcile
from workload.environment import Reconcile
from construct_runtime.executor import messages_for
from construct_runtime.records import Events, canonical, file_hash, read_json, write_json, source_identity
from construct_runtime.state import create_state, resolve_state
from construct_runtime.experience import export_source

MODEL = str(ROOT/'models/qwen3-4b-4bit')

def log(out, kind, **data):
    Events(out/'sequence.jsonl').emit(kind,**data)

def prepare(out):
    out.mkdir(parents=True,exist_ok=False)
    for folder in ['workload','scripts','methods']:
        shutil.copytree(ROOT/folder,out/'snapshot'/folder,ignore=shutil.ignore_patterns('__pycache__'))
    write_json(out/'runtime-source.json',source_identity())
    source = [case('source',i) for i in range(8)]
    development = [case('development',i) for i in range(4)]
    write_json(out/'controller-cases.json',source+development)
    examples = [{'source_id':c['id'],'reference_config':c['config']} for c in source[:4]]
    write_json(out/'experience.json',examples)
    cfg = {'model_path':MODEL,'model_manifest':str(ROOT/'resources/model.json'),
           'environment':{'path':str(ROOT/'workload/environment.py'),'sha256':file_hash(ROOT/'workload/environment.py')},
           'experience':str(out/'experience.json'),'mode':'memory',
           'inherited_artifacts':{'transform.py':str(ROOT/'workload/transform.py')},'max_steps':6}
    state = create_state(cfg,out/'states/base','external-reuse',decision={'reason':'protocol01 baseline; authored code and references available to both arms'})
    log(out,'prepared',state_id=state['state_id'],protocol_sha256=file_hash(ROOT/'methods/PROTOCOL-01.md'))
    # Independent generator/oracle agreement check and meaningful defect checks.
    for c in source+development:
        assert reconcile(c['task'],c['config']) == c['expected']
    c=source[0]
    bad={**c['config'],'accept':['posted','void']}
    assert reconcile(c['task'],bad) != c['expected']
    assert reconcile(c['task'],{**c['config'],'dedup':'latest'}) != c['expected']
    assert reconcile(c['task'],{**c['config'],'credit_negative':False}) != c['expected']
    try: Reconcile().validate_task({**c['task'],'expected':c['expected']})
    except ValueError: pass
    else: raise AssertionError('evaluator boundary failed')
    log(out,'tool_oracle_checks',cases=len(source+development),mutation_checks=3,label_rejection=True)


def run_case(out, state, c, stage, suffix=''):
    folder=out/'runs'/stage/(c['id']+suffix)
    if folder.exists():
        raise ValueError('refusing repeated output directory')
    folder.mkdir(parents=True)
    write_json(folder/'public-task.json',c['task'])
    tick=time.monotonic()
    with (folder/'worker.log').open('w') as stream:
        proc=subprocess.run([sys.executable,str(ROOT/'scripts/worker.py'),str(out/'states'/state),MODEL,
                             str(folder/'public-task.json'),str(folder/'work')],stdout=stream,stderr=subprocess.STDOUT,timeout=300)
    result=read_json(folder/'work/result.json') if (folder/'work/result.json').exists() else {'status':'crashed','usage':{}}
    artifact=read_json(folder/'work/reconciled.json') if (folder/'work/reconciled.json').exists() else {}
    row={'stage':stage,'state':state,'case_id':c['id'],'split':c['split'],'changed':c['changed'],
         'exit_code':proc.returncode,'controller_seconds':time.monotonic()-tick,
         'grade':grade(c,artifact,result['status']),'result':result,'folder':str(folder.relative_to(out))}
    write_json(folder/'grade.json',row)
    log(out,'task_checked',**row)
    print(stage,c['id'],row['grade']['complete'],flush=True)
    if proc.returncode:
        raise RuntimeError(f'worker crashed: {folder}')
    return row


def references(out):
    cases=read_json(out/'controller-cases.json')
    cfg=resolve_state(out/'states/base',MODEL)
    examples=read_json(out/'experience.json')
    selections=[]
    for c in cases:
        if c['split']!='source': continue
        folder=out/'references'/c['id']
        folder.mkdir(parents=True,exist_ok=False)
        (folder/'inherited').mkdir()
        shutil.copyfile(ROOT/'workload/transform.py',folder/'inherited/transform.py')
        events=Events(folder/'events.jsonl')
        messages=messages_for(c['task'],examples,'memory',Reconcile(),cfg)
        for action in [{'tool':'run_saved','config':c['config']},{'tool':'finish'}]:
            events.emit('reference_request',messages=messages)
            events.emit('reference_action',action=action)
            result=Reconcile().dispatch(c['task'],action,folder) if action['tool']!='finish' else {'finished':True}
            events.emit('tool_result',result=result)
            messages=messages+[{'role':'assistant','content':canonical(action)},
                               {'role':'user','content':'Tool result: '+canonical(result)}]
        assert grade(c,read_json(folder/'reconciled.json'),'succeeded')['complete']
        selections.append({'split':'source','origin':'authored-correction','case_id':c['id'],
                           'events':str(folder/'events.jsonl'),'reason':'executed investigator reference; source-only teaching irrespective of collector success'})
    result=export_source(selections,out/'training-data')
    log(out,'references_exported',**result,authored_actions=16,separate_teacher_calls=0,authoring_cost=None)


def baseline(out, smoke=False):
    cases=read_json(out/'controller-cases.json')
    for c in cases[:1] if smoke else cases:
        run_case(out,'base',c,'smoke' if smoke else 'baseline')
    if not smoke: references(out)


def traincheck(out,steps):
    path=out/f'adapter-{steps}'
    tick=time.monotonic()
    with (out/f'training-{steps}.log').open('w') as stream:
        proc=subprocess.run([sys.executable,str(ROOT/'scripts/train.py'),str(out/'states/base'),MODEL,
                             str(out/'training-data/training.json'),str(path),str(steps)],stdout=stream,stderr=subprocess.STDOUT,timeout=1800)
    log(out,'training_attempt',steps=steps,exit_code=proc.returncode,controller_seconds=time.monotonic()-tick)
    if proc.returncode: raise RuntimeError(f'training failed; inspect training-{steps}.log')
    cfg=resolve_state(out/'states/base',MODEL)
    parent=cfg.pop('state',None)
    cfg['adapter']=str(path)
    create_state(cfg,out/f'states/adapter-{steps}',f'adapter-{steps}',parent=parent,
                 decision={'reason':'development candidate; fresh optimizer from base','steps':steps})
    for c in read_json(out/'controller-cases.json'):
        run_case(out,f'adapter-{steps}',c,f'check-{steps}')


def evaluate(out,steps):
    # This action is only called after investigator decision is persisted.
    decision=read_json(out/'decision.json')
    assert decision['selected_steps']==steps
    cases=[case('evaluation',i) for i in range(12)]
    assert not (out/'evaluation-cases.json').exists()
    write_json(out/'evaluation-cases.json',cases)
    log(out,'evaluation_generated',cases_sha256=file_hash(out/'evaluation-cases.json'),decision_sha256=file_hash(out/'decision.json'))
    for c in cases:
        assert reconcile(c['task'],c['config'])==c['expected']
        # alternate order, sequential workers, no concurrent heavy runs.
        for arm in (['base',f'adapter-{steps}','compiled-base',f'compiled-adapter-{steps}'] if int(c['id'].split('-')[-1])%2==0 else [f'compiled-adapter-{steps}','compiled-base',f'adapter-{steps}','base']):
            run_case(out,arm,c,'evaluation-'+arm)
    c=read_json(out/'controller-cases.json')[0]
    run_case(out,'base',c,'reset')
    first=read_json(out/'runs/baseline'/c['id']/'work/reconciled.json')
    last=read_json(out/'runs/reset'/c['id']/'work/reconciled.json')
    assert first==last
    log(out,'reset_artifact_check',identical=True)


def summarize(out):
    groups={}
    for p in sorted((out/'runs').glob('*/*/grade.json')):
        row=read_json(p)
        g=groups.setdefault(row['stage'],{'tasks':0,'complete':0,'prompt_tokens':0,'completion_tokens':0,'calls':0,'failed_calls':0,'tool_calls':0,'model_seconds':0.,'tool_seconds':0.,'elapsed_seconds':0.,'controller_seconds':0.})
        g['tasks']+=1; g['complete']+=int(row['grade']['complete'])
        for k,v in row['result'].get('usage',{}).items(): g[k]+=v
        g['elapsed_seconds']+=row['result'].get('elapsed_seconds',0)
        g['controller_seconds']+=row['controller_seconds']
    write_json(out/'summary.json',groups)
    print(json.dumps(groups,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['prepare','smoke','baseline','traincheck','evaluate','summarize']);p.add_argument('--output',required=True);p.add_argument('--steps',type=int,default=32)
    a=p.parse_args();out=Path(a.output).resolve()
    if a.phase=='prepare': prepare(out)
    elif a.phase=='smoke': baseline(out,True)
    elif a.phase=='baseline': baseline(out)
    elif a.phase=='traincheck': traincheck(out,a.steps)
    elif a.phase=='evaluate': evaluate(out,a.steps)
    else: summarize(out)
