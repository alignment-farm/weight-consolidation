"""Owned controller: private benchmark truth never enters agent tasks/tools."""
import argparse,json,shutil,sqlite3,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CONT=ROOT/'continuation'
sys.path.insert(0,str(CONT))
from workload.environment import DatabaseWork
from construct_runtime.records import Events,canonical,file_hash,read_json,write_json,source_identity
from construct_runtime.executor import messages_for
from construct_runtime.state import create_state,resolve_state
from construct_runtime.experience import export_source

MODEL=str(ROOT/'models/qwen3-4b-4bit')
MODEL_MANIFEST=str(ROOT/'resources/model.json')
PROFILE='4b'
def configure(out,profile=None):
    global MODEL,MODEL_MANIFEST,PROFILE
    saved=out/'model-profile.json'
    PROFILE=profile or (read_json(saved)['profile'] if saved.exists() else '4b')
    MODEL=str(ROOT/'models'/('qwen3-4b-4bit' if PROFILE=='4b' else 'qwen2.5-coder-7b-4bit'))
    MODEL_MANIFEST=str(ROOT/('resources/model.json' if PROFILE=='4b' else 'continuation/resources/model7b.json'))
PARTS={'source0':[2,3,4,6,9,10,11,13,16,17,18,21],'development0':[1,5,7,12,14,15],
       'fresh0':[19,20,22,24,25,26,27,28,29,30],'source1':[101,103,106,109,110,113,117],
       'development1':[102,104,107,111],'fresh1':[105,108,112,114,115,116,118,119,120,23]}

def database(rev):return ROOT/'.deps/cl-databases'/('products.db' if rev=='before' else 'products_drifted.db')
def log(out,kind,**data):Events(out/'sequence.jsonl').emit(kind,**data)
def bank():
    folder=ROOT/'.deps/continual-learning-bench/data/database_exploration'
    return {r['question_id']:r for name in ['questions.json','questions_post_drift.json'] for r in read_json(folder/name)}
def task(r,revision):return {'job':f"q{r['question_id']}",'question':r['question'],'revision':revision}
def oracle(r,revision):
    with sqlite3.connect('file:'+str(database(revision))+'?mode=ro&immutable=1',uri=True) as conn:
        deadline=time.monotonic()+30;conn.set_progress_handler(lambda:int(time.monotonic()>deadline),10000)
        return [list(x) for x in conn.execute(r['sql']).fetchall()]
def compare(actual,expected,tolerance):
    if not isinstance(actual,list) or len(actual)!=len(expected):return False
    for a,b in zip(actual,expected):
        if len(a)!=len(b):return False
        for x,y in zip(a,b):
            if isinstance(x,(int,float)) and isinstance(y,(int,float)):
                if abs(x-y)>max(tolerance,1e-8):return False
            elif x!=y:return False
    return True

def state(out,name,history,adapter=None,parent=None,revision="before"):
    folder=out/'state-inputs'/name;folder.mkdir(parents=True,exist_ok=False)
    write_json(folder/'history.json',history)
    write_json(folder/'experience.json',[{k:r[k] for k in ['id','question','revision','origin']} for r in history])
    cfg={'model_path':MODEL,'model_manifest':MODEL_MANIFEST,'mode':'base','max_steps':8,
         'environment':{'path':str(CONT/'workload/environment.py'),'sha256':file_hash(CONT/'workload/environment.py')},
         'experience':str(folder/'experience.json'),'guidance':f'There are {len(history)} source queries available. Search the history for related work when useful; execute saved queries directly when they answer the current request.',
         'inherited_artifacts':{'history.json':str(folder/'history.json'),'views.py':str(CONT/'workload'/f'views_{revision}.py'),'documentation.txt':str(CONT/'workload'/f'documentation-{revision}.txt')}}
    if adapter:cfg['adapter']=str(adapter)
    return create_state(cfg,out/'states'/name,name,parent=parent,decision={'reason':'protocol03 fixed history/tool snapshot','source_count':len(history)})

