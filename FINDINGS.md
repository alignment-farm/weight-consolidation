# Reconciliation pilot: what adapter learning adds to retained code

17 September 2026. **Bounded phase complete; broader question remains open.**

On twelve new synthetic reconciliation jobs with full source evidence available
to both conditions, an adapter improves manual configuration of retained code
from **3/12 to 5/12** complete tasks. A developed explicit contract compiler makes
both conditions **12/12**, including all six changed-contract tasks. The adapted
model incurs twelve additional malformed-action repairs in this stronger harness.
Direct compiler execution also completes 12/12 without model calls. For this
bounded contract language, explicit reuse removes the observed quality headroom;
the adapter adds training/checking and use-time work without improving completion.
This is a workload limitation, not a general result against adapter learning.

The experiment includes successful but partial source acquisition, prompt and
harness diagnosis, and a corrected evidence-access flaw. All **172 model task
executions**, the sole training run, failed calls and authored teaching remain
preserved. [Final audit](evidence/confirmation-01/audit.json),
[full cost ledger](evidence/costs.json), [reproduction](REPRODUCE.md).

## Corrected confirmation results

| Full-source-access condition | Original contracts | Revised contracts | Complete total |
| --- | ---: | ---: | ---: |
| Retained transformation, model configures it | 2/6 | 1/6 | 3/12 |
| Same + fixed 32-step adapter | 3/6 | 2/6 | 5/12 |
| Retained compiler + transformation | 6/6 | 6/6 | 12/12 |
| Same compiler route + same adapter | 6/6 | 6/6 | 12/12 |
| Direct compiler + transformation, no model | 6/6 | 6/6 | 12/12 |

The twelve confirmation payloads were generated after the fixed decision and
rechecks. No final result triggered another prompt, candidate or training change.
Both learned and unlearned manual routes preserve the unknown-account quarantine
and always-excluded void row on all six revised tasks. However, the adapter's
complete exclusion list is right on only 2/6 revised tasks versus the base's 6/6:
it keeps accepting only the old posted status in four cases. Better complete-task
counts therefore do not imply uniformly better revision handling. Both compiler
conditions satisfy every checked obligation on every task. See
[preserved obligations](evidence/confirmation-01/preserved-obligations.json).

All arms receive the compact references automatically; none requests a full source
record in confirmation. Availability is verified separately: every exact training
row and collector history can be read by both arms. The comparison measures
weights with equal available source evidence, not identical lifetime exposure.

With compiler reuse, base uses **24 model calls, 24,329 input tokens, 164 generated
tokens and zero tool errors**. Adapter uses **36 calls, 38,025 input tokens,
842 generated tokens and twelve tool errors**. Each adapted job first emits a
malformed configuration/contract-call combination, then recovers with run_contract
and finish. This is consistent with interference from the old action format;
it does not isolate the training-prompt mismatch from other causes. Both retain
all manual fallback and source-reading tools. [Action diagnosis](evidence/confirmation-01/diagnosis.json).

## Method

[Protocol](methods/PROTOCOL-01.md), [reproduction](REPRODUCE.md),
[instrument provenance](resources/PROVENANCE.md),
[methods inspection](sources/INSPECTION-01.md).

One synthetic invoice-reconciliation history contains eight source jobs, four
development jobs and twelve fresh row sets. The model interprets column mappings,
units, credit signs, revision precedence and accepted statuses. A retained program
handles joining, deduplication and arithmetic. Complete success requires the right
records, sum, exclusions, quarantine, job identity and successful finish. Six fresh
jobs revise status eligibility, revision precedence and credit-sign rules while
retaining account/quarantine and other exclusion obligations.

Fresh means unseen payloads and amounts. Four evaluation jobs repeat development
configuration combinations; two original-policy jobs and six revised jobs use
configurations absent from both source and development. These are correlated
fixtures in a narrow generated language, not independent real-world histories.
See [configuration overlap](evidence/confirmation-01/evaluation-overlap.json). The controller-only
oracle uses canonical integer facts separately from the transformation code.

