"""Compare FIFO dispatch and round-robin VM assignment on one synthetic batch."""

from dataclasses import dataclass, field
from math import fsum
from random import Random

from .energy import energy_wh

DEFAULT_SEED = 42


@dataclass(frozen=True)
class Task:
    name: str
    cpu_cores: int
    memory_gib: int
    runtime_seconds: int
    power_w: float
    priority: str


@dataclass(frozen=True)
class VM:
    name: str
    cpu_cores: int
    memory_gib: int


@dataclass(frozen=True)
class Completion:
    task: Task
    vm: VM
    finish_seconds: int

    @property
    def energy_wh(self) -> float:
        return energy_wh(self.task.power_w, self.task.runtime_seconds)


@dataclass
class ScheduleResult:
    completed: list[Completion] = field(default_factory=list)
    rejected: list[Task] = field(default_factory=list)
    reward_score: int = 0

    def record_reward(self, points: int) -> None:
        """Record dimensionless service points separately from energy."""
        self.reward_score += points

    @property
    def makespan_seconds(self) -> int:
        return max((item.finish_seconds for item in self.completed), default=0)

    @property
    def total_energy_wh(self) -> float:
        return fsum(item.energy_wh for item in self.completed)


DEMO_VMS = (VM("vm-a", 2, 4), VM("vm-b", 4, 8), VM("vm-c", 2, 12))


def build_workload(seed: int = DEFAULT_SEED) -> tuple[Task, ...]:
    """Shuffle explicit synthetic task profiles into a fixed-seed queue."""
    tasks = [
        Task("parse", 1, 2, 60, 100, "low"),
        Task("compile", 4, 4, 120, 180, "high"),
        Task("aggregate", 2, 10, 75, 140, "medium"),
        Task("index", 2, 4, 90, 120, "low"),
        Task("export", 1, 2, 45, 80, "medium"),
        Task("validate", 1, 4, 30, 90, "high"),
        Task("oversized-cpu", 5, 4, 60, 160, "high"),
        Task("oversized-memory", 2, 16, 60, 150, "medium"),
    ]
    Random(seed).shuffle(tasks)
    return tuple(tasks)


def schedule(
    tasks: tuple[Task, ...], vms: tuple[VM, ...], *, round_robin: bool
) -> ScheduleResult:
    """Dispatch one ordered batch at time zero with one task at a time per VM.

    Both policies reject only tasks that exceed every VM's CPU or memory
    capacity. Compatible work waits for its assigned VM if needed.
    """
    result = ScheduleResult()
    available_at = [0] * len(vms)
    next_vm = 0
    for task in tasks:
        eligible = [
            index
            for index, vm in enumerate(vms)
            if task.cpu_cores <= vm.cpu_cores and task.memory_gib <= vm.memory_gib
        ]
        if not eligible:
            result.rejected.append(task)
            result.record_reward(-1)
            continue

        if round_robin:
            # Scan cyclically from the cursor, skipping incompatible VMs.
            vm_index = min(eligible, key=lambda index: (index - next_vm) % len(vms))
            next_vm = (vm_index + 1) % len(vms)
        else:
            vm_index = min(eligible, key=lambda index: available_at[index])

        finish_seconds = available_at[vm_index] + task.runtime_seconds
        available_at[vm_index] = finish_seconds
        result.completed.append(Completion(task, vms[vm_index], finish_seconds))
        result.record_reward(1)
    return result


def run_demo(seed: int = DEFAULT_SEED) -> tuple[ScheduleResult, ScheduleResult]:
    tasks = build_workload(seed)
    return (
        schedule(tasks, DEMO_VMS, round_robin=False),
        schedule(tasks, DEMO_VMS, round_robin=True),
    )


def main() -> None:
    fifo, round_robin = run_demo()
    print(f"DEMO ONLY | Synthetic workload | Seed {DEFAULT_SEED}")
    for name, result in (("FIFO", fifo), ("Round Robin", round_robin)):
        completed = len(result.completed)
        rejected = len(result.rejected)
        rejection_rate = rejected / (completed + rejected)
        print(
            f"{name}: {completed} completed, {rejected} rejected "
            f"({rejection_rate:.1%}) | makespan {result.makespan_seconds} s | "
            f"modeled task energy {result.total_energy_wh:.3f} Wh | "
            f"reward {result.reward_score} points"
        )


if __name__ == "__main__":
    main()
