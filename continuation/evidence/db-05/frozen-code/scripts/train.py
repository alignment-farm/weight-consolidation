import sys
from construct_runtime.state import resolve_state
from backend import StudyModel
state,model,data,output,steps,*extra=sys.argv[1:]
if extra:
    import learner_lowrate as learner
    learner.train(resolve_state(state,model),data,output,int(steps),float(extra[0]))
else:
    from construct_runtime import learner
    learner.MLXModel=StudyModel
    learner.train(resolve_state(state,model),data,output,int(steps))
