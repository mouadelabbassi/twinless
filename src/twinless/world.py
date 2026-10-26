"""Simulated observations. Ground truth is private to this harness, not to the agent."""

from dataclasses import dataclass, field
import random
from .physics import FeederModel, OperatingPoint


@dataclass
class HiddenWorld:
    _truth: FeederModel = field(repr=False)
    noise_std: float = 0.0
    seed: int = 7
    _rng: random.Random = field(init=False, repr=False)

    def __post_init__(self):
        if self.noise_std < 0:
            raise ValueError("noise_std must be non-negative")
        self._rng = random.Random(self.seed)

    def measure_pump_voltage(self, point: OperatingPoint) -> float:
        exact = self._truth.voltages(point)["pump"]
        return exact + self._rng.gauss(0, self.noise_std)
