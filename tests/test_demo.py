import pytest

from src.demo_scheduling import Task, VM, build_workload, run_demo, schedule


def test_seed_reproduces_queue_and_results():
    assert build_workload(42) == build_workload(42)
    assert build_workload(42) != build_workload(43)
    assert run_demo(42) == run_demo(42)


def test_baselines_process_the_same_workload_with_the_same_capacity_checks():
    workload = build_workload()
    oversized = {"oversized-cpu", "oversized-memory"}
    expected_completed = [task for task in workload if task.name not in oversized]
    expected_rejected = [task for task in workload if task.name in oversized]

    for result in run_demo():
        assert len(result.completed) == 6
        assert len(result.rejected) == 2
        assert [completion.task for completion in result.completed] == expected_completed
        assert result.rejected == expected_rejected
        for completion in result.completed:
            assert completion.task.cpu_cores <= completion.vm.cpu_cores
            assert completion.task.memory_gib <= completion.vm.memory_gib


def test_energy_is_positive_for_each_completed_task():
    fifo, round_robin = run_demo()
    for result in (fifo, round_robin):
        for completion in result.completed:
            task = completion.task
            assert completion.energy_wh > 0
            assert completion.energy_wh == task.power_w * task.runtime_seconds / 3600
        assert result.total_energy_wh == pytest.approx(55_200 / 3600)


def test_policies_differ_in_assignment_and_model_waiting():
    vms = (VM("vm-a", 1, 1), VM("vm-b", 1, 1))
    tasks = (
        Task("long", 1, 1, 100, 100, "low"),
        Task("short-1", 1, 1, 10, 100, "low"),
        Task("short-2", 1, 1, 10, 100, "low"),
    )

    fifo = schedule(tasks, vms, round_robin=False)
    round_robin = schedule(tasks, vms, round_robin=True)

    assert [item.vm for item in fifo.completed] == [vms[0], vms[1], vms[1]]
    assert [item.vm for item in round_robin.completed] == [vms[0], vms[1], vms[0]]
    assert fifo.makespan_seconds == 100
    assert round_robin.makespan_seconds == 110
