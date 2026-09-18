import sys
from construct_runtime.state import resolve_state
from construct_runtime import learner
from backend import StudyModel
state,model,data,output,steps=sys.argv[1:]
learner.MLXModel=StudyModel
learner.train(resolve_state(state,model),data,output,int(steps))
