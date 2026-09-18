# Methods inspection, 2026-09-17

Inspected exact HTML versions AgentOdyssey 2606.24893v1 §4 and Appendix 10,
AgentCL 2606.02461v1 §§3.1–3.3, and Co-Evolving Harnesses and Models
2609.09134v1 §§3.1–3.4. Metadata cached in metadata.xml from one arXiv API
query, descriptive User-Agent WeightConsolidationStudy/0.1; no parallel API/OAI
clients or repeated requests used. See arxiv-headers.txt. No paper code or data
copied; this is methods inspection, not reproduction of reported outcomes.

AgentOdyssey combines LoRA and external short-term experience; combined learning
is therefore not our novelty claim. Its rank16 Q/K/V/O training recipe differs
from the initial runtime rank8 Q/V recipe. AgentCL motivates explicit task
relationships and frozen held-out memory; its no-ground-truth memory construction
differs from our openly authored source supervision. Co-Evolving Harnesses and
Models motivates checking complete harness behavior after tuning. Its localized
on-policy correction is not the same as our full two-action authored references;
if planning deteriorates, inspect that difference before expanding search.

Runtime cloned at 9ffb10a66180626b80127fb1892b2cf71e39d946 into ignored .deps.
INVESTIGATOR.md, MILESTONE-2.md, model, learner, executor, experience and state
implementations inspected. No LICENSE file found in pinned runtime tree: local
use is explicitly commissioned; do not infer a general redistribution license.
Runtime source is not vendored into study publication. Preserve its hash manifest
and upstream pin. No upstream example/evaluator/data copied into our workload.
Model repository declares Apache-2.0; manifest pins quantization and tokenizer
files. MLX-LM source is pinned by runtime uv.lock. New workload and controller
code are investigator-authored in this session.
