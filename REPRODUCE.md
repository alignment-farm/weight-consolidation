# Reproduction

Run from this repository on Apple silicon with sufficient free unified memory.
Only one heavy worker at a time. All output directories must be new. The runtime
checks exact base/tokenizer, adapter and state hashes; no existing output is reused.

```sh
mkdir -p .deps
git clone https://github.com/alignment-farm/construct-runtime .deps/construct-runtime
git -C .deps/construct-runtime checkout --detach 9ffb10a66180626b80127fb1892b2cf71e39d946
uv sync --project .deps/construct-runtime --extra mlx --locked
uv run --project .deps/construct-runtime python -c 'from huggingface_hub import snapshot_download; snapshot_download("mlx-community/Qwen3-4B-Instruct-2507-4bit", revision="50d427756c6b1b2fe0c0a10f67fbda1fc8e82c1b", local_dir="models/qwen3-4b-4bit", max_workers=2)'
uv run --project .deps/construct-runtime python scripts/study.py prepare --output evidence/reproduction
uv run --project .deps/construct-runtime python scripts/study.py smoke --output evidence/reproduction
uv run --project .deps/construct-runtime python scripts/study.py baseline --output evidence/reproduction
uv run --project .deps/construct-runtime python scripts/study.py traincheck --output evidence/reproduction --steps 32
```

These commands reproduce the improved pilot-02 interface. Pilot-01's earlier
interface and controller are preserved in evidence/pilot-01/snapshot. Every
snapshot records the source used at that decision; the root scripts contain the
completed controller. A new acquisition search must make its own development
selection decision before testing. To reproduce the FIXED reported 32-step
comparison, continue without reselecting based on reproduction outcomes:

```sh
uv run --project .deps/construct-runtime python scripts/extension.py evidence/reproduction 32 v1
uv run --project .deps/construct-runtime python scripts/extension.py evidence/reproduction 32 v2
uv run --project .deps/construct-runtime python scripts/fixed_decision.py evidence/reproduction
uv run --project .deps/construct-runtime python scripts/study.py evaluate --output evidence/reproduction --steps 32
uv run --project .deps/construct-runtime python scripts/audit.py evidence/reproduction
uv run --project .deps/construct-runtime python scripts/diagnose.py evidence/reproduction
```

The extension's v1 checks preserve the development failure in which correct
compiler output was overwritten. V2 is the final stronger external-reuse harness.
The adapter is trained under the original manual-configuration harness; no
compiler-harness retraining occurs. Training always starts from base with a fresh
optimizer. Do not call it optimizer continuation.

Offline audit of the published run (no model loaded):

```sh
uv run --project .deps/construct-runtime python scripts/audit.py evidence/pilot-01
uv run --project .deps/construct-runtime python scripts/audit.py evidence/pilot-02
uv run --project .deps/construct-runtime python scripts/diagnose.py evidence/pilot-02
```

The evaluator and source generator are controller-only modules. Workers receive
only public tasks and content-pinned state bundles; expected outputs are not put
in model context or exposed by tools. This is a trusted process boundary, not an
OS sandbox. Evidence stores exact requests, responses, actions, failures, output
artifacts, provenance, selection and training costs. Paths in historical traces
are original paths, not rewritten relocation claims. `resolve_state` supports
moving bundles and rebinding base weights locally.

The source model files and .deps environment are ignored by Git. Small adapters,
states and full study traces are retained. The runtime does not include an
explicit license in its pinned tree; local use is commissioned, and this study
does not redistribute its source. See resources/PROVENANCE.md.

## Corrected full-source-access confirmation

The initial pilot exposed only compact source configurations externally. Its
adapter comparison is exploratory. The corrected, fixed-candidate experiment
uses the published pilot source history and adapter (no new optimization):

```sh
uv run --project .deps/construct-runtime python scripts/confirmation.py prepare evidence/confirmation-reproduction
uv run --project .deps/construct-runtime python scripts/confirmation.py recheck evidence/confirmation-reproduction
uv run --project .deps/construct-runtime python scripts/confirmation.py evaluate evidence/confirmation-reproduction
uv run --project .deps/construct-runtime python scripts/audit.py evidence/confirmation-reproduction
uv run --project .deps/construct-runtime python scripts/diagnose.py evidence/confirmation-reproduction
```

For offline verification of the actual corrected run:

```sh
uv run --project .deps/construct-runtime python scripts/audit.py evidence/confirmation-01
uv run --project .deps/construct-runtime python scripts/diagnose.py evidence/confirmation-01
uv run --project .deps/construct-runtime python scripts/costs.py evidence
```

The confirmation prepare command verifies all sixteen training rows are accessible
through every state's public `read_source` tool; the audit rechecks their contents.
Reproduction inherits the fixed published source history and adapter and does not
claim a new independent learning history. To reproduce acquisition itself, use the
pilot commands first. The corrected comparison's new seeds change row values and
IDs, not the predeclared contract-combination schedule.
