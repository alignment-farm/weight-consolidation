import os,sys
from pathlib import Path
from construct_runtime.records import read_json,file_hash,write_json
from construct_runtime.state import resolve_state
from construct_runtime.executor import execute
from backend import StudyModel
state,model,database,binding,task,output=sys.argv[1:]
assert file_hash(database)==read_json(binding)['sha256'],'database identity mismatch'
os.environ['WC_DATABASE_PATH']=database
cfg=resolve_state(state,model)
from construct_runtime import model as runtime_model
runtime_model.MLXModel=StudyModel
cfg['study_database_binding']=read_json(binding)
execute(read_json(task),cfg,output)
