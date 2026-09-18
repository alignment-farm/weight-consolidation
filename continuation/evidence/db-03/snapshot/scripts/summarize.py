"""Summarize every preserved execution, including failed exploration, in native units."""
import collections,json
from construct_runtime.environment import parse_action
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EVIDENCE=ROOT/'continuation/evidence'

def read(path):return json.loads(path.read_text())
def main():
    groups={};runs=[];training=[]
    for path in sorted(EVIDENCE.glob('db-*/runs/*/q*/grade.json')):
        r=read(path);events=[json.loads(x) for x in (path.parent/'work/events.jsonl').read_text().splitlines()]
        start=next(e for e in events if e['kind']=='execution_started')
        loaded=next((e for e in events if e['kind']=='model_loaded'),None)
        actions=[]
        for event in events:
            if event['kind']=='model_response':
                try:actions.append(parse_action(event['text']))
                except ValueError:actions.append({'tool':'malformed-action'})
        r['tools']=dict(collections.Counter(a.get('tool','unknown') for a in actions))
        r['model_identity']=loaded['identity'] if loaded else None
        r['path']=str(path.relative_to(ROOT));r['process_id']=start['process_id'];runs.append(r)
        key=path.parts[-5]+'/'+r['stage'];g=groups.setdefault(key,{'n':0,'complete':0,'correct_artifact':0,'usage':{},'tools':{},'controller_seconds':0,'checking_seconds':0,'ids':[],'correct_ids':[]})
        g['n']+=1;g['complete']+=r['grade']['complete'];g['correct_artifact']+=r['grade']['result_correct'];g['ids'].append(r['id'])
        if r['grade']['complete']:g['correct_ids'].append(r['id'])
        for k,v in r['result'].get('usage',{}).items():g['usage'][k]=g['usage'].get(k,0)+v
        for k,v in r['tools'].items():g['tools'][k]=g['tools'].get(k,0)+v
        for k in ['controller_seconds','checking_seconds']:g[k]+=r[k]
    for path in sorted(EVIDENCE.glob('db-*/adapter*/manifest.json')):
        training.append({'path':str(path.relative_to(ROOT)),**read(path)})
    totals={'task_executions':len(runs),'complete':sum(r['grade']['complete'] for r in runs),'usage':{},'controller_seconds':sum(r['controller_seconds'] for r in runs),'checking_seconds':sum(r['checking_seconds'] for r in runs),'training_runs':len(training),'training_updates':sum(t['steps'] for t in training),'training_usage':{},'training_elapsed_seconds':sum(t['elapsed_seconds'] for t in training)}
    for r in runs:
        for k,v in r['result'].get('usage',{}).items():totals['usage'][k]=totals['usage'].get(k,0)+v
    for t in training:
        for k,v in t['usage'].items():totals['training_usage'][k]=totals['training_usage'].get(k,0)+v
    totals['unknown']=['investigator authoring/reasoning time and tokens','upstream data/code/teacher effort','energy','FLOPs','amortized deployment break-even']
    result={'groups':groups,'totals':totals,'training':training,'note':'Use-time, search, shared source collection and consolidation remain separated by stage. Controller elapsed includes loading/generation/tools; do not add those nested times again. Includes every graded task; separately inspect worker failures without grades and failed training_attempt events.'}
    (EVIDENCE/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'groups':{k:{x:v[x] for x in ['n','complete','correct_artifact','correct_ids','tools']} for k,v in groups.items()},'totals':totals},indent=2))
if __name__=='__main__':main()
