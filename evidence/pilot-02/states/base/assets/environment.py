"""Public reconciliation tools; expected outputs never enter this module."""
import json
import runpy
from construct_runtime.records import write_json

class Reconcile:
    name = 'reconcile/1'
    tool_names = ('read_procedure','run_saved')
    artifact_names = ('reconciled.json',)
    system_prompt = '''Reconcile an invoice export using its CURRENT contract and account crosswalk.
Return one JSON tool action per turn, no prose. Retained transform.py performs all parsing,
joining, revision selection, arithmetic, sorting, and writes the complete output. Use it.
Choose a config from the contract. Deduplicate before filtering. Quarantine accepted rows
with unknown accounts; exclude all unaccepted statuses. Current contract overrides examples.
Tools:
{"tool":"run_saved","config":{"fields":{"id":"column","account":"column","amount":"column","status":"column","revision":"column","kind":"column"},"units":"major","dedup":"latest","credit_negative":true,"accept":["posted"]}}
units is major (dollars to cents) or minor (already cents); dedup is first or latest revision.
credit_negative converts credit-kind amounts to negative absolute values when true, otherwise
preserves their supplied sign. accept lists exactly the eligible status strings.
{"tool":"read_procedure"} reads retained transform.py.
{"tool":"experience"} reads source examples, already supplied in context.
{"tool":"finish"} finishes after successful output. Inspect the returned artifact first.
Replace every column placeholder with the actual column name from the current contract.
The first-occurrence rule means dedup=first; highest revision means dedup=latest.
To finish emit exactly {"tool":"finish"}, with no input or other keys.
Tool errors and output previews are available for repair. They do not certify semantic correctness.'''
    def validate_task(self, task):
        if set(task) != {'job','contract','rows','accounts'}:
            raise ValueError('only job, contract, rows, accounts permitted')
        if not isinstance(task['contract'],str) or not isinstance(task['rows'],list):
            raise ValueError('invalid public task')
        if not all(isinstance(x,dict) and all(isinstance(v,(str,int)) for v in x.values()) for x in task['rows']):
            raise ValueError('rows must contain only scalar public fields')
        if not isinstance(task['accounts'],dict) or not all(isinstance(v,str) for v in task['accounts'].values()):
            raise ValueError('accounts must map strings')
    def task_prompt(self, task):
        return json.dumps(task, separators=(',',':'))
    def dispatch(self, task, action, workspace):
        if action == {'tool':'read_procedure'}:
            return {'source':(workspace/'inherited'/'transform.py').read_text()}
        if set(action) != {'tool','config'} or action['tool'] != 'run_saved':
            raise ValueError('run_saved requires config')
        try:
            result = runpy.run_path(str(workspace/'inherited'/'transform.py'))['reconcile'](task,action['config'])
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(str(e)) from e
        write_json(workspace/'reconciled.json',result)
        return {'artifact':'reconciled.json','preview':result}

def create_environment():
    return Reconcile()
