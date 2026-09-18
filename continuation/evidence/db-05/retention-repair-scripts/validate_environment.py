"""Controller-only interface, migration and exact external source-access checks."""
import json,os,runpy,shutil,sqlite3,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'continuation'))
from workload.environment import DatabaseWork
from construct_runtime.records import file_hash,read_json,write_json
from construct_runtime.state import resolve_state

def environment_checks():
    results={}
    for revision,filename in [('before','products.db'),('after','products_drifted.db')]:
        path=ROOT/'.deps/cl-databases'/filename
        conn=sqlite3.connect('file:'+str(path)+'?mode=ro&immutable=1',uri=True)
        runpy.run_path(str(ROOT/'continuation/workload'/f'views_{revision}.py'))['install'](conn,revision)
        checks={}
        for view,raw in [('products','items'),('reviews','fdbk')]:
            checks[view+'_rows_preserved']=conn.execute(f'SELECT COUNT(*) FROM {view}').fetchone()[0]==sum(conn.execute(f'SELECT COUNT(*) FROM {raw}_g{g}').fetchone()[0] for g in [1,2,3])
        checks['office_epoch_preserved']=conn.execute('SELECT epoch_seconds FROM reviews_1 EXCEPT SELECT ts/1000.0 FROM fdbk_g1').fetchall()==[] and conn.execute('SELECT ts/1000.0 FROM fdbk_g1 EXCEPT SELECT epoch_seconds FROM reviews_1').fetchall()==[]
        if revision=='after':
            checks['authoritative_price']=conn.execute('SELECT COUNT(*) FROM products_2 p JOIN items_g2 i USING(ref_id) WHERE p.price IS NOT i.prc_v2/100.0').fetchone()[0]==0
            checks['migration_consequential']=conn.execute('SELECT COUNT(*) FROM items_g2 WHERE prc != prc_v2').fetchone()[0]>0
            checks['split_dates_preserved']=conn.execute('SELECT COUNT(*) FROM reviews_3 WHERE year IS NOT NULL').fetchone()[0]==conn.execute('SELECT COUNT(*) FROM fdbk_g3 WHERE review_year IS NOT NULL').fetchone()[0]
            checks['current_attributes']=conn.execute("SELECT COUNT(*) FROM attributes WHERE category='musical instruments'").fetchone()[0]==conn.execute('SELECT COUNT(*) FROM product_attributes_g3').fetchone()[0]
        assert all(checks.values()),checks
        conn.close();results[revision]=checks
    env=DatabaseWork()
    try:env.validate_task({'job':'boundary','question':'x','revision':'before','expected':42})
    except ValueError:results['truth_field_rejected']=True
    else:raise AssertionError('unexpected task truth accepted')
    write_json(ROOT/'continuation/evidence/environment-checks.json',results)
    return results

def access_checks(out,arm,point,model):
    cfg=resolve_state(out/'states'/arm,model);env=DatabaseWork()
    expected=read_json(out/f'training-data{point}/training.json');actual=[]
    with tempfile.TemporaryDirectory(dir=out) as tmp:
        workspace=Path(tmp);(workspace/'inherited').mkdir()
        for name,p in cfg['inherited_artifacts'].items():shutil.copyfile(p,workspace/'inherited'/name)
        history=read_json(workspace/'inherited/history.json')
        task={'job':'access-audit','question':'Verify inherited records','revision':'before' if point==0 else 'after'}
        for r in history:
            meta=env.dispatch(task,{'tool':'read_source','id':r['id']},workspace)
            for index in range(meta['record_count']):actual.append(env.dispatch(task,{'tool':'read_source','id':r['id'],'index':index},workspace)['record'])
        assert actual==expected
        result={'arm':arm,'point':point,'records_retrievable':len(actual),'training_sha256':file_hash(out/f'training-data{point}/training.json'),'inherited':cfg['inherited_artifact_hashes'],'exact_match':True}
        write_json(out/f'access-{arm}.json',result)
        return result
if __name__=='__main__':print(json.dumps(environment_checks(),indent=2))
