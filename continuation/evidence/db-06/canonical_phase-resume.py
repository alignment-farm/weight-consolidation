"""Protocol 04: reuse collected experience, add checked complete source programs."""
import argparse,os,shutil,sys,time
from pathlib import Path
import run
from construct_runtime.records import Events,canonical,file_hash,read_json,write_json
from construct_runtime.state import resolve_state
from construct_runtime.executor import messages_for
from construct_runtime.experience import export_source
from validate_environment import access_checks

def reference_block(out,point):
    source_out=run.CONT/'evidence/db-05' if point==0 else out
    rows=run.bank();revision='before' if point==0 else 'after';cfg=resolve_state(out/'states'/f'collector{point}',run.MODEL)
    canonical_sql=read_json(run.CONT/'workload/canonical_source_sql.json')
    overrides=out/f'canonical-overrides{point}.json'
    if overrides.exists():canonical_sql.update(read_json(overrides)['queries'])
    prior0={r['id']:r for r in read_json(source_out/'history0-retained.json')} if point==0 else {}
    history=read_json(out/'history0.json') if point else [];selections=read_json(out/'source-selections0.json') if point else []
    for i in run.PARTS[f'source{point}']:
        r=rows[i];sql=canonical_sql[str(i)];collected=source_out/'runs'/f'source{point}'/f'q{i}'
        grade=read_json(collected/'grade.json');folder=out/f'references{point}'/f'q{i}';(folder/'inherited').mkdir(parents=True,exist_ok=True)
        already_validated=(folder/'answer.json').exists()
        tick=time.monotonic()
        if already_validated:
            assert read_json(folder/'answer.json')['query']==sql
            run.log(out,'source_reference_reused',id=i,events_sha256=file_hash(folder/'events.jsonl'),reason='Resume after later source-query timeout; previously validated replay retained without rerunning.')
        else:
            for name,path in cfg['inherited_artifacts'].items():shutil.copyfile(path,folder/'inherited'/name)
            os.environ['WC_DATABASE_PATH']=str(run.database(revision));env=run.DatabaseWork();task=run.task(r,revision)
            messages=messages_for(task,read_json(cfg['experience']),'base',env,cfg);events=Events(folder/'events.jsonl')
            for action in [{'tool':'submit','query':sql},{'tool':'finish'}]:
                events.emit('reference_request',messages=messages);events.emit('reference_action',action=action)
                result=env.dispatch(task,action,folder) if action['tool']=='submit' else {'finished':True}
                events.emit('tool_result',result=result)
                messages=messages+[{'role':'assistant','content':canonical(action)},{'role':'user','content':'Tool result: '+canonical(result)}]
            assert run.compare(read_json(folder/'answer.json')['rows'],run.oracle(r,revision),r.get('tolerance',0)),i
        item={'id':f'q{i}','question':r['question'],'sql':sql,'revision':revision,'origin':'investigator-canonical-source-program','prior_records':prior0.get(f'q{i}',{}).get('records',[]),'collection_events_sha256':file_hash(collected/'work/events.jsonl'),'collection_path':str(collected),'collector_complete':grade['grade']['complete']}
        item['collected_queries']=run.retained_components(collected/'work/events.jsonl',item)
        old_query=prior0[f'q{i}']['sql'] if point==0 else (read_json(collected/'work/answer.json')['query'] if grade['grade']['complete'] else r['sql'])
        if old_query!=sql and not any(q['sql']==old_query for q in item['collected_queries']):
            item['collected_queries'].append({'id':f'q{i}:prior-source-program','sql':old_query,'revision':revision,'origin':'prior-source-program','previously_checked_as_source_answer':True})
        history.append(item)
        if (collected/'work/saved.json').exists():
            for name,query in read_json(collected/'work/saved.json').items():
                history.append({'id':f'q{i}-saved-{name}','question':r['question']+'; retained worker query '+name,'sql':query,'revision':revision,'origin':'executor-saved-ungraded'})
        selections.append({'split':'source','origin':'authored-correction','case_id':f'q{i}','events':str(folder/'events.jsonl'),'reason':'Investigator complete computational query in existing normalized views; executed against pinned source data and source oracle. Original queries/components and prior teacher records retained externally.'})
        if not already_validated:run.log(out,'source_reference',id=i,sql_origin='investigator-canonical-source-program',seconds=time.monotonic()-tick,collection_reused=point==0,collection_events_sha256=item['collection_events_sha256'])
    write_json(out/f'source-selections{point}.json',selections);result=export_source(selections,out/f'training-data{point}')
    training=read_json(out/f'training-data{point}/training.json')
    for item in history:item['records']=[r for r in training if r['case_id']==item['id']]
    write_json(out/f'history{point}.json',history);run.state(out,f'base{point}',history,revision=revision)
    access_checks(out,f'base{point}',point,run.MODEL)
    run.log(out,'source_exported',point=point,**result)
    if point==0:run.state(out,'collector1',history,revision='after')

def source1(out):
    rows=run.bank()
    for i in run.PARTS['source1']:run.run_case(out,'collector1',rows[i],'after','source1')
    reference_block(out,1)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['prepare','source1']);p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output).resolve();run.configure(out,'4b')
    if a.phase=='prepare':
        run.prepare(out);run.log(out,'protocol04_started',protocol_sha256=file_hash(run.CONT/'methods/PROTOCOL-04.md'),canonical_programs_sha256=file_hash(run.CONT/'workload/canonical_source_sql.json'),reused_source0='continuation/evidence/db-05/runs/source0')
        reference_block(out,0)
    else:source1(out)
