"""An inspectable Day-1 discrepancy -> probe -> update experiment."""

from .physics import FeederModel, OperatingPoint
from .world import HiddenWorld
from .experiment import PROBES
from .inference import build_candidates, update_posterior, choose_probe


def run_mission(seed: int = 7, noise_std: float = 0.0) -> dict:
    starting = OperatingPoint()
    documented = FeederModel(bypass_present=False)
    # True bypass is withheld from the inference algorithm. The evaluator
    # instantiates the truth; only observations reach hypothesis scoring.
    environment = HiddenWorld(_truth=FeederModel(bypass_present=True),
                              noise_std=noise_std, seed=seed)
    candidates = build_candidates(starting)
    prior = {candidate.name: 1.0 / len(candidates) for candidate in candidates}

    initial_voltage = environment.measure_pump_voltage(starting)
    model_prediction = documented.voltages(starting)["pump"]
    initial_posterior = update_posterior(prior, candidates, starting, initial_voltage)

    probe = choose_probe(candidates, initial_posterior, starting, PROBES)
    probe_point = probe.apply(starting)
    probe_voltage = environment.measure_pump_voltage(probe_point)
    posterior = update_posterior(initial_posterior, candidates, probe_point, probe_voltage)
    ordered = sorted(posterior.items(), key=lambda p: p[1], reverse=True)
    return {
        "metadata": {"project": "TWINLESS", "phase": "Day-1 deterministic research baseline",
                     "seed": seed, "noise_std": noise_std,
                     "physics_limit": "Toy steady-state resistive DC approximation, not an AC safety model",
                     "uses_meta_model": False},
        "observation": {"documented_pump_voltage": round(model_prediction, 5),
                        "measured_pump_voltage": round(initial_voltage, 5),
                        "residual_voltage": round(initial_voltage - model_prediction, 5)},
        "hypotheses": {name: round(weight, 6) for name, weight in initial_posterior.items()},
        "experiment": {"probe": probe.name,
                       "clinic_current_amps": probe_point.clinic_amps,
                       "pump_current_amps": probe_point.pump_amps,
                       "observed_voltage": round(probe_voltage, 5)},
        "posterior": {name: round(weight, 6) for name, weight in posterior.items()},
        "best_supported_model": ordered[0][0],
        "ground_truth_for_evaluator_only": "undocumented_bypass",
        "limitations": [
            "Single constructed fixture; no performance claims or empirical generalization.",
            "No independent action synthesis, intervention validation, or Meta model integration yet.",
            "Inadmissible physical control is out of scope; probes are simulated only.",
        ],
    }
