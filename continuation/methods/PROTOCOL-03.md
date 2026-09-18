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
engineering. Fresh labels stay controller-only and are used only for grading frozen runs.
The JSON bank loader parses the entire upstream file in controller memory; this
is an access boundary, not a claim that held-out bytes are never loaded. Only
selected source rows enter teaching replay and only question text enters workers.

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

## Smoke diagnosis before collection: db-01 -> db-02

Two failures preserved. Q1 shows the helper dropped huge corrupt epochs when SQLite
returned NULL date/year; add raw epoch_seconds and document range behavior. Q12
returns one review count per qualifying product instead of a product count; add a
general grouped-count reminder to both arms. Also separate before/after helper and
handbook assets: db-01's full handbook prematurely disclosed migration mappings.
That discovery smoke is not eligible source history. db-02 withholds later mapping
names/code from all before-migration worker assets. Helpers are known current
capabilities, never future patch solutions. Keep action schemas constant after this
repair. Check both smoke jobs again before collection. No fresh outcomes inspected.

## Capability diagnosis and bounded model expansion

Repaired db-02 Qwen3-4B completes source capability probes 2/2 (q2,q9) but
development 1/6 (q5; fails q1,q7,q12,q14,q15). Before any learning, try
Qwen2.5-Coder-7B-Instruct 4-bit at HF revision
019cc73c45c770444708a6dd8690c66243cc5c80 with the same interface and six development
jobs. This is a capability decision, not selection on adapter advantage. The
4.28GB download and all 4B development work are experimental search costs. Keep
serial execution and the initial 16GiB training cap. Prefer 7B only if baseline
behavior improves; otherwise diagnose the environment/model boundary. No fresh
outcomes have been examined. The runtime, action budget and initial learning
recipe stay unchanged.

## Turn-budget check before learner/model selection

Detailed db-02 inspection shows q15 has a correct final artifact but consumes its
sixth turn on submit, leaving no finish turn. Increase the common allowance to
eight actions and repeat all six development jobs with 4B (db-03) and 7B (db-04).
This avoids treating a completion-budget failure as SQL incapability or favoring
the larger model through unequal budgets. Preserve both complete-task and artifact
correctness. The public tools, prompts, data split and learning recipe are unchanged.
Eight turns become the common source/development/fresh allowance after this check.

The 4B eight-turn development pass completes 2/6 (q5, q15). Q15's earlier
artifact was correct; extra time restores its finish. Q1/q7/q12/q14 remain wrong,
so the diagnosed capability issue is not solely a turn-limit effect.

## Model selection before source collection and learning

The matched 7B candidate (db-04) completes 1/6, versus 4B 2/6 (db-03). It mistakes
median for mean, mishandles aggregation and sometimes repeats retrieval without
executing. Select 4B for the primary db-05 comparison: it has better development
behavior and lower resource use in this check. This does not establish general
model superiority. No additional model search is planned. Useful simple source
execution was already demonstrated; now establish the developed external-reuse
baseline after all twelve source jobs before interpreting any learning result.
Proceed with the declared 48-update recipe and one purposeful alternative if
behavioral acquisition fails. No fresh outcomes have been examined.

## Cumulative exposure declaration before first training result

Source0 exports 24 action examples; cumulative Source0+1 will export 38. Hold
complete passes constant across consolidation points, not a partial cycle that
underexposes newly appended jobs. The initial 48-step candidate is two passes;
its later cumulative counterpart is 76 steps. If the purposeful alternative is
96 steps/four passes, its later counterpart is 152 steps. This clarification is
made while the base0 behavioral check is running, before any training result or
fresh outcome. Record both actual counts in the frozen selection. Every update
still starts from base with a fresh optimizer; native cyclic order remains.

## Failed first recipe and purposeful optimization alternative

The native 48-step, 0.0005 recipe fails the first source replay q2 with repeated
SQL fragments, invalid JSON and a missing join. Q3 is investigator-terminated
during the same pathological pattern; its partial event costs remain included.
Stop remaining checks for this failed candidate; do not claim a full 18-job score.
The console prints every eight steps, coinciding with finish examples, so those
small losses obscure higher query-target losses. Inspect all token-target losses
and gradient norms (optimization-diagnosis.json), not console snapshots alone.

The single purposeful alternative is 96 updates at 0.0001, four full passes, with
identical data, target masking, AdamW, LoRA, seed and execution interface. An owned
copy of the pinned trainer changes only learning-rate configuration and records
its hash; the dependency checkout is unchanged. This tests a gentler optimization
recipe, not an isolated learning-rate effect. If selected, later cumulative
training is 152 updates at 0.0001 (four passes). Both restart from base. No fresh
evaluation has begun. If this still fails, diagnose using source/development
evidence and label any fresh comparison as failed-acquisition feasibility.

## Bounded explanatory continuation, fixed before fresh outcomes

After completing the primary chronological comparison, run a source-only
optimization/context diagnostic on first source q2 and last source q21. For base,
failed 48-step and selected 96-step models, compare final teacher-forced query
loss and first-action generation with the exact recorded source prompt versus
the deployed prompt (history metadata says twelve sources instead of zero).
Use identical targets and unchanged model/tool interface, at most twelve
generations total. This can distinguish final forgetting/optimization failure
from sensitivity to changing inherited-history metadata; it does not isolate
individual optimization hyperparameters or measure complete-task performance.
It is chosen now, before fresh outcomes, does not change candidate selection,
and incurs its own forward/generation costs. The uncertainty matters because
low online training loss failed to predict actual source behavior. Independent
histories remain a separate, larger follow-up, not a claim made by this probe.

## Retention audit repair and interpretation before fresh evaluation

The lower-rate candidate completes 9/12 source and 1/6 development jobs against
10/12 and 1/6 for base0. It learns direct submit/finish behavior, but does NOT meet
the declared accuracy acquisition criterion. Do not interpret a subsequent null
as evidence that useful weight acquisition cannot transfer. Retain the stable
96-step candidate for a bounded failed-acquisition/efficiency comparison; no
promotion or further recipe search is justified by these results.

A source-retention audit finds q11's final successful query is literal arithmetic
after two useful component count queries. Final-only history omitted those
executable components. Repair both arms by retaining every successfully executed
source SQL component (deduplicated, explicitly ungraded), with original observed
outputs and direct run_saved IDs. Keep teacher records byte-identical; do not
rewrite training targets post hoc. Search exposes component IDs; read_source and
run_saved retrieve/execute them. No new model action format or system prompt is
introduced. Recheck both arms with this complete retained code before fresh work.
Old states, checks, failed traces and literal-arithmetic teaching targets remain.
Source1 uses the repaired collector with the same fixed base and block history.

## Actual diagnostic and continuation disposition

Before any fresh task was opened, the source-only context diagnostic was moved
forward and refocused to q2 and q6 (one successful and one failed source), keeping
the twelve-generation bound. The same q6 group error persisted with the exact
recorded source prompt. Protocol 04 then tested one computational source-program
repair. db-05's decision and all failed acquisition evidence remain preserved;
its proposed fresh comparison was superseded before execution. The actual final
comparison is db-06 under protocol 04, with a separately frozen decision.
