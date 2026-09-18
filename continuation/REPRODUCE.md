# Continuing-work reproduction

Run from the study root on Apple silicon. The measured machine was an M1 Ultra
with 64 GB; the instrument caps MLX allocation at 16 GiB. Use new output folders.
Old evidence refuses overwrite. The original publication's commands remain in
../REPRODUCE.md and its evidence is unchanged.

If dependencies/assets are absent:

```sh
mkdir -p .deps
git clone https://github.com/alignment-farm/construct-runtime .deps/construct-runtime
git -C .deps/construct-runtime checkout --detach 9ffb10a66180626b80127fb1892b2cf71e39d946
uv sync --project .deps/construct-runtime --extra mlx --locked
git clone https://github.com/pgasawa/continual-learning-bench .deps/continual-learning-bench
git -C .deps/continual-learning-bench checkout --detach 5f8c50eb1e84b2eda2ef4faff757dfc812a0ea26
HF_HUB_DISABLE_XET=1 uv run --project .deps/construct-runtime python -c 'from huggingface_hub import snapshot_download; snapshot_download("mlx-community/Qwen3-4B-Instruct-2507-4bit", revision="50d427756c6b1b2fe0c0a10f67fbda1fc8e82c1b", local_dir="models/qwen3-4b-4bit", max_workers=2)'
uv run --project .deps/construct-runtime python continuation/scripts/fetch_assets.py database
uv run --project .deps/construct-runtime python continuation/scripts/learner_lowrate.py
```

The last command restores exact archived adaptation source from the pinned
runtime and the owned transformation. It checks the original trained source hash.
Full unlicensed runtime source is not vendored in Git; see
[resource provenance](resources/PROVENANCE.md). Base weights and databases remain
ignored. Published database/model hashes are verified. Historical trace paths
remain original provenance strings; `resolve_state` relocates bundled assets and
binds the local base path without rewriting evidence.

To replay the fixed primary comparison from its saved states, without new model
or recipe selection:

```sh
uv run --project .deps/construct-runtime python continuation/scripts/replay_primary.py --source continuation/evidence/db-06 --output continuation/evidence/db-replay-before --point 0
uv run --project .deps/construct-runtime python continuation/scripts/replay_primary.py --source continuation/evidence/db-06 --output continuation/evidence/db-replay-after --point 1
uv run --project .deps/construct-runtime python continuation/scripts/run.py preserved --output continuation/evidence/db-replay-after
```

These reuse the actual published source history and adapters, not a newly
independent learning history. All query answers are recomputed against the pinned
SQLite snapshots. Fresh tasks begin from matched immutable snapshots; evaluation
outputs are preserved but never fed into later training or source selection.

To reproduce optimization itself from the exact eligible source records:

```sh
uv run --project .deps/construct-runtime python continuation/scripts/train.py continuation/evidence/db-06/states/base0 models/qwen3-4b-4bit continuation/evidence/db-06/training-data0/training.json continuation/evidence/adapter0-reproduction 144 0.0001
uv run --project .deps/construct-runtime python continuation/scripts/train.py continuation/evidence/db-06/states/base1 models/qwen3-4b-4bit continuation/evidence/db-06/training-data1/training.json continuation/evidence/adapter1-reproduction 228 0.0001
```

Both start from the pinned base and fresh AdamW. They are six complete passes over
24 and 38 action examples respectively, not optimizer continuation. The native
2048-token training limit, last-eight-layer Q/V rank8 LoRA and seed17 remain.
Package/hardware differences can affect numeric execution; compare recorded
identities and exact artifacts rather than assuming bitwise results on another
platform.

The original collection, capability/model trials and failed recipes are in
`db-01` through `db-05`. Their snapshots and protocol amendments preserve the
code and decisions used then. Protocol 04 reused the twelve actual db-05 Source0
executions, added checked computational teacher programs, and newly collected
seven Source1 jobs. This is not a rerun of source collection under a new model.
The q109 teacher anti-join timed out; `db-06/canonical-overrides1.json` records its
source-only set-difference repair, and `references1-failed-01` preserves failure.
No fresh label or outcome selected that repair or the fixed 228-step update.

The controller entry points for a new protocol-04 replication are:

```sh
uv run --project .deps/construct-runtime python continuation/scripts/canonical_phase.py prepare --output continuation/evidence/db-new
uv run --project .deps/construct-runtime python continuation/scripts/run.py check --output continuation/evidence/db-new --arm base0
uv run --project .deps/construct-runtime python continuation/scripts/run.py train --output continuation/evidence/db-new --steps 144 --learning-rate 0.0001
uv run --project .deps/construct-runtime python continuation/scripts/run.py check --output continuation/evidence/db-new --arm adapter0-144
```

`canonical_phase prepare` deliberately reuses the published db-05 source traces.
For the fixed chronological continuation, use the published decision without
reselecting on replay outcomes. Apply the already documented source-query repair
before new source collection/replay; the original failed attempt stays preserved.

```sh
cp continuation/evidence/db-06/decision.json continuation/evidence/db-new/decision.json
cp continuation/evidence/db-06/canonical-overrides1.json continuation/evidence/db-new/canonical-overrides1.json
uv run --project .deps/construct-runtime python continuation/scripts/run.py fresh --output continuation/evidence/db-new --point 0
uv run --project .deps/construct-runtime python continuation/scripts/canonical_phase.py source1 --output continuation/evidence/db-new
uv run --project .deps/construct-runtime python continuation/scripts/run.py check --output continuation/evidence/db-new --point 1 --arm base1
uv run --project .deps/construct-runtime python continuation/scripts/run.py train --output continuation/evidence/db-new --point 1 --steps 228 --learning-rate 0.0001
uv run --project .deps/construct-runtime python continuation/scripts/run.py check --output continuation/evidence/db-new --point 1 --arm adapter1-228
uv run --project .deps/construct-runtime python continuation/scripts/run.py fresh --output continuation/evidence/db-new --point 1
uv run --project .deps/construct-runtime python continuation/scripts/run.py preserved --output continuation/evidence/db-new
```

New collection can differ numerically; this is a replication using published
partitions and decisions, not an independent history or a reconstruction of the
original decision timestamp. Saved-state replay above reproduces the exact
published comparison inputs. The historical frozen-code audit applies to the
published folders, not a newly collected folder using today's utility scripts.

Offline verification of the published record (no model generation or training):

```sh
uv run --project .deps/construct-runtime python continuation/scripts/learner_lowrate.py
uv run --project .deps/construct-runtime python continuation/scripts/validate_environment.py
uv run --project .deps/construct-runtime python continuation/scripts/audit.py --output continuation/evidence/db-05
uv run --project .deps/construct-runtime python continuation/scripts/audit.py --output continuation/evidence/db-06
uv run --project .deps/construct-runtime python continuation/scripts/check_components.py continuation/evidence/db-06
uv run --project .deps/construct-runtime python continuation/scripts/summarize.py
```

The audit resolves and verifies states, checks identical external assets within
each comparison, reads exact training records through the public tool, verifies
recorded model/adapter identities, preserves cumulative source prefixes and
recomputes report grades/artifact hashes. Component execution checks use the same
`run_saved` tool available to workers. This is an accidental-leakage/process
boundary, not an adversarial OS sandbox or proof against pretraining contamination.
The controller parses the upstream question bank; workers receive only public
question/revision fields and the declared inherited history/tools.

For the rejected larger-model trial, optionally fetch the exact 7B pin with
`fetch_assets.py 7b`, then prepare a new output with `run.py prepare --model-profile
7b` and use the fixed development IDs in protocol 03. No 7B adapter was trained.
