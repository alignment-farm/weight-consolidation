"""Bounded source-only diagnostic: final loss and generation under inherited-history metadata change."""
import json,sys,time
from pathlib import Path
import mlx.core as mx
import mlx.nn as nn
from construct_runtime.executor import messages_for
from construct_runtime.records import read_json,write_json
from construct_runtime.state import resolve_state
from construct_runtime.environment import parse_action
from backend import StudyModel
import run

out=Path(sys.argv[1]).resolve();arm=sys.argv[2];run.configure(out)
folder=out/'context-diagnosis'/arm;folder.mkdir(parents=True,exist_ok=False)
cfg=resolve_state(out/'states'/arm,run.MODEL);model=StudyModel(cfg)
rows=read_json(out/'training-data0/training.json');cases=run.bank();results=[]
for i in [2,21]:
    row=next(r for r in rows if r['case_id']==f'q{i}')
    deployment=messages_for(run.task(cases[i],'before'),read_json(cfg['experience']),'base',run.DatabaseWork(),cfg)
    for context,messages in [('recorded_source',row['messages']),('deployment',deployment)]:
        prefix=model.encode(messages);target=model.tokenizer.encode(row['target'],add_special_tokens=False)+[model.tokenizer.eos_token_id]
        tick=time.monotonic();ids=mx.array(prefix+target)[None,:]
        logits=model.model(ids[:,:-1])[:,len(prefix)-1:,:]
        loss=nn.losses.cross_entropy(logits.astype(mx.float32),ids[:,len(prefix):],reduction='mean');mx.eval(loss)
        loss_seconds=time.monotonic()-tick
        generation=model.generate(messages)
        try:action=parse_action(generation['text']);valid=True
        except ValueError:action=None;valid=False
        results.append({'id':i,'context':context,'query_target_nll':loss.item(),'loss_input_tokens':len(prefix)+len(target)-1,'loss_target_tokens':len(target),'loss_seconds':loss_seconds,'generation':generation,'valid_json_action':valid,'action':action,'messages':messages})
write_json(folder/'result.json',{'arm':arm,'identity':model.identity,'results':results,'scope':'Source-only first-action diagnostic, not complete tasks, no candidate selection or fresh labels. Same model/target, recorded source context versus deployed history metadata.'})
print(arm,[(r['id'],r['context'],round(r['query_target_nll'],4),r['valid_json_action']) for r in results],flush=True)
