"""Fetch pinned large assets into ignored owned paths; verify published manifests."""
import argparse,hashlib,json,os,time
from pathlib import Path
os.environ.setdefault('HF_HUB_DISABLE_XET','1')
from huggingface_hub import snapshot_download,hf_hub_download
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('asset',choices=['database','7b']);args=p.parse_args()
start=time.monotonic()
if args.asset=='database':
    manifest=json.loads((ROOT/'continuation/sources/database-manifest.json').read_text())
    for name in ['products.db','products_drifted.db']:
        hf_hub_download(manifest['repository'],name,repo_type='dataset',revision=manifest['revision'],local_dir=ROOT/'.deps/cl-databases')
else:
    manifest=json.loads((ROOT/'continuation/resources/model7b.json').read_text())
    path=ROOT/'models/qwen2.5-coder-7b-4bit'
    snapshot_download(manifest['repository'],revision=manifest['revision'],local_dir=path)
    for name,expected in manifest['files'].items():
        assert hashlib.sha256((path/name).read_bytes()).hexdigest()==expected,name
print(json.dumps({'asset':args.asset,'download_verify_seconds':time.monotonic()-start}))
