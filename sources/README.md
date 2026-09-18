# Starting sources

Prepared 17 September 2026. These sources motivate the comparison; their reported
outcomes have not been reproduced by this study. The root inspected selected
methods, not complete implementations. Follow the closest methods as the workload
and learning recipe become concrete.

- [AgentOdyssey, 2606.24893v1](https://arxiv.org/html/2606.24893v1), §4, §6 and
  Appendix 10: LoRA updates and external memory in continuing text games. This
  already answers the broad possibility of useful combined learning. Our question
  adds competent retained examples/code, comparable evidence access, changed
  requirements and acquisition-cost accounting.
- [AgentCL, 2606.02461v1](https://arxiv.org/html/2606.02461v1), §§3.1–3.3:
  controlled task relationships distinguish reuse, repetition and generalization.
  Its non-parametric memory construction excludes ground-truth guidance; a local
  corrected-trajectory recipe has a different feedback boundary to disclose.
- [Co-Evolving Harnesses and Models, 2609.09134v1](https://arxiv.org/html/2609.09134v1),
  §3.4 and Appendix B: a possible correction-based acquisition method that retains
  the learner's surrounding trajectory. Generic harness/model composition is
  already studied. Teacher work and selection are paid acquisition, and this
  recipe is a lead rather than a required treatment.

Relevant local publications:

- [Evidence use under revision](https://github.com/alignment-farm/evidence-use-under-revision/blob/da1233fdfb26fe6c5daa337a3dbf9f784f34f9f7/FINDINGS.md):
  bounded adapter transfer through changed values, with qualified cost evidence
  and regression after further training. It does not establish a general hybrid
  advantage over competent retained code and examples.
- [Executable experience retention](https://github.com/alignment-farm/executable-experience-retention/blob/baf4d764cb4e571551a2b69d45751bb7f3281eaf/REPORT.md):
  available implementation and retention after reconstruction avoid repeated
  generation. Preserve those alternatives when judging added learning value.
- [State and revision support](https://github.com/alignment-farm/procedure-retention-and-revision/blob/3e71eb5f146e6493c60cef26d15d86dedd2249fb/FINDINGS-STATE-SUPPORT.md):
  inherited learning history affects which support preserves behavior. Present
  accuracy alone is insufficient to characterize maintenance.

The root selection and reading ledger were inspected during preparation at
`../../construct-2/notes/WEIGHT_CONSOLIDATION.md` and
`../../construct-2/sources/2026-09-17-runtime-study-selection/README.md` in the lab
layout. They contained uncommitted root work; the root Git HEAD alone does not
identify them. [preparation.json](preparation.json) records content hashes and
the runtime pin. This README and the study brief are self-contained starting
instructions; a remote clone does not require those sibling paths to exist.

## Local execution follow-through

The study inspected the pinned methods and cached one arXiv API query before
workload execution. See [inspection and reuse boundaries](INSPECTION-01.md),
[metadata](metadata.xml), and [local findings](../FINDINGS.md). No public paper
results were reproduced, and no paper code or data were incorporated into the
synthetic workload. Runtime source remained at the preparation pin without edits.

## Continuing-work discovery leads — 18 September

These support [the follow-up](../CONTINUING_WORK.md). Root inspected project
overviews and README documentation on 18 September; no benchmark implementation
or experiment was reproduced and no dataset has been selected. Inspect actual
tasks and relevant methods, then record exact paper and code/data versions before
reuse. These leads narrow workload discovery; they do not establish feasibility
with our models or answer the marginal value of weights.

- [BIRD-INTERACT](https://github.com/bird-bench/BIRD-Interact): database work with
  documentation, clarification, state-changing operations and executable checks.
  Its data schema identifies deliberately injected ambiguities. It offers an
  interaction/evaluation design to inspect, not an existing longitudinal
  consolidation comparison. Check availability of the required evaluation assets.
- [Continual Learning Bench](https://github.com/pgasawa/continual-learning-bench):
  constructed task instances in shared environments, multi-episode schedules,
  feedback and comparison with stateless operation. Inspect individual tasks
  for meaningful reuse and affordable model capability; existing continual
  evaluation narrows what a new local experiment would contribute.
- [STATE-Bench](https://github.com/microsoft/STATE-Bench): enterprise tool
  workflows, task-local sandbox databases, simulated users and a learning track.
  Its README discloses LLM-generated datasets. Inspect scoring and the learning
  interface before assuming that it supports our matched-history weight comparison.

For changing execution interfaces, root also inspected selected methods in
[HarnessForge, 2606.01779v1](https://arxiv.org/html/2606.01779v1), §§3.4, 4.3–4.4,
limitations and Appendix G.1: harness-specific alignment and crossed policy/harness
evaluation. Those methods and the earlier P42 correction method narrow a possible
compatibility diagnosis. Public results remain author-reported and do not explain
the prior local malformed actions by themselves. Generic co-evolution already
has concrete precedents.
