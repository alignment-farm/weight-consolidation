import json
import platform
import subprocess
import time
from pathlib import Path
commands={'memory':['sysctl','hw.memsize'],'cpu':['sysctl','machdep.cpu.brand_string'],
          'pressure':['memory_pressure'],'processes':['ps','-axo','pid,%cpu,%mem,command'],
          'docker_models':['docker','model','list']}
result={'time_ns':time.time_ns(),'platform':platform.platform(),'commands':{}}
for k,cmd in commands.items():
    p=subprocess.run(cmd,capture_output=True,text=True)
    result['commands'][k]={'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
Path('evidence/resources.json').write_text(json.dumps(result,indent=2)+'\n')
