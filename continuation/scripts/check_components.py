"""Exercise retained component execution through the same public tool used by workers."""
import json,os,shutil,sys,tempfile,time
from pathlib import Path
from construct_runtime.records import read_json,write_json,file_hash
from construct_runtime.state import resolve_state
from construct_runtime.environment import load_environment
import run
out=Path(sys.argv[1]).resolve();run.configure(out);checks=[];start=time.monotonic()
for point in [0,1]:
    history_path=out/f'history{point}.json'
    if not history_path.exists():continue
    candidates=[f'base{point}']+[p.name for p in (out/'states').glob(f'adapter{point}-*')]
    if point and (out/'states/stale1').exists():candidates+=['stale1']
    revision='before' if point==0 else 'after';history=read_json(history_path)
    components=[q for r in history for q in r.get('collected_queries',[]) if q.get('revision')==revision and 'observed_result' in q][:2]
    for arm in candidates:
        cfg=resolve_state(out/'states'/arm,run.MODEL)
        with tempfile.TemporaryDirectory(dir=out) as tmp:
            work=Path(tmp);(work/'inherited').mkdir()
            for name,path in cfg['inherited_artifacts'].items():shutil.copyfile(path,work/'inherited'/name)
            os.environ['WC_DATABASE_PATH']=str(run.database(revision));env=load_environment(cfg)
            for q in components:
                response=env.dispatch({'job':'component-audit','question':'Replay preserved component','revision':revision},{'tool':'run_saved','id':q['id']},work)
                response=json.loads(json.dumps(response))  # worker tools expose JSON arrays, not SQLite tuples
                for key in ['columns','rows','row_count']:assert response[key]==q['observed_result'][key],(arm,q['id'],key)
                checks.append({'arm':arm,'component':q['id'],'executed':True,'observed_output_reproduced':True,'history_sha256':cfg['inherited_artifact_hashes']['history.json']})
write_json(out/'component-execution-audit.json',{'checks':checks,'tool_calls':len(checks),'seconds':time.monotonic()-start});print('verified component executions',len(checks))
