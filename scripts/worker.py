import json
import sys
from pathlib import Path
from construct_runtime.executor import execute
from construct_runtime.state import resolve_state

state, model, task, output = sys.argv[1:]
execute(json.loads(Path(task).read_text()),resolve_state(state,model),Path(output))
