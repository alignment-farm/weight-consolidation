"""Checks focused on semantic defects and leakage boundaries, not a mirrored implementation."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from workload.fixtures import case
from workload.transform import reconcile
from workload.compile_contract import compile_contract
from workload.environment import Reconcile
from workload.environment_compiled_parity import ReconcileCompiled

for split,n in [('source',8),('development',4)]:
    for i in range(n):
        c=case(split,i)
        assert reconcile(c['task'],compile_contract(c['task']['contract']))==c['expected']
c=case('source',0)
for mutation in [{'accept':['posted','void']},{'dedup':'latest'},{'credit_negative':False},{'units':'minor'}]:
    try:actual=reconcile(c['task'],{**c['config'],**mutation})
    except ValueError:continue
    assert actual!=c['expected'],mutation
for env in [Reconcile(),ReconcileCompiled()]:
    try:env.validate_task({**c['task'],'expected':c['expected']})
    except ValueError:pass
    else:raise AssertionError('truth field accepted')
for invalid in [c['task']['contract']+' Amounts are integer cents.', c['task']['contract'].replace('Accept statuses','Eligible states')]:
    try:compile_contract(invalid)
    except ValueError:pass
    else:raise AssertionError('ambiguous or unsupported contract accepted')
print('12 source/development oracle agreements, 4 semantic mutations, 2 label-boundary and 2 parser checks passed')
