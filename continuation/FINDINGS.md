# Continuing database work with retained source programs

18 September 2026. Bounded follow-up to the unchanged [17 September result](../FINDINGS.md).
**No adapter is promoted.** In one constructed database history, the selected
adapter strategy completed 6/20 fresh jobs correctly, versus 7/20 with fixed
weights and the same external experience. Correct report artifacts, including
unfinished executions, were 6/20 versus 9/20. Training made familiar source jobs
shorter, but neither fresh accuracy nor the cumulative update improved. This is
limited feasibility, not a general result against weight consolidation.

## Workload and comparison

[Discovery](sources/DISCOVERY.md) inspected complete repository-maintenance jobs
(Tablib and Tenacity), database exploration and migration, BIRD interaction, and
retail state-changing jobs. The selected CL-Bench database has AmazonReviews-derived
content with authored obfuscated schemas, questions and a migration. It is not
an observed enterprise work stream, and its three product groups are not three
independent histories. Code, data, papers and licensing qualifications are pinned
in discovery and [resource provenance](resources/PROVENANCE.md). This study adapts
that environment; it does not reproduce a published leaderboard result.

Workers answer full SQL reporting questions using read-only SQLite, normalized
views, documentation, schema inspection, retained queries, saved executable
components, lexical history search and exact source training records. A report
must contain the complete correct rows and the worker must finish within eight
actions to count as a complete task. We also report artifact correctness because
a correct report can exist when the model fails to finish. Oracle queries execute
separately in the controller. Workers never receive oracle SQL or fresh labels.
The controller parses the question bank: this is an audited data-flow boundary,
not a byte-blind controller or adversarial operating-system sandbox.

Twelve source jobs and six development jobs precede ten fresh probes. Seven new
source jobs and four development jobs follow a database change, then ten more
fresh probes. The migration changes price storage, office record status, music
attribute storage, verification labels and review dates. Shared normalized views
handle physical mapping changes. Two previously learned, still-valid office-price
and review-date obligations are tested separately after the change; these are
source retention checks, not fresh generalization. Exact IDs and chronology are
in [protocol 04](methods/PROTOCOL-04.md) and the [frozen decision](evidence/db-06/decision.json).

Source collection uses the fixed base model. Earlier fresh results are not
inherited into later source collection or training. Both arms inherit identical
source histories, successful intermediate SQL, named saved queries, investigator
corrections, documentation and tools. Selected training examples are checked
submit/finish teacher trajectories, not raw autonomous successful traces. At the
second point both arms can read all 38 training records, the 19 source programs,
11 additional saved-query aliases and 38 retained executed components. The stale
adapter also gets the current external history and helpers. Search returns three
lexically ranked entries; this is a functioning reuse baseline, not a claim of
optimal retrieval.

The instrument is pinned native MLX Qwen3-4B-Instruct-2507 4-bit with rank-8 Q/V
LoRA in the last eight layers. Fresh workers verify base/tokenizer/adapter and
SQLite identities. The selected updates use learning rate 0.0001 and six complete
passes: 144 updates on 24 actions, then 228 on 38 cumulative actions. **Each starts
from base with fresh AdamW**, not optimizer continuation. The recipe, partitions
and preserved obligations were fixed before the first fresh evaluation.

## Acquisition and purposeful diagnosis

All earlier experiments remain in `evidence/db-01` through `db-05`:

- Initial environment checks exposed date conversion and future-documentation
  problems; repaired runs are separate. An eight-action allowance addressed a
  development case that produced the answer without finishing. The resulting 4B
  development baseline completed 2/6 jobs. A pinned 7B coder trial completed 1/6
  and was rejected before adapter training.
- The first actual source collector completed 7/12. Five source answers needed
  authored corrections using eligible source truth. A 48-update native-rate recipe
  produced repeated SQL and invalid actions. One check failed and a second was
  interrupted for futility; the other checks were not run. It is not a 0/18 result.
- Lower-rate, 96-update training reduced instability but did not improve source
  or development accuracy. An audit added previously omitted intermediate queries
  to both arms and repeated the affected checks. With full retained components,
  source scores were 9/12 base versus 8/12 adapter; development was 2/6 versus 1/6.
- Twelve source-only first-action probes compared exact training prompts with
  deployment prompts. One critical wrong-table identifier persisted in both
  contexts despite low teacher-forced loss. Another query was correct in both;
  the earlier high-rate adapter remained malformed even on the exact prompt.
  These probes argue against history-count context mismatch as the principal
  cause in those two cases. Mean loss hid consequential token errors.

The useful bounded continuation was to replace fragile/literal source answers
with complete computational SQL in the already available normalized views, while
retaining original code and teacher records externally. This tested whether better
source teaching could establish useful acquisition before interpreting transfer.
It reused the actual twelve collector traces, added twelve checked teacher
replays, and used the fixed six-pass recipe. Both conditions then completed all
12 source jobs; model calls fell from **87 to 24** with the adapter. Development
remained 2/6 in each condition, with different successes. This establishes shorter
successful source execution, not an accuracy gain or a necessary cost of external
reuse: a stored correct source query can also be executed directly without a model.
Recipe changes bundle learning rate, passes and source representation, so their
individual causal effects are not identified.

