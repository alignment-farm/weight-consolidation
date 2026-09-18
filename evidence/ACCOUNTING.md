# Cost boundary

`costs.json` aggregates all published model workers across preserved pilots and
confirmation, including failed tasks/calls and the early evidence-access defect.
Remote smoke is separate because it used another model and backend. Its serving
token counts and reported backend timing are saved; network end-to-end time is
unknown. Native units are not converted into FLOPs, money or a shared compute unit.

Only pilot-02 actually trained. Confirmation copies that candidate and source data;
its manifests preserve historical training metadata, not a second training charge.
Eight investigator-authored reference trajectories (sixteen executed actions) are
shared source teaching work. They are not automatically collected successes and
are not free teacher labor. Authoring tokens/labor and reference-execution timing
are unknown. Pure tool validation checks are recorded but their aggregate timing
was not measured. Download progress recorded about 244 seconds; setup and hashing
are not covered by that number. The model manifest's historical download timing
comes from upstream and must not be counted as a local measurement.

All smoke, baseline collection, candidate checks, compiler-harness development,
access-parity rechecks and reset work are experimental search/acquisition/checking.
The final confirmation's twelve tasks per arm are the declared use horizon.
Comparisons are counterfactual branches sharing one history, not a single deployed
agent performing 48 distinct user jobs. Training and candidate checking are
incremental when considering deployment of the learned branch. Both branches pay
for authored source examples and retained code. Compiler engineering/checking is
additional shared external-reuse development with unmetered authoring effort.

Worker wall time includes model loading, hashing, instrumentation and tools.
Model/tool time is inside worker time, not added again. Controller time includes
worker startup/collection. Training update time is inside total training time.
Direct compiler timing covers an in-process function call only, excluding imports
and engineering/checking. It is not a controlled latency comparison with a fresh
model worker. No hardware-exclusive timing benchmark, energy or total-dollar
claim is made.
