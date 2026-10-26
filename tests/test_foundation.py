import math
import pytest
from twinless.physics import FeederModel, OperatingPoint, Line
from twinless.experiment import PROBES, Probe
from twinless.inference import build_candidates, choose_probe, update_posterior
from twinless.mission import run_mission


def test_voltage_solver_preserves_source_and_kcl_physics():
    model = FeederModel(bypass_present=False)
    op = OperatingPoint()
    values = model.voltages(op)
    assert values["source"] == 12.0
    assert values["source"] > values["hub"] > values["pump"]
    # Hub supply line carries pump + clinic sinks with no bypass.
    assert math.isclose((12.0 - values["hub"]) / 0.4, 2.5, abs_tol=1e-9)


def test_bypass_changes_observable_voltage():
    point = OperatingPoint()
    assert FeederModel(True).voltages(point)["pump"] > FeederModel(False).voltages(point)["pump"]


def test_candidate_ambiguity_at_initial_operating_point():
    start = OperatingPoint()
    models = {c.name: c.predict(start) for c in build_candidates(start)}
    assert models["sensor_bias_only"] == pytest.approx(models["undocumented_bypass"])
    assert models["documented_topology"] != pytest.approx(models["undocumented_bypass"])


def test_probe_is_admissible_and_differentiating():
    start = OperatingPoint()
    candidates = build_candidates(start)
    posterior = {"documented_topology": 0.0, "undocumented_bypass": 0.5, "sensor_bias_only": 0.5}
    probe = choose_probe(candidates, posterior, start, PROBES)
    point = probe.apply(start)
    pred = {c.name: c.predict(point) for c in candidates}
    assert abs(pred["undocumented_bypass"] - pred["sensor_bias_only"]) > 0.01


def test_run_mission_reproducible_and_recovers_hidden_bypass():
    result = run_mission(seed=11)
    assert result == run_mission(seed=11)
    assert result["observation"]["residual_voltage"] > 0
    assert result["best_supported_model"] == "undocumented_bypass"
    assert result["posterior"]["undocumented_bypass"] > 0.85
    assert result["metadata"]["uses_meta_model"] is False


def test_noise_and_invalid_inputs():
    assert run_mission(seed=9, noise_std=0.02) == run_mission(seed=9, noise_std=0.02)
    with pytest.raises(ValueError):
        Line("source", "source", 0.1)
    with pytest.raises(ValueError):
        Probe("unsafe", clinic_delta=9).apply(OperatingPoint())
    with pytest.raises(ValueError):
        update_posterior({"x":1}, build_candidates(OperatingPoint()), OperatingPoint(), 0, sigma=0)
