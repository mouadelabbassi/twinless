"""Controlled probe definitions for the small-signal simulation fixture."""

from dataclasses import dataclass
from .physics import OperatingPoint


@dataclass(frozen=True)
class Probe:
    name: str
    clinic_delta: float = 0.0
    pump_delta: float = 0.0
    cost: float = 1.0

    def apply(self, point: OperatingPoint) -> OperatingPoint:
        updated = OperatingPoint(
            clinic_amps=point.clinic_amps + self.clinic_delta,
            pump_amps=point.pump_amps + self.pump_delta,
        )
        # These are fixture-specific laboratory limits, not certified safety thresholds.
        if not (0.5 <= updated.clinic_amps <= 2.1 and 0.5 <= updated.pump_amps <= 1.8):
            raise ValueError(f"Probe {self.name} outside simulated admissible envelope")
        return updated


PROBES = (
    Probe("increase_pump_load", pump_delta=0.6, cost=1.0),
    Probe("decrease_pump_load", pump_delta=-0.4, cost=1.0),
    Probe("increase_clinic_load", clinic_delta=0.4, cost=1.5),
    Probe("decrease_clinic_load", clinic_delta=-0.4, cost=1.5),
)
