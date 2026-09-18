"""Prospective compiler reuse comparison; no extra optimization."""
import sys
from pathlib import Path
import shutil
sys.path.insert(0,str(Path(__file__).resolve().parent))
from study import ROOT, MODEL, log, run_case, read_json, write_json, file_hash, create_state, resolve_state

out=Path(sys.argv[1]).resolve();steps=int(sys.argv[2])
for folder in ['workload','scripts','methods']:
    shutil.copytree(ROOT/folder,out/'extension-snapshot'/folder,ignore=shutil.ignore_patterns('__pycache__'))
for arm in ['base',f'adapter-{steps}']:
    cfg=resolve_state(out/'states'/arm,MODEL)
    parent=cfg.pop('state',None)
    cfg['environment']={'path':str(ROOT/'workload/environment_compiled.py'),'sha256':file_hash(ROOT/'workload/environment_compiled.py')}
    cfg['inherited_artifacts']['compile_contract.py']=str(ROOT/'workload/compile_contract.py')
    cfg.pop('inherited_artifact_hashes',None)
    create_state(cfg,out/'states'/('compiled-'+arm),'compiled-'+arm,parent=parent,
                 decision={'reason':'prospective stronger external reuse route, same adapter; no outcome-based tuning'})
    for c in read_json(out/'controller-cases.json'):
        if c['split']=='development':run_case(out,'compiled-'+arm,c,'compiled-check-'+arm)
log(out,'compiler_development_finished',steps=steps)
