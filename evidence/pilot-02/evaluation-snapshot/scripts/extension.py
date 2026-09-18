"""Prospective compiler reuse comparison; no extra optimization."""
import sys
from pathlib import Path
import shutil
sys.path.insert(0,str(Path(__file__).resolve().parent))
from study import ROOT, MODEL, log, run_case, read_json, write_json, file_hash, create_state, resolve_state

out=Path(sys.argv[1]).resolve();steps=int(sys.argv[2]); version=sys.argv[3] if len(sys.argv)>3 else 'v1'
prefix='compiled-' if version=='v1' else 'compiled-v2-'
env='environment_compiled.py' if version=='v1' else 'environment_compiled_v2.py'
for folder in ['workload','scripts','methods']:
    shutil.copytree(ROOT/folder,out/('extension-snapshot-'+version)/folder,ignore=shutil.ignore_patterns('__pycache__'))
for arm in ['base',f'adapter-{steps}']:
    cfg=resolve_state(out/'states'/arm,MODEL)
    parent=cfg.pop('state',None)
    cfg['environment']={'path':str(ROOT/'workload'/env),'sha256':file_hash(ROOT/'workload'/env)}
    cfg['inherited_artifacts']['compile_contract.py']=str(ROOT/'workload/compile_contract.py')
    cfg.pop('inherited_artifact_hashes',None)
    create_state(cfg,out/'states'/(prefix+arm),prefix+arm,parent=parent,
                 decision={'reason':'prospective stronger external reuse route, same adapter; no outcome-based tuning'})
    for c in read_json(out/'controller-cases.json'):
        if c['split']=='development':run_case(out,prefix+arm,c,prefix+'check-'+arm)
log(out,'compiler_development_finished',steps=steps)
