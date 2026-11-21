# Data and reproduction

## Missing artifacts

| File | Role in the original exploratory notebook |
| --- | --- |
| `vmCloud_data.csv` | Source data for resource regression and forecasting exploration in cells 0–1. Both cells refer to a private Windows path. |
| `cpu_model.pkl` | CPU regression model saved in cell 2 and loaded in cell 3. |
| `memory_model.pkl` | Memory regression model saved in cell 2 and loaded in cell 3. |
| `encoder.pkl` | Fitted task-type and task-priority encoder saved in cell 2 and loaded in cell 3. |

The [paper draft](../cloud_darft1.pdf) names Kaggle on page 3 (§III-A). The exact dataset URL and version, full schema and data dictionary, collection provenance, and redistribution permissions for the CSV and model files are unknown.

**Never load untrusted pickle files.** Deserializing a pickle, including through `joblib.load`, can execute code. The demo uses explicit synthetic task profiles and requires none of these files.

## Columns referenced by the notebook

Cell 0 uses `power_consumption`, `num_executed_instructions`, `execution_time`, `task_type`, and `task_priority` as predictors, with `cpu_usage` and `memory_usage` as targets. The forecasting exploration in cell 1 also reads `timestamp`, `network_traffic`, `task_status`, and `energy_efficiency`. These are names referenced by the [original exploratory notebook](../multiagent_task.ipynb). The actual CSV types, units, sampling interval, and meaning of derived fields remain unverified.

## Reproduction status

Several notebook cells depend on earlier definitions or on the missing model files. Cell 0 fits the encoder and imputes values before the train/test split. It also fits the encoder with named columns and later passes unnamed inputs. Cell 1 uses a random split and calls the last 7, 30, or 365 test rows future forecasts. Those rows come from the existing test set. Its rolling CPU feature also includes the current row's target. A future evaluation would need chronological splits, preprocessing fitted on training data only, consistent transforms, and features available at the forecast cutoff.

Reproducing the draft's comparison requires the original inputs or a verified way to regenerate them, along with the baseline workloads, VM configurations, admission rules, and per-policy run logs. The draft lists power in watts and runtime in seconds, but the notebook labels unconverted products as Wh. Cell 6 also applies a priority weight to energy, and cell 7 adds reward points to VM energy totals. Confirm the units of the source fields and the accounting used for each reported total. [Claim audit](CLAIM_AUDIT.md)

The independent FIFO and Round Robin demo runs with `python -m src.demo_scheduling` from the repository root. It uses documented synthetic inputs and computes Wh from watts and seconds.