def prepare(out):
    out.mkdir(parents=True,exist_ok=False)
    write_json(out/'model-profile.json',{'profile':PROFILE,'model_manifest':MODEL_MANIFEST})
    for folder in ['scripts','workload','methods']:
        shutil.copytree(CONT/folder,out/'snapshot'/folder,ignore=shutil.ignore_patterns('__pycache__'))
    write_json(out/'runtime.json',source_identity());write_json(out/'partition.json',PARTS)
    for rev in ['before','after']:
        path=database(rev)
        with sqlite3.connect('file:'+str(path)+'?mode=ro&immutable=1',uri=True) as conn:
            check=conn.execute('PRAGMA quick_check').fetchall()
            schema={r[0]:[x[1] for x in conn.execute('PRAGMA table_info("'+r[0]+'")')] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        assert check==[('ok',)],check
        write_json(out/f'database-{rev}.json',{'name':path.name,'sha256':file_hash(path),'bytes':path.stat().st_size,'revision':read_json(CONT/'sources/database-manifest.json')['revision'],'schema':schema,'quick_check':check})
    state(out,'collector0',[])
    log(out,'prepared',protocol_sha256=file_hash(CONT/'methods/PROTOCOL-03.md'))

def run_case(out,arm,r,revision,stage):
    folder=out/'runs'/stage/f"q{r['question_id']}";folder.mkdir(parents=True,exist_ok=False)
    write_json(folder/'task.json',task(r,revision))
    tick=time.monotonic()
    with (folder/'worker.log').open('w') as stream:
        p=subprocess.run([sys.executable,str(CONT/'scripts/worker.py'),str(out/'states'/arm),MODEL,str(database(revision)),str(out/f'database-{revision}.json'),str(folder/'task.json'),str(folder/'work')],stdout=stream,stderr=subprocess.STDOUT,timeout=300)
    seconds=time.monotonic()-tick
    result=read_json(folder/'work/result.json') if (folder/'work/result.json').exists() else {'status':'crashed','usage':{}}
    artifact=read_json(folder/'work/answer.json') if (folder/'work/answer.json').exists() else {}
    tick=time.monotonic();expected=oracle(r,revision);check_seconds=time.monotonic()-tick
    grade={'complete':result['status']=='succeeded' and compare(artifact.get('rows'),expected,r.get('tolerance',0)),
           'result_correct':compare(artifact.get('rows'),expected,r.get('tolerance',0)),'expected':expected,
           'upstream_stored_answer':r['answer'],'tolerance':r.get('tolerance',0),'reference_sql':r['sql']}
    row={'stage':stage,'arm':arm,'id':r['question_id'],'revision':revision,'grade':grade,'result':result,'controller_seconds':seconds,'checking_seconds':check_seconds,'exit_code':p.returncode}
    write_json(folder/'grade.json',row);log(out,'checked',**row)
    print(stage,r['question_id'],grade['complete'],flush=True)
    if p.returncode:raise RuntimeError('worker failed: '+str(folder))
    return row

def source_block(out,point):
    records=bank();revision='before' if point==0 else 'after';arm=f'collector{point}'
    for i in PARTS[f'source{point}']:run_case(out,arm,records[i],revision,f'source{point}')
    reference_block(out,point)

def reference_block(out,point):
    records=bank();revision='before' if point==0 else 'after';cfg=resolve_state(out/'states'/f'collector{point}',MODEL)
    previous=read_json(out/'history0.json') if point else []
    eligible=[];new=[]
    for i in PARTS[f'source{point}']:
        r=records[i];collected=out/'runs'/f'source{point}'/f'q{i}'
        grade=read_json(collected/'grade.json')['grade']
        if grade['complete']:
            sql=read_json(collected/'work/answer.json')['query'];sql_origin='executor'
        else:sql=r['sql'];sql_origin='authored-source-correction'
        folder=out/f'references{point}'/f'q{i}';(folder/'inherited').mkdir(parents=True,exist_ok=False)
        for name,p in cfg['inherited_artifacts'].items():shutil.copyfile(p,folder/'inherited'/name)
        import os
        os.environ['WC_DATABASE_PATH']=str(database(revision))
        env=DatabaseWork();messages=messages_for(task(r,revision),read_json(cfg['experience']),'base',env,cfg)
        events=Events(folder/'events.jsonl');tick=time.monotonic()
        for action in [{'tool':'submit','query':sql},{'tool':'finish'}]:
            events.emit('reference_request',messages=messages)
            events.emit('reference_action',action=action)
            answer=env.dispatch(task(r,revision),action,folder) if action['tool']=='submit' else {'finished':True}
            events.emit('tool_result',result=answer)
            messages=messages+[{'role':'assistant','content':canonical(action)},{'role':'user','content':'Tool result: '+canonical(answer)}]
        assert compare(read_json(folder/'answer.json')['rows'],oracle(r,revision),r.get('tolerance',0))
        eligible.append({'split':'source','origin':'authored-correction','case_id':f'q{i}','events':str(folder/'events.jsonl'),
                         'reason':f'Executed two-action teaching replay; SQL origin={sql_origin}. Replay sequence investigator-authored, not claimed on-policy.'})
        new.append({'id':f'q{i}','question':r['question'],'sql':sql,'revision':revision,'origin':sql_origin})
        log(out,'source_reference',id=i,sql_origin=sql_origin,seconds=time.monotonic()-tick)
    # Cumulative export always restarts from base; retain original source trace bytes.
    if point:eligible=read_json(out/'source-selections0.json')+eligible
    write_json(out/f'source-selections{point}.json',eligible)
    result=export_source(eligible,out/f'training-data{point}')
    rows=read_json(out/f'training-data{point}/training.json')
    history=previous+new
    for r in history:r['records']=[x for x in rows if x['case_id']==r['id']]
    write_json(out/f'history{point}.json',history)
    state(out,f'base{point}',history,revision=revision)
    # Verify exact trainer inputs reachable via public tool for both later arms.
    assert [x for r in history for x in r['records']]==rows
    from validate_environment import access_checks
    access_checks(out,f'base{point}',point,MODEL)
    log(out,'source_exported',point=point,**result)
    if point==0:state(out,'collector1',history,revision='after')

def train(out,point,steps):
    candidate=out/f'adapter{point}-{steps}';tick=time.monotonic()
    with (out/f'train{point}-{steps}.log').open('w') as stream:
        proc=subprocess.run([sys.executable,str(CONT/'scripts/train.py'),str(out/'states'/f'base{point}'),MODEL,str(out/f'training-data{point}/training.json'),str(candidate),str(steps)],stdout=stream,stderr=subprocess.STDOUT,timeout=1800)
    log(out,'training_attempt',point=point,steps=steps,exit_code=proc.returncode,controller_seconds=time.monotonic()-tick)
    if proc.returncode:raise RuntimeError('training failed; preserve log')
    state(out,f'adapter{point}-{steps}',read_json(out/f'history{point}.json'),candidate,revision='before' if point==0 else 'after')
    from validate_environment import access_checks
    access_checks(out,f'adapter{point}-{steps}',point,MODEL)

def check(out,point,arm):
    rows=bank();rev='before' if point==0 else 'after'
    for i in PARTS[f'source{point}']+PARTS[f'development{point}']:
        run_case(out,arm,rows[i],rev,'check-'+arm)

def fresh(out,point):
    decision=read_json(out/'decision.json');steps=decision['steps'];records=bank();rev='before' if point==0 else 'after'
    arms=[f'base{point}',f'adapter{point}-{steps}']
    if point:
        state(out,'stale1',read_json(out/'history1.json'),out/f'adapter0-{steps}',revision='after')
        from validate_environment import access_checks
        access_checks(out,'stale1',point,MODEL)
        arms.append('stale1')
    log(out,'fresh_started',point=point,decision_sha256=file_hash(out/'decision.json'))
    for n,i in enumerate(PARTS[f'fresh{point}']):
        for arm in arms if n%2==0 else list(reversed(arms)):
            run_case(out,arm,records[i],rev,'fresh-'+arm)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['prepare','smoke','source','train','check','fresh']);p.add_argument('--output',required=True);p.add_argument('--point',type=int,default=0);p.add_argument('--steps',type=int,default=48);p.add_argument('--arm');p.add_argument('--model-profile',choices=['4b','7b']);a=p.parse_args();out=Path(a.output).resolve();configure(out,a.model_profile)
    if a.phase=='prepare':prepare(out)
    elif a.phase=='smoke':
        rows=bank()
        for i in [1,12]:run_case(out,'collector0',rows[i],'before','smoke')
    elif a.phase=='source':source_block(out,a.point)
    elif a.phase=='train':train(out,a.point,a.steps)
    elif a.phase=='check':check(out,a.point,a.arm)
    else:fresh(out,a.point)
