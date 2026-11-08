# TP03 — Gemma 3 fine-tuning

[Notebook](APDS_TP03_Gemma3_Final.ipynb) · [Report](TP03_Report.md) · [Setup](docs/SETUP.md)

Khmer question-answering experiments with Gemma 3 4B, 4-bit loading, and LoRA. The executed notebook shows the alternative context-QA run; the report compares all four completed experiments.

```text
tp3/
├── APDS_TP03_Gemma3_Final.ipynb
├── TP03_Report.md
├── README.md
├── pyproject.toml
├── uv.lock
├── data/       # Source CSVs, frozen prepared splits, audits and attribution
├── scripts/    # Data preparation and prediction display helpers
├── results/    # Metrics, predictions and loss plots for four completed runs
└── docs/       # Setup, report figures and preserved course notes
```

## Run

From this `tp3` folder:

```bash
uv sync --python 3.11
uv run jupyter lab
```

Select the project kernel. A compatible NVIDIA CUDA GPU is required. Restart the kernel before changing experiments. New runs save to the ignored `outputs/` folder. Archived results preserve the original run metadata; only file organization and imports have changed since the saved execution.

The alternative QA run improved chrF from 20.50 to 32.14 on 31 examples. Banking answers still contain factual errors. Scores across context QA and closed-book banking are not directly comparable.

## Data

The supplied banking CSV is preserved unchanged in `data/raw/`. Alternative data derives from sengtha / iAny E-KHMER Technology and Wikipedia contributors under CC BY-SA 4.0. Keep the [attribution](data/sources/khmerqa/ATTRIBUTION.md) and provenance when redistributing it. No general license grant for the supplied banking data is asserted.

The [course notes](docs/COURSE_NOTES.md) are preserved separately. Model weights, checkpoints, environments and caches are excluded.
