"""Read-only database agent tools. No question bank, evaluator or expected answers."""
import json
import os
import re
import runpy
import sqlite3
import time
from pathlib import Path
from construct_runtime.records import write_json


def ranked(records,query):
    stop={'the','a','of','in','is','what','how','many','to','and','for','with','that','have','are','on','by','as','from','than','more','only','or'}
    words=lambda s:set(re.findall(r'[a-z0-9]+',s.lower()))-stop
    q=words(query)
    return sorted(records,key=lambda r:(-len(q&words(r['question']+' '+r['sql'])),r['id']))

class DatabaseWork:
    name='continuing-database/1'
    tool_names=('sql','submit','schema','read','search_history','read_source','run_saved','save_sql')
    artifact_names=('answer.json',)
    system_prompt='''Complete the database report with a correct executable SQL query. One JSON tool action per turn, no prose.
You have read-only SQLite, retained SQL and exact source histories. Use ordinary execution to check your work; public SQL errors are repair feedback, not correctness labels. Search relevant retained experience when useful. Current documentation overrides old examples.
Normalized views are installed automatically:
products(category,ref_id,title,price,catalog_rating,status,image_count)
reviews(category,ref_id,product_id,user_id,rating,body,review_date,year,month,verified,verification_label,epoch_seconds)
attributes(category,ref_id,attr_key,attr_val); categories(category,ref_id,cat_lvl,cat_nm).
category is 'office products', 'electronics', or 'musical instruments'. price is DOLLARS; verified is integer 0/1. Join views on category AND ref_id. product_id is NOT the product foreign key. category taxonomy level1 is broad category. Count the requested unit (reviews/products/distinct users), not joined duplicates. For a count of products satisfying a GROUP BY/HAVING condition, count the grouped rows with an outer SELECT COUNT(*) FROM (...); do not output one count per product. Do not confuse catalog_rating with actual review means. Do not drop archived products unless requested. NULL text verification_label means missing label, NOT unverified. Use year/month for available date parts. SQLite dates/years can be NULL for huge corrupt epochs; use numeric epoch_seconds to test far-future timestamps. Raw tables are also available; inspect schemas/docs when needed.
Tools:
{"tool":"sql","query":"SELECT ..."} executes a read-only query, returns up to 20 preview rows.
{"tool":"submit","query":"SELECT ..."} executes final SQL and writes the FULL result to answer.json. Use exactly the requested result/column(s). It does not grade correctness.
{"tool":"schema"} lists all raw and view columns. Optional table name selects one.
{"tool":"read","name":"documentation.txt"} reads handbook. name="views.py" reads helper implementation.
{"tool":"search_history","query":"your current need"} returns the 3 most relevant retained questions and executable SQL, with source IDs.
{"tool":"read_source","id":"source-id","index":0} reads an exact training record (messages and target); omit index to list metadata and record counts.
{"tool":"run_saved","id":"source-id","params":{}} executes retained SQL and writes answer.json. This is direct reuse, not query regeneration. Params optional.
{"tool":"save_sql","name":"name","query":"SELECT ..."} retains a query in this job; run_saved may use its name. Useful successful source queries are inherited across sessions by both conditions.
{"tool":"experience"} lists shared history metadata. After inspecting successful final execution emit exactly {"tool":"finish"}. Never finish after a failed submit. No evaluator labels are available.'''
    def validate_task(self,task):
        if set(task)!={'job','question','revision'} or task['revision'] not in ['before','after']:
            raise ValueError('public task requires only job/question/revision')
        if not all(isinstance(v,str) for v in task.values()):raise ValueError('public values must be text')
    def task_prompt(self,task):
        return json.dumps(task,separators=(',',':'))
    def dispatch(self,task,action,workspace):
        inherited=workspace/'inherited'
        history=json.loads((inherited/'history.json').read_text())
        tool=action.get('tool')
        if tool=='read':
            if action['name'] not in ['documentation.txt','views.py']:raise ValueError('unknown public document')
            return {'content':(inherited/action['name']).read_text()}
        if tool=='search_history':
            return {'matches':[{k:r[k] for k in ['id','question','sql','revision','origin']}|{'saved_component_ids':[q['id'] for q in r.get('collected_queries',[])]} for r in ranked(history,action['query'])[:3]]}
        if tool=='read_source':
            r=next((r for r in history if r['id']==action['id']),None)
            if r is None:r=next((q|{'records':[]} for parent in history for q in parent.get('collected_queries',[]) if q['id']==action['id']),None)
            if r is None:raise ValueError('unknown source ID')
            if 'index' not in action:return {k:v for k,v in r.items() if k!='records'}|{'record_count':len(r['records'])}
            i=action['index']
            if type(i) is not int or not 0<=i<len(r['records']):raise ValueError('source index out of range')
            return {'record':r['records'][i]}
        if tool=='save_sql':
            name=action['name']
            if not re.fullmatch(r'[a-zA-Z0-9_-]{1,64}',name):raise ValueError('invalid query name')
            saved=json.loads((workspace/'saved.json').read_text()) if (workspace/'saved.json').exists() else {}
            saved[name]=action['query'];write_json(workspace/'saved.json',saved)
            return {'saved':name}
        query=action.get('query')
        params=action.get('params',{})
        if tool=='run_saved':
            saved=json.loads((workspace/'saved.json').read_text()) if (workspace/'saved.json').exists() else {}
            r=next((r for r in history if r['id']==action['id']),None)
            if r is None:r=next((q for parent in history for q in parent.get('collected_queries',[]) if q['id']==action['id']),None)
            query=saved.get(action['id'],r['sql'] if r else None)
            if query is None:raise ValueError('unknown saved query')
        if tool not in ['sql','submit','schema','run_saved']:raise ValueError('unknown action')
        conn=sqlite3.connect('file:'+os.environ['WC_DATABASE_PATH']+'?mode=ro&immutable=1',uri=True)
        try:
            runpy.run_path(str(inherited/'views.py'))['install'](conn,task['revision'])
            if tool=='schema':
                names=[r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' UNION SELECT name FROM sqlite_temp_master WHERE type='view'")]
                if 'table' in action:names=[n for n in names if n==action['table']]
                return {'schema':{n:[r[1] for r in conn.execute('PRAGMA table_info("'+n.replace('"','""')+'")')] for n in names}}
            if not isinstance(query,str) or len(query)>20000:raise ValueError('invalid SQL query')
            deadline=time.monotonic()+20
            conn.set_progress_handler(lambda:int(time.monotonic()>deadline),10000)
            denied={sqlite3.SQLITE_INSERT,sqlite3.SQLITE_UPDATE,sqlite3.SQLITE_DELETE,sqlite3.SQLITE_ATTACH,sqlite3.SQLITE_DETACH,sqlite3.SQLITE_DROP_TABLE,sqlite3.SQLITE_DROP_VIEW,sqlite3.SQLITE_CREATE_TABLE,sqlite3.SQLITE_CREATE_VIEW,sqlite3.SQLITE_PRAGMA}
            conn.set_authorizer(lambda a,b,c,d,e:sqlite3.SQLITE_DENY if a in denied else sqlite3.SQLITE_OK)
            cursor=conn.execute(query,params)
            columns=[c[0] for c in cursor.description] if cursor.description else []
            rows=cursor.fetchall()
            if tool in ['submit','run_saved']:
                write_json(workspace/'answer.json',{'query':query,'params':params,'columns':columns,'rows':rows})
            return {'columns':columns,'rows':rows[:20],'row_count':len(rows),'artifact':'answer.json' if tool in ['submit','run_saved'] else None}
        except sqlite3.Error as e:raise ValueError(str(e)) from e
        finally:conn.close()

def create_environment():return DatabaseWork()
