import sys
from construct_runtime.learner import train
from construct_runtime.state import resolve_state
state, model, data, output, steps = sys.argv[1:]
train(resolve_state(state,model),data,output,int(steps))
