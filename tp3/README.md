# APDS TP03 — Gemma 3 fine-tuning

Local Khmer question-answering experiments using Gemma 3 4B, 4-bit loading, and LoRA adapters.

## Submission

- [Executed notebook](APDS_TP03_Gemma3_Final.ipynb): configuration, training, loss curves, and before/after predictions. The saved execution uses the alternative Khmer QA dataset.
- [Experiment report](TP03_Report.md): workflow, hyperparameters, data preparation, loss analysis, measured comparisons, and limitations.
- [Local setup with uv](README_local_uv.md): installation, experiment presets, and reproduction instructions.
- `outputs/`: recorded metrics, raw predictions, saved splits, cleaning manifests, plots, and available executed notebooks for the four reported experiments.
- `data_prepared/`: frozen datasets and preparation audits; cleaning code is in the Python helper scripts.

The alternative QA run improved chrF from 20.50 to 32.14 on 31 held-out examples. Banking outputs remain unreliable; see the report for the unsuccessful experiments and remaining errors. Context-supplied QA and closed-book banking scores are not directly comparable.

## Running

```bash
uv sync --python 3.11
uv run jupyter lab
```

Open the notebook and select the project environment. A compatible NVIDIA CUDA GPU is required. Restart the kernel before changing experiments. Training saves new run folders without replacing the recorded results.

## Data attribution

The supplied banking CSV is preserved as received. The alternative dataset derives from sengtha / iAny E-KHMER Technology and Wikipedia contributors, under CC BY-SA 4.0. Preserve the [attribution and license information](data_sources/khmerqa/ATTRIBUTION.md) and source provenance when redistributing the data. No general license grant for the supplied banking data is asserted here.

Local environments, model caches, checkpoints, and adapters are excluded from this submission package.

## Course notes

The pre-existing [TP03 course notes](COURSE_NOTES.md) are preserved separately from the experiment submission.