Both arms inherit identical authored code and four source configuration examples,
automatically included and also retrievable. Eight source attempts are recorded;
eight separately executed investigator-authored reference trajectories provide
sixteen training actions. These are explicit teaching, not autonomous successful
traces. No separate teacher model calls occurred; authoring-agent work is unmetered.
Source feedback is eligible for learning. Development results select the recipe;
fresh evaluation never enters training, context, tool feedback or selection.

The pinned Qwen3-4B 4-bit model receives 32 rank-eight Q/V LoRA updates under the
unchanged runtime. Each job loads verified base/tokenizer and optional adapter in
a fresh process and workspace. Training starts from base with a fresh optimizer.
The exact [adapter manifest](evidence/pilot-02/adapter-32/manifest.json) records
changed adapter tensors, unchanged base tensors and load checks.

## Development and diagnosis

The [first smoke](evidence/pilot-01/) copied a schema placeholder and repeatedly
used an invalid finish argument. The improved prompt clarified both before any
training. Those failed costs and original files remain preserved.

With manual configuration of retained code, the base completes 5/8 source jobs
and 1/4 development jobs. The adapter completes 7/8 source jobs and 1/4 development
jobs, with different development successes. This meets the protocol's narrow
source-acquisition gate but does not establish robust generalization. A source
failure degenerates into invalid JSON; a development failure repeatedly finishes
after an arithmetic-validation error. Other failures use stale units or credit
settings. Loss reduction alone would conceal these failures.

The finite contract language permits a small explicit compiler. It reads the
public contract without fixtures or expected outputs. Both conditions receive it
at the same point, retain manual fallback, and undergo development checks. Under
the first compiler prompt, base completes 1/4 and adapter 4/4 development jobs:
the base sometimes overwrites correct compiler output with stale source settings.
Clarifying “compile first; finish on success; manual fallback on error” raises the
base to 4/4 while the adapter remains 4/4. Both prompt versions and all checks are
preserved. This is a joint workflow-guidance intervention, not a tool-permission-only
comparison. No compiler-harness retraining occurs; the same adapter is tested.

Recipe selection was frozen before compiler checks. The final harness and planned
four-arm comparison were frozen before fresh payload generation. See
[decision](evidence/pilot-02/decision.json) and
[evaluation freeze](evidence/pilot-02/evaluation-freeze.json).

## Evidence parity correction

An audit during pilot-02 evaluation found a material limitation: its `experience`
tool exposed four compact configurations, while training consumed full trajectories
for eight source jobs. The exact source training rows were not externally readable.
Equal inference context did not establish equal evidence access. Pilot-02 is
therefore **exploratory**, not the requested full-access causal comparison. This
was found before the confirmation set was generated. All 91 pilot executions,
including this flawed comparison, remain in the record and cost ledger.

[Protocol 02](methods/PROTOCOL-02.md) adds indexed access to every exact training
row and the source collector histories for both conditions, preserving all prior
tools. It uses the same already selected adapter without further optimization or
selection. Thirty-two source/development rechecks precede 48 executions on twelve
new confirmation payloads, followed by a base reset. Source-access checks execute
the public read tool and compare the returned records against all sixteen training
rows in every arm. This also exposes a prompt mismatch with the original training
contexts; the rechecks, rather than the old source scores, determine whether
acquisition remains evident under the corrected interface.


Under the repaired interface, source completion is **6/8 base versus 7/8 adapter**;
manual-code development completion is **1/4 versus 2/4**. Both compiler-assisted
conditions complete **4/4** development jobs. Thus the fixed treatment still meets
the narrow source-acquisition gate after restoring evidence parity, while the
stronger explicit route leaves no development quality headroom. No training or
selection was repeated. See [confirmation freeze](evidence/confirmation-01/evaluation-freeze.json).

