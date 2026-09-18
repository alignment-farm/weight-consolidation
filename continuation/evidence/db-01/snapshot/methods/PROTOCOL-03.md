# Continuing database work — protocol 03

Declared 2026-09-18 before learner executions. Separate from accepted 491c0f8.
Discovery inspects complete STATE-Bench customer-support jobs and CL Bench real
Tablib/Tenacity PR tasks as well as database questions/migration. Select database
work for a bounded execution check, not for an adapter advantage. Existing CL
Bench already measures continuing schema reuse; our added comparison is weights
on shared history with retained executable SQL and supplied competent documentation.

Pins: CL Bench 5f8c50eb1e84b2eda2ef4faff757dfc812a0ea26; HF database-exploration
snapshot a0cc57eeb9a54f01c0490a1b46cb705b4e05aa19. Existing Amazon-review-derived
SQLite snapshots with constructed schemas and questions, NOT observed enterprise
maintenance histories. One multigroup history, not three independent histories.
This phase is limited continuing-work feasibility unless supplemented independently.

Give BOTH arms actual schemas, all raw read-only SQL, complete mapping/migration
documentation, normalized views, deterministic execution feedback, saved query
execution, exact eligible source records and lexical search. No mappings hidden.
Normalized views are investigator engineering, not agent-acquired code. Collected
SQL is retained as executable source experience; identify its author. Do not make
fixed-weight agents regenerate a working query. There is no question-to-answer
compiler or evaluator feedback tool. Submit a query, execute it and preserve its
complete result; evaluator grades outside the worker.

Partition fixed before outcomes, using upstream question IDs:
- Source0: 2,3,4,6,9,10,11,13,16,17,18,21.
- Development0: 1,5,7,12,14,15.
- Fresh0: 19,20,22,24,25,26,27,28,29,30.
- Source1 after migration: 101,103,106,109,110,113,117.
- Development1: 102,104,107,111.
- Fresh1 after migration: 105,108,112,114,115,116,118,119,120.
- Preserved-obligation probe: previously unused 23 on the migrated snapshot.
Question wording inspected for selection. SQL/answers for initial 1–3 and 101–103
were inspected in discovery, so all are source/development, never fresh. No final
labels or model outcomes guide selection. Source/development may be inspected for
engineering. Fresh labels stay controller-only, loaded only for grading frozen runs.

Initial smoke: development 1 and 12, with the full tools/docs. Confirm database
integrity and source/reference execution. If basic ability is useful, collect all
Source0 with the pinned base as shared collector. Source correctness feedback is
eligible for source corrections only. Keep raw collector failures. Successful
collector final SQL may be retained; failed jobs receive executed investigator
corrections based on source truth. Training uses source-only successful trajectories
or explicitly authored corrections, never development/evaluation. Exact records
and query artifacts are externally reachable in both conditions, checked before
comparison. State0 collection starts without learned history; Source1 collection
uses fixed base with accumulated Source0 history and retained query artifacts.

Initial native model: verified Qwen3-4B Instruct 2507 4-bit pin from prior phase.
Model/recipe not fixed scientific assumptions. First bounded recipe 48 updates,
rank8 last-eight Q/V, seed17, target-only loss, runtime LR0.0005. If acquisition
fails, diagnose interface, data and optimization; try at most one purposeful
alternative (e.g. 96 updates, lower LR, correction trajectory targets), chosen
using source/development. Record decision before fresh results. A model expansion
must follow a concrete capability/resource diagnosis, not a desire for positive
results. Core acquisition criterion: gain on at least one failed source task,
without worse development total. If baseline at source ceiling, assess acquired
behavior through source errors/calls and development, not loss alone.

Use the same selected recipe at two chronological consolidation points. Update1
restarts from base on cumulative Source0+Source1; no optimizer continuation.
Keep interface/action format unchanged across collection, training and checks.
Fresh0 is run after first selection. Its labels/outcomes never enter later data
or recipe choice. Predeclare update1 recipe before Fresh0. Run Fresh1 with fixed
base external reuse, stale adapter0 and cumulative adapter1 to distinguish reuse,
stale learned behavior and updating. All three share current external evidence,
code and documentation. No state-specific tool changes. Include earlier still-valid
obligations and report complete tasks and failures, not only changed columns.

Budget: six action turns initially, 512 generation tokens/turn if instrument
adaptation needed; 20s SQL timeout, bounded result previews with full result artifact.
One MLX worker at a time. Training at most 16 GiB initially. Native token positions,
serving tokens, tool calls, elapsed times, setup/download and correction costs stay
separate. Source acquisition and failed exploration are charged. Unknown authoring,
energy and FLOPs stay unknown. No latency claim on shared hardware.

Before standing down, assess and pursue one useful bounded continuation that can
resolve a remaining uncertainty. Freeze it separately before its fresh outcomes.
Do not stop merely after publication or extend indefinitely merely because the
broader question remains open.

Implementation declaration before first execution: source collection uses a fixed
history within each block (empty for Source0, Source0 for Source1), updated at block
boundaries. The initial backend wrapper permits 512 generated tokens, keeps the
runtime's 6000-token context and 2048-token training-sequence checks, and uses its
unchanged model/tokenizer/adapter verification. SQL snapshots are immutable and
bound/hash-verified separately; no 400MB per-task copies. Exact outputs and queries
are artifacts. File helpers/history are content-pinned state assets. Teacher
reference trajectories preserve the same action schema as execution.