Later collection completed 4/7 jobs (5/7 correct artifacts). One canonical source
query, q109, exceeded the 20-second SQL budget. Its failed replay is preserved;
an equivalent source-only set-difference query was validated before training.
Previously validated replays were reused. No fresh outcome selected this repair
or changed the fixed update. Later source checks scored 5/7 base versus 6/7 updated
adapter, while development scored 1/4 versus 0/4.

## Fresh and preserved outcomes

| Period / condition | Correct report | Correct report and finish | Model calls |
|---|---:|---:|---:|
| Before change, external reuse | 6/10 | 4/10 | 71 |
| Before change, adapter 144 | 4/10 | 4/10 | 33 |
| After change, external reuse | 3/10 | 3/10 | 73 |
| After change, stale adapter 144 | 3/10 | 3/10 | 40 |
| After change, cumulative adapter 228 | 2/10 | 2/10 | 42 |
| Preserved source obligations, external reuse | 2/2 | 2/2 | 14 |
| Preserved source obligations, stale adapter | 2/2 | 2/2 | 4 |
| Preserved source obligations, cumulative adapter | 2/2 | 2/2 | 4 |

Before the change, the base completed q19/q25/q29/q30; the adapter completed
q25/q26/q29/q30. Afterward the base completed q114/q115/q118, the stale adapter
q112/q114/q115, and the updated adapter q114/q115. The cumulative update therefore
lost one stale-adapter success without gaining another. Small, dependent samples
from one history do not support population-level significance claims.

Recorded behavior explains a tradeoff. Every fresh adapter condition made zero
history searches or saved-query executions; the base made 20 history searches and
13 saved-query executions across its two fresh blocks. The learned policy mostly
attempted direct submit/finish actions. It used fewer calls but could produce
wrong SQL or malformed actions. Equal source access did not yield equal retrieval
or context exposure. This description is post-evaluation analysis, not a newly
selected treatment or claim tested on those same outcomes.

## Incurred work and interpretation

The [machine-readable ledger](evidence/summary.json) includes **229 task executions**
(including one interrupted check), **12 additional first-action probes**, **31
successful teacher replays**, and **four training runs / 516 updates**. Failed
recipes and exploratory environments are included. The successful training
processes include scientifically unsuccessful recipes; zero process failures does
not mean zero experimental failures.

| Native quantity | Recorded follow-up work |
|---|---:|
| Model task calls | 1,207 |
| Task prompt / completion tokens | 1,934,115 / 57,638 |
| Task model time | 2,498.61 s |
| Task controller elapsed, including nested model/tool work | 3,297.58 s |
| Task oracle checking | 98.64 s |
| Four training runs elapsed | 612.19 s |
| Training input / supervised loss tokens | 400,308 / 15,360 |
| Successful source teacher replay elapsed | 35.40 s |
| Auxiliary probe prompt / completion tokens | 8,256 / 1,830 |

Interrupted-task usage is a lower bound. Separately preserved are one failed
teacher SQL attempt (20-second execution budget, exact elapsed unknown), one
checker tuple/JSON-array comparison failure (one tool call, elapsed unknown), and
10 successful component-replay audit calls (2.34 s). The checker was corrected;
no worker reports or grades changed. Final audits recomputed 86 db-05 and 121
db-06 grades. Their full elapsed time was not instrumented and is not in the task
checking total. Database download took 67.52 s; the successful 7B download/hash
retry took 636.63 s, after a stalled download of unknown duration. These are
experimental search/setup costs, not per-deployment costs.

The selected 20-job strategy used 75 model calls, 72,554 prompt tokens, 5,151
completion tokens and 124.00 model seconds, versus external reuse's 144 calls,
287,824 prompt tokens, 4,905 completion tokens and 332.80 model seconds. Its two
training runs additionally took 438.17 seconds, apart from source teaching,
collection, checking and development. These timings are local measurements, not
a controlled latency benchmark or one interchangeable compute currency. The
adapter strategy has lower quality, so no quality-matched break-even is established.
Investigator/tool-development/teacher authoring time and tokens, upstream work,
energy and FLOPs remain unknown. No remote model inference was charged; endpoint
access alone did not demonstrate remote training or adapter capability.

WC1 receives no incremental fresh-completion support in this setting. WC2 shows
retention of two old obligations but no update advantage after change; shared
helpers already handle physical schema maintenance. WC3 has no demonstrated
quality-matched repayment over this horizon. All original WC1–WC3 wording and
previous phase evidence remain unchanged.

The [audit](evidence/db-06/audit.json) verifies state parity, exact accessible
training evidence, unchanged base weights, changed adapters, cumulative source
prefixes, actual recorded identities, recomputed report grades and decision timing.
[Reproduction commands](REPRODUCE.md) cover fixed-state replay and training.
This does not establish absence of public-task pretraining contamination.

This phase closes on an explanatory limitation after the bounded source-quality
continuation: the learner acquires short familiar SQL actions, while useful fresh
work still needs retrieval, tool use and reliable query composition that this
teaching recipe did not establish. Base fresh performance is also low. An
independently sourced maintenance history and training on successful retrieval/
execution trajectories could test a different capability, but would require new
source collection, development and a separately frozen comparison. Repeating
more steps on these now-observed probes would not resolve that uncertainty. The
broader research question remains open; publication acceptance is not the reason
for stopping this bounded phase.
