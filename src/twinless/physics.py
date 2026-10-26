"""A toy resistive DC feeder, NOT a validated real-grid engineering solver.

Each load is a constant-current sink; a voltage source is treated as an ideal
slack bus. Solve KCL at non-slack buses using a conductance matrix. This
ignores real AC power flow, transients, protection logic and thermal limits.
"""

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Line:
    left: str
    right: str
    resistance_ohm: float

    def __post_init__(self):
        if self.left == self.right or self.resistance_ohm <= 0:
            raise ValueError("Lines must have distinct endpoints and positive resistance")


NODES = ("source", "hub", "clinic", "pump")
BASE_LINES = (
    Line("source", "hub", 0.4),
    Line("hub", "clinic", 0.55),
    Line("hub", "pump", 0.7),
)
BYPASS_LINE = Line("source", "pump", 0.6)


@dataclass(frozen=True)
class OperatingPoint:
    clinic_amps: float = 1.5
    pump_amps: float = 1.0

    def __post_init__(self):
        if self.clinic_amps < 0 or self.pump_amps < 0:
            raise ValueError("Load currents must be non-negative")


@dataclass(frozen=True)
class FeederModel:
    bypass_present: bool
    source_voltage: float = 12.0

    def voltages(self, point: OperatingPoint) -> dict[str, float]:
        """Compute idealized steady-state voltages from Kirchhoff's current law."""
        nodes = NODES[1:]
        indices = {name: i for i, name in enumerate(nodes)}
        matrix = np.zeros((len(nodes), len(nodes)), dtype=float)
        rhs = np.zeros(len(nodes), dtype=float)
        for line in BASE_LINES + ((BYPASS_LINE,) if self.bypass_present else ()):
            g = 1.0 / line.resistance_ohm
            for this, other in ((line.left, line.right), (line.right, line.left)):
                if this not in indices:
                    continue
                i = indices[this]
                matrix[i, i] += g
                if other == "source":
                    rhs[i] += g * self.source_voltage
                elif other in indices:
                    matrix[i, indices[other]] -= g
        rhs[indices["clinic"]] -= point.clinic_amps
        rhs[indices["pump"]] -= point.pump_amps
        try:
            values = np.linalg.solve(matrix, rhs)
        except np.linalg.LinAlgError as exc:
            raise ValueError("Feeder is disconnected or singular") from exc
        return {"source": self.source_voltage, **dict(zip(nodes, map(float, values)))}
