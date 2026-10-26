"""Transparent candidate-model likelihoods and one-step experiment selection.

This is a deterministic BASELINE, not an LLM/Meta agent. A future Muse Spark
agent must outperform or add value beyond this baseline in held-out tests.
"""

from dataclasses import dataclass
import math
from .physics import FeederModel, OperatingPoint
from .experiment import Probe


@dataclass(frozen=True)
class Candidate:
    name: str
    model: FeederModel
    pump_sensor_bias_volts: float = 0.0

    def predict(self, point: OperatingPoint) -> float:
        return self.model.voltages(point)["pump"] + self.pump_sensor_bias_volts


def build_candidates(start: OperatingPoint) -> tuple[Candidate, ...]:
    """A fixture with observationally ambiguous bypass vs. sensor offset.

    The sensor-bias candidate is calibrated from two proposed models at the
    INITIAL operating point, not from the hidden world's actual observation.
    Calibration is intentionally fixed during later probes. It represents a
    one-time fitted sensor-bias alternative to a structural topology change.
    """
    no_bypass = FeederModel(bypass_present=False)
    bypass = FeederModel(bypass_present=True)
    offset = bypass.voltages(start)["pump"] - no_bypass.voltages(start)["pump"]
    return (
        Candidate("documented_topology", no_bypass),
        Candidate("undocumented_bypass", bypass),
        Candidate("sensor_bias_only", no_bypass, pump_sensor_bias_volts=offset),
    )


def update_posterior(prior: dict[str, float], candidates: tuple[Candidate, ...],
                     point: OperatingPoint, observed: float, sigma: float = 0.06) -> dict[str, float]:
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    logs = {}
    for c in candidates:
        p = prior.get(c.name, 0.0)
        logs[c.name] = (math.log(p) if p > 0 else float("-inf")) - (
            (observed - c.predict(point)) / sigma
        ) ** 2 / 2
    max_log = max(logs.values())
    if not math.isfinite(max_log):
        raise ValueError("All candidate models have zero prior probability")
    weights = {name: math.exp(value - max_log) for name, value in logs.items()}
    total = sum(weights.values())
    return {name: value / total for name, value in weights.items()}


def choose_probe(candidates: tuple[Candidate, ...], posterior: dict[str, float],
                 initial: OperatingPoint, probes: tuple[Probe, ...]) -> Probe:
    """Pick a test with the greatest posterior-weighted predicted variance/cost.

    Surrogate information score, NOT exact expected Bayesian information gain.
    """
    if not probes:
        raise ValueError("No admissible probes supplied")
    scores: list[tuple[float, int, Probe]] = []
    for i, probe in enumerate(probes):
        point = probe.apply(initial)
        predictions = {c.name: c.predict(point) for c in candidates}
        mean = sum(posterior[c.name] * predictions[c.name] for c in candidates)
        variance = sum(posterior[c.name] * (predictions[c.name] - mean) ** 2 for c in candidates)
        scores.append((variance / probe.cost, -i, probe))
    return max(scores, key=lambda item: (item[0], item[1]))[2]
