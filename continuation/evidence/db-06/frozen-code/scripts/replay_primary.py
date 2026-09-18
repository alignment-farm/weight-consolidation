"""Replay frozen primary conditions from saved states, without rerunning selection."""
import argparse,shutil
from pathlib import Path
import run
from construct_runtime.records import read_json,write_json
p=argparse.ArgumentParser();p.add_argument('--source',default='continuation/evidence/db-05');p.add_argument('--output',required=True);p.add_argument('--point',type=int,choices=[0,1],required=True);a=p.parse_args()
source=Path(a.source).resolve();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=False)
for name in ['model-profile.json','decision.json',f'database-{"before" if a.point==0 else "after"}.json']:
    shutil.copyfile(source/name,out/name)
run.configure(out);decision=read_json(out/'decision.json')
arms=[decision['base0_arm'],decision['adapter0_arm']] if a.point==0 else ['base1',f"adapter1-{decision['later_steps']}",'stale1']
for arm in arms:shutil.copytree(source/'states'/arm,out/'states'/arm)
rows=run.bank();revision='before' if a.point==0 else 'after'
for n,i in enumerate(run.PARTS[f'fresh{a.point}']):
    for arm in arms if n%2==0 else list(reversed(arms)):
        run.run_case(out,arm,rows[i],revision,'replay-'+arm)
