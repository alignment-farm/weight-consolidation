"""Same public interface plus reusable contract compilation, available to both arms."""
import json
import runpy
from construct_runtime.records import write_json

# Load original public environment from an inherited, content-pinned file at dispatch.
# System prompt deliberately restates tools without importing any controller fixtures.
class ReconcileCompiled:
    name='reconcile-compiled/2'
    tool_names=('read_procedure','run_saved','run_contract')
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
Tool errors and previews permit repair but do not certify semantic correctness.'''
    def validate_task(self,task):
        if set(task)!={'job','contract','rows','accounts'}:raise ValueError('public fields only')
        if not isinstance(task['contract'],str) or not isinstance(task['rows'],list) or not isinstance(task['accounts'],dict):raise ValueError('invalid task')
    def task_prompt(self,task):return json.dumps(task,separators=(',',':'))
    def dispatch(self,task,action,workspace):
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
