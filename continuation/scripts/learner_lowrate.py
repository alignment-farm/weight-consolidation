"""Reconstruct the exact owned adaptation without vendoring unlicensed runtime source."""
import hashlib
import importlib.util
import json
from pathlib import Path
from construct_runtime import learner as upstream

NATIVE_SHA256='32917b5ea07aba2c4fb27aa15bb60732a5da8329635f4f931a2b2c4ddfe81e86'
ADAPTED_SHA256='964c258768282cbae8bff7c6967423cf685ce0e787d323c8b03ce33eaa64304c'

def source_text():
    source=Path(upstream.__file__).read_text()
    assert hashlib.sha256(source.encode()).hexdigest()==NATIVE_SHA256,'pinned native learner changed'
    source=source.replace('from .experience import','from construct_runtime.experience import').replace('from .model import LORA, MLXModel','from construct_runtime.model import LORA\nfrom backend import StudyModel as MLXModel').replace('from .records import','from construct_runtime.records import')
    source=source.replace('def train(config, data_path, output, steps):','def train(config, data_path, output, steps, learning_rate=0.0001):').replace('"learning_rate": 0.0005,','"learning_rate": learning_rate,\n        "owned_learner_sha256": file_hash(Path(__file__)),\n        "adaptation": "native pinned trainer with configurable lower learning rate; objective/order/optimizer unchanged",')
    source='# Adapted from Construct Runtime 9ffb10a66180626b80127fb1892b2cf71e39d946.\n'+source
    assert hashlib.sha256(source.encode()).hexdigest()==ADAPTED_SHA256
    return source

def train(*args,**kwargs):
    root=Path(__file__).resolve().parents[2]
    path=root/'.deps/weight-study-adaptation/learner_lowrate.py';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(source_text())
    spec=importlib.util.spec_from_file_location('_weight_study_owned_learner',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.train(*args,**kwargs)

def restore_snapshots():
    root=Path(__file__).resolve().parents[2];source=source_text();count=0
    for manifest in (root/'continuation/evidence').rglob('learner_lowrate.py.reconstruct.json'):
        metadata=json.loads(manifest.read_text());assert metadata['sha256']==ADAPTED_SHA256
        target=manifest.with_name('learner_lowrate.py')
        if target.exists():assert hashlib.sha256(target.read_bytes()).hexdigest()==ADAPTED_SHA256
        else:target.write_text(source)
        count+=1
    return count

if __name__=='__main__':print('Verified/restored exact archived trainer sources:',restore_snapshots())
