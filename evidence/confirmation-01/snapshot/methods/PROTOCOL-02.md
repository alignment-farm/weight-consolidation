# Protocol 02 — repair full-source access parity

Declared during the frozen pilot-02 evaluation, before confirmation payloads exist.
The audit found that both model arms received four compact source configs, while
adapter training used eight full source reference trajectories. Those full traces
were not exposed by a model-callable tool. Identical inference contexts alone do
not establish comparable access to the acquisition evidence. Preserve the entire
pilot-02 run as exploratory, including adverse outcomes; do not present its
comparison as the requested full-history-access test.

Correct this by exposing every exact source training row (messages and target) via
read_source(source_id), one source job per read to keep context bounded. Both arms
retain all eight files, the same compact source configs, code, current contract,
manual fallback and public errors. New prompts name the source index source-0
through source-7 and give the identical read_source action. No evaluator-only
fields or development/evaluation examples enter these files. This adds access;
no working code or ordinary tool is removed. Access and actual use stay distinct.

Use the already selected 32-step adapter, without retraining or reselection. This
is a fixed candidate, not optimization on pilot fresh outcomes. Acquisition was
7/8 versus 5/8 under the old prompt; recheck the eight source and four development
jobs under the repaired manual harness for BOTH arms and the four development
jobs under the repaired compiler harness for BOTH arms. No further prompt/recipe
changes in this phase, regardless of results. Training used the older prompt;
report this interface mismatch and the rechecked acquisition gate explicitly.

Then generate twelve new confirmation jobs using seed 2801+i, IDs confirmation-i,
with the same predeclared configuration schedule, six original and six revised.
No previous evaluation payload or label is used to generate training or select
these configurations. First four repeat dev configurations, next two and revised
six are absent from source/dev. Evaluate all four frozen conditions (manual base,
manual adapter, compiler base, compiler adapter), alternate order, one worker at a
time. Same six-turn and 256-token-per-turn limits. Direct compiler reference and
one base reset. Use exact complete outcomes and component grades. Treat confirmation
as a single correlated synthetic history, not an independent-history significance
test. Do not continue tuning after confirmation results.

Expansion: 32 recheck executions, 48 confirmation executions, one reset. All prior
work is paid experimental search; costs of these checks are charged separately.
No additional training or model download. Expected memory remains below 16 GiB;
worker execution remains serial. Record source file hashes and prove every training
row is externally reachable in both states. Publication closes on explanation or
this workload's demonstrated limit, not a general negative statement about LoRA.
