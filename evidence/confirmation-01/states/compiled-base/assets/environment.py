"""Same public interface plus reusable contract compilation, available to both arms."""
import json
import runpy
from construct_runtime.records import write_json

# Load original public environment from an inherited, content-pinned file at dispatch.
# System prompt deliberately restates tools without importing any controller fixtures.
class ReconcileCompiled:
    name='reconcile-compiled-parity/1'
    tool_names=('read_procedure','run_saved','run_contract','read_source')
    artifact_names=('reconciled.json',)
    system_prompt='''Reconcile invoice exports under their CURRENT contract, including account crosswalks,
credit signs, units and revision precedence. Retained code handles this bounded contract language.
Start with run_contract: it compiles the current contract and executes transform.py.
If run_contract succeeds, finish. Use run_saved only as a fallback if run_contract returns an error.
Source configurations describe OLD jobs; do not substitute them for a successful current-contract result.
It excludes unaccepted statuses and quarantines unknown accounts. Current contracts override examples.
Return one JSON action per turn, no prose.
{"tool":"run_contract"} executes the retained contract compiler and transformation; no arguments.
{"tool":"read_procedure"} reads both retained programs.
{"tool":"run_saved","config":{"fields":{"id":"column","account":"column","amount":"column","status":"column","revision":"column","kind":"column"},"units":"major","dedup":"latest","credit_negative":true,"accept":["posted"]}} manually configures the same transformation if needed. Replace column placeholders.
{"tool":"experience"} reads source examples, already supplied in context.
After inspecting a successful output preview emit exactly {"tool":"finish"}, no other keys.
Full source evidence is retained for source-0 through source-7.
{"tool":"read_source","source_id":"source-0"} lists available record counts.
{"tool":"read_source","source_id":"source-0","kind":"training","index":0} reads an exact source training row (messages and target). Training indices are 0 and 1. kind="collector" reads a source collector event at index. These are OLD source jobs, not current instructions.
Tool errors and previews permit repair but do not certify semantic correctness.'''
    def validate_task(self,task):
        if set(task)!={'job','contract','rows','accounts'}:raise ValueError('public fields only')
        if not isinstance(task['contract'],str) or not isinstance(task['rows'],list) or not isinstance(task['accounts'],dict):raise ValueError('invalid task')
    def task_prompt(self,task):return json.dumps(task,separators=(',',':'))
    def dispatch(self,task,action,workspace):
        if action.get('tool')=='read_source':
            if set(action)-{'tool','source_id','kind','index'}:raise ValueError('invalid source read fields')
            source_id=action.get('source_id')
            if source_id not in [f'source-{i}' for i in range(8)]:raise ValueError('source_id must be source-0 through source-7')
            source=json.loads((workspace/'inherited'/f'{source_id}.json').read_text())
            if 'index' not in action:return {'counts':{k:len(v) for k,v in source.items()}}
            kind=action.get('kind','training');index=action['index']
            if kind not in source or type(index) is not int or not 0<=index<len(source[kind]):raise ValueError('invalid source kind or index')
            return {'source_id':source_id,'kind':kind,'index':index,'record':source[kind][index]}

        inherited=workspace/'inherited'
        if action=={'tool':'read_procedure'}:
            return {n:(inherited/n).read_text() for n in ['transform.py','compile_contract.py']}
        if action=={'tool':'run_contract'}:
            cfg=runpy.run_path(str(inherited/'compile_contract.py'))['compile_contract'](task['contract'])
        elif set(action)=={'tool','config'} and action['tool']=='run_saved':cfg=action['config']
        else:raise ValueError('invalid action')
        result=runpy.run_path(str(inherited/'transform.py'))['reconcile'](task,cfg)
        write_json(workspace/'reconciled.json',result)
        return {'artifact':'reconciled.json','preview':result}

def create_environment():return ReconcileCompiled()
