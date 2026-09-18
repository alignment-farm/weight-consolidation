# Weight consolidation with retained experience

Prepared 17 September 2026 as an independent Construct-2 ancillary study.
**Status: bounded feasibility and confirmation complete (17 September 2026).**
[Findings and abstract](FINDINGS.md) · [Reproduction](REPRODUCE.md) ·
[Corrected confirmation audit](evidence/confirmation-01/audit.json) ·
[All incurred costs](evidence/costs.json).

With full source evidence accessible to both arms, adapter learning improves
manual use of retained transformation code from **3/12 to 5/12** complete fresh
tasks. A developed explicit contract compiler yields **12/12 with either model**,
including six changed-contract jobs. The adapter adds twelve malformed-action
repairs in that stronger harness. Direct compiler execution also scores 12/12.
This demonstrates a limit of the finite synthetic workload, not a general negative
result about weight consolidation. No adapter is promoted; the broader question
remains open.

The complete record preserves 172 model task executions, one 32-update training
run, all failed attempts, and an exploratory comparison corrected after a
source-access audit. [Protocol 01](methods/PROTOCOL-01.md) records acquisition and
harness development; [Protocol 02](methods/PROTOCOL-02.md) fixes full-source parity
before new confirmation payloads. Original WC1–WC3 below remain unchanged; see
[their assessments](FINDINGS.md#incurred-work-and-interpretation).

Read [AGENTS.md](AGENTS.md) for responsibilities and available resources.

## Question

Does periodically learning from accumulated task experience improve complete
future work beyond a competent agent that can already retrieve the same examples
and reuse the same acquired code? Does any benefit survive a change in requirements
and the cost of acquiring, checking and maintaining the adapter?

The broader program asks how agents accumulate useful experience across sessions
and where it should live. This study asks what weights add inside a system that
already preserves experience externally. It does not presume that external memory
should be replaced, that an adapter must win, or that a new learning controller is
needed. The investigator owns workload selection, methods, protocols, execution,
diagnosis and publication.

## Starting expectation

Begin with bounded workload and acquisition development. Establish a useful
external-reuse baseline, demonstrate what the learning treatment acquires on
development tasks, and estimate the resources for an identifying comparison.
Then proceed autonomously to fresh evaluation when feasible. Preparation itself
starts no agent, service or training run.

A concrete workload lead is recurring data integration: interpret source
contracts, combine exports and produce independently checked reconciled records.
Earlier jobs leave examples, mappings, corrections and reusable transformation
code. Later jobs combine familiar operations with new source contracts; an
authoritative requirement then changes while other obligations remain valid.
Use actual integration fixtures or a motivated, explicitly labeled analogue.
This is a starting lead, not a mandatory benchmark. Select a better job if it
provides a clearer consequential comparison.

Establish why prior experience helps, what transfers beyond copying an answer,
and where the agent still has useful work to do. Keep deterministic parsing and
arithmetic in competent tools. Do not manufacture headroom by hiding mappings,
requiring code regeneration, degrading retrieval or restricting ordinary feedback.
If a cheap explicit route resolves the setting, that is an informative limit.

## Starting comparison

At declared points in a chronological source history, fork identical available
experience and executable artifacts into:

- **External reuse:** fixed model weights with developed retrieval, retained
  examples and direct reuse of available code.
- **External reuse plus adapter:** the same environment, context policy, tools
  and retained material, adding an adapter trained from that history.

A current-task-only reference can establish the value of accumulated experience,
but is not the main opponent. Both principal conditions keep working code and
can retain a successful reconstruction. Skills are optional representations.
Record actual exposure and tool use: equal evidence access does not mean the
models retrieve identical context or choose identical actions.

Use fresh probes for familiar operations in new combinations, changed requirements
and preserved obligations. Keep their labels and outcomes out of subsequent
training and candidate selection. Collect later source experience separately
under a declared collector and feedback policy, with the same resulting evidence
available to both conditions. Identify executor traces, authored corrections and
teacher work separately. Shared histories isolate the added effect of weights;
they do not establish autonomous selection of future experiences.

Choose recipes and readiness criteria on development material before evaluating
the resulting claims on fresh material. Multiple independent task histories are
more informative than many paraphrases of one case. You own sample sizes,
workload generation, budgets and the exact protocol; this brief is not a fixed
experimental recipe.

Report complete outcomes and all acquisition, failed attempts, checking,
selection, repair and use costs over the declared horizon. Distinguish shared
source collection, incremental consolidation, experimental search and deployment
work. Keep quality and costs visible in their native units; unknown engineering
costs remain unknown. Lower loss, changed tensors and successful adapter loading
are insufficient evidence of acquired useful behavior.

## Prospective expectations — WC1–WC3

These are copied from the root's selection note before execution. Preserve their
wording and append subsequent assessments, including adverse results.

- **WC1:** Weight updates may improve reuse on fresh combinations of recurring
  operations even when source examples and code remain accessible. No incremental
  gain would favor retaining the simpler external arrangement for this setting.
- **WC2:** Learning stable behavior may survive changed current requirements;
  learning stale shortcuts may increase violations. Check complete revised tasks
  and preserved obligations, including cases where external reuse remains right.
- **WC3:** Better use-time performance need not repay acquisition and checking.
  Report cumulative complete outcomes and incurred work over the declared horizon,
  with costs in their native units and unknown engineering costs visible.

Diagnose failed acquisition within a bounded development effort before interpreting
a transfer null. Preserve failed attempts and test claims developed through
diagnosis on fresh material. Close on explanatory progress, a demonstrated
limitation or a concrete resource constraint. A failed first recipe alone is not
closure; neither is a positive adapter result required.

## Runtime instrument

The starting instrument is
[Construct Runtime at 9ffb10a66180626b80127fb1892b2cf71e39d946](https://github.com/alignment-farm/construct-runtime/tree/9ffb10a66180626b80127fb1892b2cf71e39d946).
Read its pinned [investigator interface](https://github.com/alignment-farm/construct-runtime/blob/9ffb10a66180626b80127fb1892b2cf71e39d946/docs/INVESTIGATOR.md)
and [Milestone 2](https://github.com/alignment-farm/construct-runtime/blob/9ffb10a66180626b80127fb1892b2cf71e39d946/reports/MILESTONE-2.md).
It provides external Python environments, named state forks, separate model/context/
tool controls, real MLX LoRA training/loading and relocatable evidence. Keep this
study's environment, evaluator, source collection, protocol and outputs here.

Use a pinned dependency or an owned checkout, rather than editing the derivative's
active checkout. The lab copy is at `../../derivatives/construct-runtime` from
this directory; inspect it read-only. One option for an owned checkout is:

```sh
mkdir -p .deps
gh repo clone alignment-farm/construct-runtime .deps/construct-runtime
git -C .deps/construct-runtime checkout --detach 9ffb10a66180626b80127fb1892b2cf71e39d946
```

Training currently starts from base, without warm-starting existing adapters or
restoring optimizer state. Rebuilding from cumulative experience is a valid first
comparison if its cost is charged and it is called periodic consolidation.
Verify sequence/update limits, model compatibility and resource needs against the
chosen workload. A justified local adaptation or alternative instrument is allowed;
pin its source and explain changes. The study need not wait for runtime development.

The runtime's examples are small development demonstrations, not ready scientific
controls for this question. Their adapters remain unpromoted, and the release-gate
example has a supplied complete program. Its working interface does not establish
new-workload acquisition or utility.

## Research basis and publication

Read [sources/README.md](sources/README.md) for exact public versions, prior local
findings and the preparation boundary. Combined memory and training, controlled
reuse streams, and harness/model interactions already have direct precedents.
Continue focused discovery as the workload clarifies; explain whether existing
work answers, narrows or redirects the question before expanding experiments.

Publish a concise abstract here, with links to local methods, failed and successful
evidence, cost accounting and reproduction instructions. Keep revisions identifiable.
Root synthesis is separate from local phase closure and the unresolved broader
question. No completed ancillary phase is reopened by this study.
