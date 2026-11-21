# Claim audit

Page numbers refer to the [paper draft](../cloud_darft1.pdf). Cell indexes are zero-based and refer to the [original exploratory notebook](../multiagent_task.ipynb).

| Claim or issue | Draft evidence | Notebook evidence and status |
| --- | --- | --- |
| 25% vs. 30% energy savings | Page 1 Abstract reports 25% against FIFO and Round Robin. Page 1 §I-A (“Novality”) gives 30% against the same baselines. Page 6 §VI gives 25%. | Cells 5–7 contain separate scheduling examples. The checkout has no runnable matched comparison or source table that establishes either figure. |
| Inter-cloud vs. intra-cloud sharing | Page 1 Abstract and §I-A describe inter-cloud sharing. Page 5 §IV-F and page 6 §V-F describe sharing within one cloud only. | Cell 7 shares rewards across `cloud.vms`. It adds reward points to each VM's `total_energy_consumed`, which can produce invalid or negative energy tallies. |
| Missing data and models | Page 3 §III-A refers to Kaggle. Page 5 §IV-C and page 6 §V-B describe pretrained models and an encoder. | Cells 0–1 read a private Windows path to `vmCloud_data.csv`. Cell 2 writes `cpu_model.pkl`, `memory_model.pkl`, and `encoder.pkl`. Cells 3 and 5 load them. All four files are missing. |
| SageMaker and S3 | Page 1 Abstract and §I-A describe integration. Page 4 §IV-A describes S3 storage. | Cells 0–1 read a local CSV and cells 2–3 use local model files. No notebook cell contains calls to either service. |
| Energy units and priority | Page 3 §III-B, Table I, lists watts and seconds and defines an efficiency field in W/s. Page 5 §IV-G multiplies power, runtime, and a priority weight. | Cell 5 multiplies power by runtime. Cells 6–7 label totals in Wh without a seconds-to-hours conversion. Cell 6 gives low-priority tasks zero weight, so an allocated task can be assigned zero energy. With watts and seconds, physical task energy in Wh is `power_w * runtime_seconds / 3600`. |
| Baseline comparability and rejection rate | Page 5 §IV-I lists allocation rate. Page 6 §VI reports about 100% assignment efficacy and says the scheduler can reject low-priority tasks. It names random allocation and FCFS, while page 1 names FIFO and Round Robin. | Cells 5–7 can leave tasks unallocated and use different task lists or VM setups. Completing fewer tasks can lower total Wh. To assess service across policies, report offered, completed and rejected counts, rejection rates, and a timing metric alongside energy. |

## Questions for the co-authors

- Which run produced each percentage? Can you share the underlying totals, savings formula, workloads, VM capacities, seeds, and per-policy completion, rejection and timing results?
- Which version of the reward-sharing code produced the reported results, and did rewards ever cross cloud boundaries?
- How were power, runtime, and idle consumption measured or modeled? Were priority weights and reward points included in the reported energy?
- What is the exact dataset URL and version? What may be redistributed? Is there a shareable implementation or run record for the SageMaker and S3 claims?
- Is there an official publication record for this draft, such as a DOI or publisher URL?
