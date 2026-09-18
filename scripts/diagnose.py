"""Offline per-task action and exposure summary, without model execution."""
import json
from pathlib import Path
import sys
from construct_runtime.records import read_json, write_json
out=Path(sys.argv[1]);rows=[]
for p in sorted((out/'runs').glob('*/*/grade.json')):
    row=read_json(p);actions=[];errors=[];tokens=0
    for line in (p.parent/'work/events.jsonl').read_text().splitlines():
        e=json.loads(line)
        if e['kind']=='model_response':
            try:actions.append(json.loads(e['text']))
            except ValueError:actions.append({'invalid_json':e['text']})
            tokens+=e['completion_tokens']
        if e['kind']=='tool_result' and 'error' in e['result']:errors.append(e['result']['error'])
    rows.append({'stage':row['stage'],'case_id':row['case_id'],'complete':row['grade']['complete'],
                 'components':row['grade']['components'],'actions':actions,'errors':errors,'generated_tokens':tokens})
write_json(out/'diagnosis.json',rows)
