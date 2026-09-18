# Resource and adaptation provenance

Primary learner: the original verified 4-bit Qwen3-4B Instruct 2507 model and
tokenizer in ../../resources/model.json. No new download of that base was charged
in this follow-up. An exploratory Qwen2.5-Coder-7B 4-bit download and six matched
development executions are preserved; model7b.json pins its exact HF revision,
file hashes, card license and measured HTTP download/hash time. An earlier Xet
attempt stalled after 64 MiB and was terminated; its duration was not instrumented.
The 7B candidate was rejected on development capability, before any adapter result.

hardware.json and memory-before-7b.txt record the local Apple M1 Ultra/64 GB check.
remote-models.json is the successful read-only response from the authorized remote
Docker Model Runner endpoint. No remote inference, gradient or adapter experiment
was conducted. All measured model tasks and training used local MLX, serially,
with the pinned dependency and a 16 GiB memory cap. These are incurred execution
times, not controlled hardware latency benchmarks.

The database HF revision is pinned in ../sources/database-manifest.json; exact
published file hashes are in database-files.json and every prepared run. SQLite
and Python versions are in sqlite.json. Large databases and base weights are not
redistributed. Code/data inspection and applicable license observations are in
../sources/DISCOVERY.md; copied CL-Bench documentation retains its canary and
Apache-2.0 license. Canonical source SQL is investigator adaptation of eligible
source queries at the pinned CL-Bench revision, not newly collected agent code.

Construct Runtime remains at 9ffb10a66180626b80127fb1892b2cf71e39d946 with no changes
to the dependency checkout. The pinned runtime has no explicit license file.
Its full source is fetched during setup, not vendored in Git. The owned lower-rate
trainer adaptation is reconstructed by ../scripts/learner_lowrate.py from the
pinned native source and exact text transformations. The resulting source hash
964c258768282cbae8bff7c6967423cf685ce0e787d323c8b03ce33eaa64304c is the actual
algorithm hash recorded in all lower-rate training recipes. Archive sidecars
reconstruct identical source bytes for audit. This packaging change occurred
after all training and changes no trained weights or experiment results.

The backend wrapper changes generation allowance to 512 tokens while retaining
native loading, base/tokenizer verification, adapter compatibility/tensor checks,
greedy sampling, 6000-token context and fresh process/cache behavior. Owned source
and its hash are captured in each model identity and frozen experiment snapshot.
No optimizer state or previous adapter is inherited by training.

Investigator/Codex work includes discovery, tools, normalization, source corrections,
canonical programs, protocols and reporting. Its token/time cost and upstream
artifact construction costs are unknown. No separate API teacher was called;
that does not make investigator teaching or engineering free.
