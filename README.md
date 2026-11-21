# Cloud Task Scheduling: Q-learning Research Prototype

How do task allocation and admission decisions affect energy use and quality of service in cloud scheduling?

## Historical Q-learning research

The [original exploratory notebook](multiagent_task.ipynb) uses linear models to estimate CPU and memory demand and explores tabular Q-learning. A VM's agent considers remaining CPU, remaining memory, and its running energy tally when choosing whether to accept a task. The notebook also contains a round-robin allocation example.

FIFO (first in, first out) takes tasks in queue order. Round Robin cycles through VMs when assigning work. The [paper draft](cloud_darft1.pdf) discusses both as baselines.

## Run the standalone FIFO and Round Robin demo

From the repository root, use Python 3.10 or newer. The demo uses the standard library.

```sh
python -m src.demo_scheduling
```

Both policies see the same fixed-seed batch at time zero and use the same CPU and memory checks. Each VM runs one task at a time. The FIFO dispatcher assigns tasks in queue order to the earliest-available eligible VM, breaking ties in VM order. Tasks assigned to different VMs can start or finish out of order. Round Robin rotates through eligible VMs and queues a task on the selected VM if it is busy. Both reject a task only when no VM can fit it.

The output shows completion and rejection counts, rejection rate, makespan, and modeled task energy in Wh. The demo records one reward point per completion and subtracts one per rejection, separately from energy.

In the default run, both policies use **15.333 Wh** of modeled task energy. The demo shows **zero energy reduction**.

To run the tests in a Python environment with pytest installed:

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Limitations

The demonstration uses eight synthetic tasks and three simulated VMs. The makespan and rejection rate depend on the queue order, task demands, runtimes, and VM capacities. Each task uses fixed running power and runtime on every VM, so completing the same tasks yields the same modeled energy. The calculation omits host idle draw, shared resources, networking, and cooling. The repository has no hardware measurements or calibrated power model.

The historical experiment requires `vmCloud_data.csv`, `cpu_model.pkl`, `memory_model.pkl`, and `encoder.pkl`, all missing from this checkout. The draft reports 25% energy savings; this repository does not currently reproduce that comparison. The draft gives different percentages across sections. The original baseline configurations and run logs are unavailable. The draft lists watts and seconds, while the notebook labels power multiplied by runtime as Wh without converting seconds to hours. The input units, historical totals, and publication status remain unverified.

See the [claim audit](docs/CLAIM_AUDIT.md) and [data and reproduction notes](docs/DATA_AND_REPRODUCTION.md).
