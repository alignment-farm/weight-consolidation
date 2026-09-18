"""Freeze the published recipe for reproduction; does not select on new outcomes."""
import sys,time
from pathlib import Path
from construct_runtime.records import write_json,file_hash
out=Path(sys.argv[1])
if (out/'decision.json').exists() or (out/'evaluation-cases.json').exists():
    raise ValueError('decision/evaluation already exists')
write_json(out/'decision.json',{'time_ns':time.time_ns(),'selected_steps':32,
           'deployment_promotion':False,'reason':'fixed replication of published 32-step recipe, no selection on replication outcomes',
           'protocol_sha256':file_hash('methods/PROTOCOL-01.md')})
