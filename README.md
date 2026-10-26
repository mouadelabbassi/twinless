# TWINLESS — Autonomous Reality Repair

> **Meta Global AI Developer Hackathon 2026** • Indie Developer • Push the Frontier
>
> **Status: Day 1 experimental physics + diagnostic baseline. Not a finished AI product.**

TWINLESS asks whether an autonomous investigator can detect when its internal
model of a physical system is incorrect, design measurements that distinguish
competing explanations, revise its assumptions, and propose *verifiable*
interventions rather than guess.

**Target domain:** incompletely documented microgrids. This repository is an
original event-window prototype, not a continuation of any older project code.

## What runs today

A transparent Python prototype creates a tiny, simulated 12-V resistive DC
feeder with a hidden bypass connection. A baseline investigator receives a
pump-voltage observation, detects disagreement with the documented topology,
tracks three hypotheses, selects an informative perturbation, and revises its
hypothesis scores using another measurement. Output is structured JSON.

This stage has **no Meta Model API calls yet**. The core is intentionally a
non-LLM baseline so later Meta-powered agents can be evaluated against it.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -e ".[dev]"
python -m twinless --seed 7
pytest -q
```

## Research hypotheses (unproven)

1. Adaptively probing physical systems reduces uncertainty about incorrect
   structural models compared with passive measurements.
2. Meta Muse Spark 1.3 can improve hypothesis / experiment selection relative
   to this transparent deterministic baseline in held-out scenarios.
3. Validated model repair can produce safer or more useful simulated recovery
   suggestions than trusting the original model uncritically.

None of these hypotheses have been demonstrated across independent test sets.

## Roadmap

- [x] Event-native, reproducible research kernel and tested toy fixture
- [ ] Meta Spark tool-using investigator (official API)
- [ ] Parameterized hidden topologies and noisy sensors
- [ ] Held-out benchmark + fixed-policy and non-LLM ablations
- [ ] Robust recovery planning + independent verifier
- [ ] User-facing interactive experiment application
- [ ] <=3-minute working product demo, public deployment, submission

## Repository structure

```text
src/twinless/      transparent physics, hidden-world harness, inference, probes
 tests/             automated regression tests
 docs/              architecture and competition compliance
 .github/workflows/ GitHub Actions tests
```

## Research limitations

This is a toy steady-state **DC resistive circuit**; it is *not* a validated AC
microgrid simulation and is *not safe to connect to real infrastructure*.
The single illustration is deliberately designed to distinguish a topology
change from a plausible fixed sensor bias. Its success is NOT a benchmark.
Results are reproducible locally but do not establish generalization,
autonomous model repair, production readiness, or improved reliability yet.

## Competition provenance

All project-specific source files in this initial scaffold were newly authored
after the October 26, 2026 kickoff. Third-party package dependencies retain
their own licenses. See [compliance notes](docs/HACKATHON_COMPLIANCE.md).
No old GreenTech code, external confidential telemetry, or unauthorized assets
are included. The commit history will document subsequent iterations.

## Meta Model API (next engineering milestone)

Official documentation: https://dev.meta.ai/docs/quickstart

- Base URL: `https://api.meta.ai/v1`
- Recommended starting model: `muse-spark-1.3`
- Put your token in the `MODEL_API_KEY` environment variable, **never GitHub**.

## License

No public code-reuse license has been selected yet. A PUBLIC repository is not
the same thing as granting a license. The owner should select a license only
after reviewing organizer requirements and their commercialization plans.
