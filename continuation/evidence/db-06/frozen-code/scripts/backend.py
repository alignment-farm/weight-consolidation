"""Pinned runtime model verification with a disclosed 512-token generation limit."""
import time
from construct_runtime.model import MLXModel

class StudyModel(MLXModel):
    def __init__(self,config):
        super().__init__(config)
        self.identity['generation']['max_tokens']=512
        self.identity['study_backend']='continuation/scripts/backend.py; native runtime loader unchanged'
        from pathlib import Path
        from construct_runtime.records import file_hash
        self.identity['study_backend_sha256']=file_hash(Path(__file__))
        self.identity['database_binding']=config.get('study_database_binding')
    def generate(self,messages):
        from mlx_lm.generate import generate_step
        from mlx_lm.sample_utils import make_sampler
        ids=self.encode(messages)
        if len(ids)>6000:raise ValueError('context exceeds 6000-token budget; no silent truncation')
        start=time.monotonic();tokens=[];ended=False
        for token,_ in generate_step(self.mx.array(ids),self.model,max_tokens=512,sampler=make_sampler(temp=0)):
            tokens.append(int(token))
            if token in self.tokenizer.eos_token_ids:ended=True;break
        return {'text':self.tokenizer.decode(tokens[:-1] if ended else tokens),'prompt_tokens':len(ids),'completion_tokens':len(tokens),'token_ids':tokens,'ended':ended,'seconds':time.monotonic()-start,'peak_mlx_bytes':self.mx.get_peak_memory(),'compute_flops':None}
