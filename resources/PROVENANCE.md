# Instrument and acquisition

Runtime: https://github.com/alignment-farm/construct-runtime at
9ffb10a66180626b80127fb1892b2cf71e39d946, owned ignored checkout .deps/construct-runtime.
Installed with `uv sync --project .deps/construct-runtime --extra mlx --locked`.
The upstream uv.lock is the dependency lock; each state and execution records
source hashes and MLX/MLX-LM/Transformers versions. Runtime code unchanged.

model.json is copied from that exact revision. Model files downloaded locally
from mlx-community/Qwen3-4B-Instruct-2507-4bit at
50d427756c6b1b2fe0c0a10f67fbda1fc8e82c1b. Its card declares Apache-2.0.
Model and tokenizer file hashes are checked at every model load. Base tensor
immutability and loaded adapter tensor hashes checked by runtime. Download log
records about 244 seconds for snapshot retrieval; hashing is additional. The
manifest's download_and_hash_seconds field is UPSTREAM historical metadata, not
this study's download time. Local model.safetensors is 2,263,022,417 bytes.

Hardware: Apple M1 Ultra, 64 GiB. No competing MLX training worker observed before
launch. Runs sequential, runtime allocation cap 16 GiB. Process and pressure
snapshot in evidence/resources.json; no exclusive hardware lease or controlled
latency benchmark is claimed. Remote smoke uses a different Qwen3 8B GGUF and
is NOT part of the matched comparison; see remote-models.json and remote-smoke.json.
It confirms inference access, not gradient/adapter support.
