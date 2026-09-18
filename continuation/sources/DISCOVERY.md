# Workload and methods discovery, 18 September 2026

This is inspected implementation evidence and investigator inference, not a
reproduction of author-reported scores. Selection preceded adapter training and
fresh outcomes. The API metadata response is cached in `arxiv-metadata.xml` (one
combined request, descriptive weight-consolidation-study User-Agent). Exact paper
versions inspected: [CL-Bench 2606.05661v1](https://arxiv.org/html/2606.05661v1),
[BIRD-INTERACT 2510.05318v1](https://arxiv.org/html/2510.05318v1), and
[HarnessForge 2606.01779v1](https://arxiv.org/html/2606.01779v1).

CL-Bench already investigates shared-environment reuse with ICL and memory
systems, including schema drift. Its database protocol counts exploratory queries
and checks final answers; our local protocol instead requires an executed full
result artifact and counts all model/tool work. We supply mappings and views that
its original hidden-schema setting asks agents to discover. Thus this study tests
the incremental effect of weights under stronger explicit support, not the
published leaderboard setting. No published outcome is claimed reproduced.

BIRD's interaction and executable-check design motivates retaining ordinary
feedback. HarnessForge's interface-specific policy alignment motivates checking
that source targets use exactly the current tool action format; its public
results do not establish that this local learner will acquire useful behavior.
The prior study's source ledger remains the basis for combined memory/LoRA and
correction methods; this phase does not claim novelty for hybrid learning itself.

## Complete jobs inspected

**Database reporting and change — selected for first execution.**
CL-Bench code at
[`5f8c50eb1e84b2eda2ef4faff757dfc812a0ea26`](https://github.com/pgasawa/continual-learning-bench/tree/5f8c50eb1e84b2eda2ef4faff757dfc812a0ea26),
Apache-2.0. Inspected task README, variants, evaluator, build script, migration
implementation and question files. Early examples include invalid future office
review timestamps, unique user counts, and electronic price aggregation; later
examples query active office products and authoritative migrated prices. Inspected
SQL/answers only for source/development jobs before execution. Workers must choose
joins, units, aggregation and current fields, then return an executed report.
Earlier experience can retain correct query patterns; later jobs compose them or
must override stale columns. SQL, schema inspection, full mapping documentation,
normalized views and saved-query execution already solve much of the work. The
remaining small-model question is reliable semantic composition, not memorizing
hidden schema. Existing source questions and migration are constructed from an
Amazon-review-derived database, not observed enterprise jobs. One database with
three groups is one history, not three independent histories.

HF database revision `a0cc57eeb9a54f01c0490a1b46cb705b4e05aa19` is pinned in
`database-manifest.json`; per-file hashes and integrity checks are in each run.
The HF database repository exposes no license card inspected here. Databases are
not redistributed. Upstream attributes raw data to McAuley-Lab/Amazon-Reviews-2023.
The Apache code license is copied in `LICENSE-CL-Bench`; copied README canaries
remain intact. Source-only online adaptation here is explicitly disclosed;
benchmark data must not be repackaged as a general training corpus. No held-out
questions, labels or trajectories enter the adapter training export.

**Real codebase maintenance — viable independent follow-up, not rejected by an
adapter outcome.** Same CL-Bench code pin. Inspected the complete problem, patch,
test patch, base commit, evaluator and required tests for `jazzband__tablib-534`
and `jd__tenacity-597` in `data/codebase_adaptation/final-dataset.jsonl`.
Tablib at `bbc273951cefc616f1a865dd1c21003859a9da14` mishandles YAML dictionaries;
the job requires an UnsupportedFormat guard while preserving ordinary imports
(one failure-to-pass and 113 passing regression tests). Tenacity at
`213446e8f5f73ca0d20e22ec8ee38b1f75a45434` needs meaningful names for retry contexts
while preserving decorators, copied retry objects, async behavior and logging
(11 failure-to-pass and 95 regression tests). Existing tests, grep, retained
patches and repository code are the competent external tools. Prior fixes could
teach architecture and compatibility constraints, but full patches exceed our
initial six-action SQL interface and require historical dependency installation.
The small available pool (19 tasks across two projects) and historical leakage
need care: the Tenacity problem includes implementation discussion/coauthor text,
which cannot be treated as an unedited contemporaneous issue. This is a promising
independent-history continuation after basic acquisition feasibility, not evidence
that a 4B/7B learner can already perform the complete patch jobs.

**Enterprise customer support — bounded alternative inspected.**
STATE-Bench at
[`5644b1838d96bc4483da29642d058ecaa6f80f7f`](https://github.com/microsoft/STATE-Bench/tree/5644b1838d96bc4483da29642d058ecaa6f80f7f),
MIT. Read README, learning/scoring interfaces and complete task/environment pairs
`11-cancel_before_shipment` and `38-exchange_outside_window`. The former requires
previewing a $599 card-order cancellation before committing it. The latter must
explain refusal of a 35-day-old electronics exchange outside a 15-day window;
its state requirements are empty, so conversation judgment is consequential.
Prior cases could teach policy and workflow ordering, but policy retrieval and
preview tools already provide explicit support. Generated task data, simulated
users and a GPT-5.4 judge add a separate measurement problem. Not selected for the
first bounded local comparison because the database route has executable
controller-side checking without a paid conversation judge.

**Interactive SQL alternative.** BIRD-Interact code at
[`451fe2c3518ee1cf908d8139e2913483bd519381`](https://github.com/bird-bench/BIRD-Interact/tree/451fe2c3518ee1cf908d8139e2913483bd519381),
MIT; HF `birdsql/mini-interact` at
`088b3787303e69129e395a9f712902670339ef72`, card CC-BY-SA-4.0.
Inspected the `alien1` ADK interaction sample, SQLite evaluator and actual
`mini_interact.jsonl` records (300 tasks). These contain injected ambiguities and
follow-up requirements, but inspected public `sol_sql`/`test_cases` fields are
empty. The first study would need additional evaluation assets or an independently
constructed oracle. No request was sent to authors. We selected the already
executable CL-Bench data instead; this is an asset/measurement decision, not a
claim that interaction is unimportant.

## Local acquisition boundary

Source collection is fixed base with the block's inherited history. Correct final
SQL is retained; failed source jobs receive upstream-reference SQL as an explicitly
authored correction. The two-action submit/finish teaching replay is investigator
construction even when its SQL came from the worker. Development and final
correctness are never tool feedback. Teacher-model tokens are zero for these
replays; investigator reasoning/engineering tokens and upstream authors' effort
are unknown, not free. See protocol 03 for timing, split and failure diagnostics.
