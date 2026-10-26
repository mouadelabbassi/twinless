# Architecture decision record 001 — Scientific kernel first

**Initiated during event:** 2026-10-26, Meta Global AI Developer Hackathon.
**Track:** Indie Developer. **Theme:** Push the Frontier.

## Research question
Can a tool-using AI investigator detect a discrepancy between an assumed
physical model and observed behavior, design informative non-invasive tests,
repair the world model under uncertainty, and produce externally validated
recovery recommendations? We have **not yet answered this question**.

## Implemented now (Day 1)
- Toy steady-state resistive DC network (4 buses, ideal 12-V source).
- Unknown redundant power connection hidden from the hypothesis evaluator.
- Candidate models: documented graph, undocumented bypass, fixed sensor bias.
- Contradiction detection from simulated sensor voltage.
- Deterministic probe selection based on posterior-weighted predictive variance
  divided by relative probe cost (not exact Bayesian mutual information).
- Gaussian model scores, posterior update, machine-readable evidence artifact.
- Deterministic pytest checks / GitHub CI workflow.

## Still NOT implemented
- Muse Spark orchestration, structured decisions or API calls.
- Bayesian structural search on arbitrary networks.
- Calibrated noise study, held-out topology benchmark, ablation against baselines.
- Robust intervention optimization and independent recovery verifier.
- Real-world hardware, validated AC power flow, safety certification.
- Product UI or final 3-minute video.

## Core module boundaries
`physics.py` computes electrical observations without LLM involvement.
`world.py` holds evaluation-only ground truth; scientific agents should receive
measurements only. `inference.py` defines a transparent non-LLM baseline.
`experiment.py` defines permitted simulated probes; no physical hardware writes.
`mission.py` produces an inspectable structured experimental record.

## Evidence policy
Report observed performance only. Never infer real-world safety from the toy
model. Keep project chronology in commits and disclose any external datasets,
third-party models, reused assets or pre-existing work. This prototype is
newly authored for the October 26–November 4 event and does not incorporate
older GreenTech code.
