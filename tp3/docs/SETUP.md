# Local setup with uv

Run these commands from `tp3/`:

```bash
uv sync --python 3.11
uv run python -m ipykernel install --user --name apds-tp03 --display-name "APDS TP03 (uv)"
uv run jupyter lab
```

Open `APDS_TP03_Gemma3_Final.ipynb` and select **APDS TP03 (uv)**. Training requires a compatible NVIDIA CUDA GPU. Restart the kernel before each experiment.

## Experiments

Set `EXPERIMENT` in the configuration cell:

| Preset | Data preparation | Epochs | Learning rate |
| --- | --- | ---: | ---: |
| `khmerqa_2epochs` | Alternative context QA; saved notebook execution | 2 | 0.0002 |
| `banking_v2_2epochs` | Revised institution-scoped banking | 2 | 0.0002 |
| `banking_v2_4epochs` | Revised banking; optional, not a reported run | 4 | 0.0002 |
| `acleda_2epochs` | Original banking preparation | 2 | 0.0002 |
| `acleda_4epochs` | Original banking preparation | 4 | 0.0002 |
| `acleda_lr5e5_2epochs` | Original banking; optional, not a reported run | 2 | 0.00005 |

The original supplied CSV is in `data/raw/dataasilida_cleaned.csv`. Frozen splits and review records are in `data/prepared/`. Helpers verify source/prepared hashes before training. Do not edit prepared data in place; generate a new version instead.

Epochs control training duration. Training loss is logged each optimizer step; validation and checkpoint saving run every ten steps, with final evaluation. The checkpoint with lowest validation loss is used for predictions.

New runs create unique folders in `outputs/`, which is ignored by Git. Recorded evidence for the four completed experiments is in `results/`: metrics JSON, prediction CSV and loss plot per run. See the [report](../TP03_Report.md) for their interpretation.

## Rebuild alternative data

Use a new destination to preserve existing splits:

```bash
uv run python -m scripts.build_alternative_dataset /path/to/new-folder /path/to/gemma-tokenizer --raw-file data/sources/khmerqa/data.json
```

The local tokenizer must be the Gemma tokenizer. The builder writes `data/raw/`, `data/prepared/khmerqa/` and `data/sources/khmerqa/` in the new destination. Omitting `--raw-file` downloads the pinned source. Keep its attribution and provenance with dataset derivatives.
