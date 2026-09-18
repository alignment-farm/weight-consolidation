"""Aggregate incurred costs across preserved pilots, native units only."""
import json
from pathlib import Path
import sys
from construct_runtime.records import read_json,write_json
root=Path(sys.argv[1]);totals={};stages=[];training=[]
for pilot in sorted([*root.glob('pilot-*'),*root.glob('confirmation-*')]):
    if not (pilot/'audit.json').exists():continue
    a=read_json(pilot/'audit.json')
    for stage,c in a['costs'].items():
        stages.append({'pilot':pilot.name,'stage':stage,**c})
        for k,v in c.items():totals[k]=totals.get(k,0)+v
    training += [{'pilot':pilot.name,**x} for x in a['training'] if x.get('trained_in_this_run',True)]
remote=read_json(root/'remote-smoke.json')
write_json(root/'costs.json',{'model_execution_totals':totals,'stages':stages,'training':training,
 'remote_smoke':{'usage':remote['usage'],'timings':remote.get('timings'),'matched_comparison':False},
 'authored_reference_actions':16,'authored_reference_trajectories':8,'reference_execution_seconds':None,
 'direct_compiler_evaluation':[read_json(p) for p in sorted((root/'pilot-02/direct-compiler').glob('*/grade.json'))],
 'download':{'model_weight_bytes':2263022417,'snapshot_progress_reported_seconds':244,'hashing_seconds':None},
 'unknown':['authoring-agent tokens','investigator labor','compiler development effort','energy','FLOPs','total setup/checking overhead'],
 'accounting':'evaluation stages are the prospective use horizon; all other model runs are experimental acquisition/development/search, including failures and reset; model/tool seconds are components of worker seconds, not additive to it; native token and time units not interchangeable'})
print(json.dumps(totals,indent=2))
