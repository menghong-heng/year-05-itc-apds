# APDS TP03 — Gemma 3 fine-tuning

```bash
uv sync --python 3.11
uv run python -m ipykernel install --user --name apds-tp03 --display-name "APDS TP03 (uv)"
uv run jupyter lab
```

Open `APDS_TP03_Gemma3_Final.ipynb` and select **APDS TP03 (uv)**. Restart the kernel before each experiment. A working NVIDIA CUDA driver is required.

## Dataset

`dataasilida_cleaned.csv` is the original supplied dataset. The source is preserved. Offline cleaning produced 303 candidate examples and quarantined 218 records; the saved splits contain 241 training, 30 validation and 32 test examples.

Prepared data, review records and the cleaning report are in `data_prepared/acleda/`. The notebook checks source and prepared-file hashes before training. Cleaning rules are implemented in `prepare_data.py`, outside the notebook.

## Experiments

| Preset | Dataset | Epochs | Learning rate |
| --- | --- | --- | --- |
| banking_v2_2epochs | Revised multi-bank supplied data | 2 | 0.0002 |
| banking_v2_4epochs | Revised multi-bank supplied data | 4 | 0.0002 |
| acleda_2epochs | Supplied banking data | 2 | 0.0002 |
| khmerqa_2epochs | Khmer Wikipedia QA subset | 2 | 0.0002 |
| acleda_4epochs | Supplied banking data | 4 | 0.0002 |
| acleda_lr5e5_2epochs | Supplied banking data | 2 | 0.00005 |

`acleda_2epochs` uses the original supplied dataset. `khmerqa_2epochs` uses the separate 303-example Khmer Wikipedia QA subset (242 train / 30 validation / 31 test). It keeps the same model, epoch budget, learning rate, batch and LoRA settings. This task provides context alongside each question. Banking and context-based QA have different content and answer lengths; scores should be reported per dataset.

Alternative data: `khmer_wikipedia_qa.csv`; prepared splits: `data_prepared/khmerqa/`; source, licensing and provenance: `data_sources/khmerqa/`. Data cleaning happens outside the notebook. The subset contains synthetic questions and answers and is not a factual benchmark. Dataset derivatives are CC BY-SA 4.0; preserve the attribution when publishing them.

## Outputs

Each run creates a unique folder under `outputs/` with local results JSON, predictions CSV, loss chart, saved splits, cleaning manifest, checkpoints and adapter. The notebook displays a compact score table and expandable prediction comparisons. It contains no Notion export cells or interpretation.

Commit the notebook, helper scripts, project configuration and lockfile together. `prediction_display.py` renders predictions; `prepare_data.py` validates prepared datasets. Keep local environments, model caches and checkpoints out of Git.

## Rebuild the alternative dataset

Use a new destination folder so existing prepared data is preserved:

```bash
uv run python build_alternative_dataset.py /path/to/new-folder /path/to/gemma-tokenizer --raw-file data_sources/khmerqa/data.json
```

The tokenizer directory must contain the saved Gemma tokenizer. Omitting --raw-file downloads the source at the pinned revision. The builder writes a CSV, audit files, splits and provenance. No training or interpretation is performed during preparation.

## Training duration and monitoring

Training ends after NUM_TRAIN_EPOCHS complete passes over the training set. max_steps is not set. Training loss is logged every optimizer step; validation and checkpoint saving run every 10 optimizer steps. Loss plots use optimizer steps on the horizontal axis. The best checkpoint is selected from those evaluation points, so it can precede the final update.

results.json records requested epochs, completed epochs, actual optimizer steps, and generation settings. Existing step-limited runs are preserved and keep their original settings. The completed notebook currently selects khmerqa_2epochs. Use banking_v2_2epochs for the revised banking experiment with the same epoch budget.

## Revised banking preparation

The banking_v2_2epochs preset uses data_prepared/banking_v2/. Read cleaning_report.md there before comparing results. This version uses explicit institution prefixes and a revised eligibility policy, with previously held-out groups protected from training. Run a fresh baseline; old test scores are not directly comparable. Original acleda and khmerqa presets remain available.

prepare_banking_v2.py reproduces v2 from the original CSV, previous acleda preparation, and a local saved Gemma tokenizer. It refuses to overwrite an existing prepared directory.

## Completed comparison

Read [TP03_Report.md](TP03_Report.md) for the measured experiment comparison, loss analysis, and limitations. The notebook keeps the latest alternative-dataset execution outputs; earlier completed banking notebooks are preserved in their run folders.
