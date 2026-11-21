import pytest

from src.demo_scheduling import Task, VM, schedule
from src.energy import energy_wh


@pytest.mark.parametrize(
    ("runtime_seconds", "expected_wh"),
    [(3600, 100), (60, 100 / 60), (0, 0)],
)
def test_energy_wh_converts_seconds(runtime_seconds, expected_wh):
    assert energy_wh(100, runtime_seconds) == expected_wh


@pytest.mark.parametrize("invalid", [-1, float("nan"), float("inf"), -float("inf")])
def test_energy_wh_rejects_invalid_power_or_runtime(invalid):
    with pytest.raises(ValueError, match="power_w"):
        energy_wh(invalid, 60)
    with pytest.raises(ValueError, match="runtime_seconds"):
        energy_wh(100, invalid)


def test_low_priority_task_consumes_energy_when_completed():
    task = Task("low-priority", 1, 1, 60, 100, "low")
    result = schedule((task,), (VM("vm", 1, 1),), round_robin=False)

    assert len(result.completed) == 1
    assert result.completed[0].energy_wh == 100 / 60


def test_reward_updates_do_not_change_energy():
    task = Task("task", 1, 1, 60, 100, "low")
    result = schedule((task,), (VM("vm", 1, 1),), round_robin=False)
    initial_energy_wh = result.total_energy_wh

    result.record_reward(5)
    assert result.reward_score == 6
    assert result.total_energy_wh == initial_energy_wh

    result.record_reward(-20)
    assert result.reward_score == -14
    assert result.total_energy_wh == initial_energy_wh