Pilot-02's exploratory fresh outcomes, retained for completeness:

| External arrangement | Base | Same arrangement + adapter |
| --- | ---: | ---: |
| Manual configuration of retained transformation | 3/12 | 4/12 |
| Retained compiler and transformation, clarified workflow | 12/12 | 12/12 |

These numbers are not substituted for the corrected confirmation. They motivated
no candidate change; the evidence-access defect, rather than a poor score,
triggered the confirmation protocol.

## Scope of the result

This is a bounded, authored-language workload. The retained compiler is ordinary
explicit engineering and solves the declared contract grammar; it is not a learned
controller and is not evidence that arbitrary business prose can be parsed safely
with these rules. The compiler and transformation are a stronger alternative than
repeated neural interpretation of the same supported clauses. Developing that
alternative is part of the study, not a forbidden shortcut.

One source history, one model, one training seed, twelve correlated confirmation
jobs and a known finite contract language limit transfer claims. No later source
history, repeated consolidation cycle, amortization horizon beyond these jobs or
real customer exports were evaluated. The adapter's training prompt predates the
compiler and full-source tools. All conditions within each comparison have the
same current tools/context policy, but this experiment does not optimize a new
adapter for each harness. No source-access claim is inferred from whether a model
actually chooses to retrieve a record.

WC1–WC3 remain verbatim in README; their assessments below concern this setting
only. A publication milestone does not resolve the broader question of where
experience should live in an agent working on less structured tasks.


## Incurred work and interpretation

Across both pilots and corrected confirmation: **172 model task executions,
424 calls, 426,743 prompt tokens, 10,626 generated tokens, 84 tool-error calls,
and 930.69 summed worker seconds**. Model generation occupies 529.77 seconds
inside that worker time; it is not added again. Source collection, failed smoke,
flawed pilot comparison, development, parity checks and resets are included.
Remote feasibility used a separate 8B model for one call: 22 input and 10 output
tokens, outside the matched totals. Direct compiler evaluation performed 24 calls
across exploratory and corrected sets, separately recorded without model tokens.

The sole 32-update training run processed **30,750 input positions and 944 target
positions**, taking **45.51 update seconds / 50.10 total seconds**, with peak MLX
allocation **4.52 GiB**. Confirmation reused this adapter; copied manifests are
not additional training. Sixteen executed authored teaching actions, code/parser
engineering and checking must also be charged. Authoring-agent tokens/labor,
reference-execution time, total setup overhead, energy and FLOPs remain unknown.
The base weight file is 2.263 GB; snapshot retrieval took about 244 seconds.
[Accounting boundaries](evidence/ACCOUNTING.md) distinguish experimental search,
shared preparation and the twelve-job use horizon. These are not controlled
production latency or dollar-cost measurements.

In the stronger full-access condition, this adapter provides no quality gain over
the horizon, incurs more inference calls/tokens and adds measured training/checking.
There is no observed repayment in these units. Unmeasured engineering costs prevent
a complete monetary break-even calculation. Direct compiler success further shows
that a neural executor is unnecessary for this particular generated language.

**WC1:** narrow acquisition and a manual-route improvement were observed, but no
incremental complete-task benefit remains against the developed compiler route.
**WC2:** compiler reuse handles all revised jobs and preserved obligations. The
manual adapter improves overall completion slightly while worsening changed-status
exclusion accuracy; aggregate accuracy alone obscures that regression.
**WC3:** the learned branch adds paid acquisition and, in the stronger harness,
extra repair/use work without additional completed jobs over the measured horizon.

This phase closes on an explanatory limitation: the supported contract language
is cheaply executable, and apparent learning headroom depends on how competently
that external route is used. The broader retained-experience question remains
unresolved for richer contracts, genuinely independent histories, later source
collection and repeated consolidation. No candidate is promoted. The next study
would need substantive integration ambiguity beyond this finite language, while
retaining the compiler and other working code wherever applicable.
