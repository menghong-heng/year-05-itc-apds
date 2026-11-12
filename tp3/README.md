# TP03 · Gemma 3 fine-tuning

[Open in Colab](https://colab.research.google.com/github/menghong-heng/year-05-itc-apds/blob/tp/tp3/APDS_TP03_Gemma3_Colab.ipynb) · [Course notes](docs/COURSE_NOTES.md) · [Earlier local report](TP03_Report.md)

The Colab notebook fine-tunes Gemma 3 4B separately on the supplied Khmer banking questions and on a Khmer Wikipedia QA subset. Both runs start from the same 4-bit checkpoint and use 60 optimizer steps, LoRA rank 8, and a learning rate of `2e-4`. The notebook compares held-out answers from the base model and each adapter.

## Run in Colab

1. Open the notebook and choose **Runtime → Change runtime type → GPU**.
2. Add your W&B API key to Colab **Secrets** as `WANDB_API_KEY` and enable **Notebook access**. Run Section 1.
3. In Section 2, upload `TP03_datasets.zip` from your local TP03 `data` folder. It contains the original banking CSV and the prepared splits for both datasets.
4. Run through Section 8 and keep `TP03_Gemma3_results.zip`. It contains both adapters, test predictions, the comparison table, and the loss plot. Section 6 prints the two W&B run links.

## Test a saved adapter

In Section 9, run the question-testing cells in order. Choose `khmerqa` or `banking` in the last cell. Leaving `QA_QUESTION` blank runs two sample questions and shows their references. To ask your own question with `khmerqa`, fill in both `QA_QUESTION` and `QA_PASSAGE`. `QA_REFERENCE` is optional.

For example, set `QA_PASSAGE` to `ភ្នំពេញជារាជធានីនៃប្រទេសកម្ពុជា។`, `QA_QUESTION` to `តើរាជធានីនៃប្រទេសកម្ពុជាមានឈ្មោះអ្វី?`, and `QA_REFERENCE` to `ភ្នំពេញ`.

Section 9 uses the adapters from the current session. After a Colab reset, select a GPU, run the installation cell in Section 1, and upload your saved `TP03_Gemma3_results.zip` when Section 9 prompts for it.

## Colab results

| Dataset | Test examples | chrF before | chrF after | Change | Exact matches before → after |
| --- | ---: | ---: | ---: | ---: | ---: |
| Original banking | 32 | 20.78 | 19.50 | −1.29 | 0 → 0 |
| Khmer Wikipedia QA | 31 | 18.90 | 32.73 | +13.83 | 0 → 8 |

Banking validation loss fell throughout training. Wikipedia QA reached its lowest validation loss at step 50. The Wikipedia prompts include a passage, so the before-to-after change within each dataset is the clearest comparison.

The supplied banking CSV is preserved in `data/raw/`. The Wikipedia subset credits sengtha / iAny and Khmer Wikipedia contributors under CC BY-SA 4.0. See the [dataset attribution and provenance](data/sources/khmerqa/ATTRIBUTION.md). The [local setup notes](docs/SETUP.md) cover the earlier notebook and runs.

The notebook follows Dustin Boswell and Trevor Foucher’s *The Art of Readable Code*, particularly its guidance on descriptive names, extracting subproblems, and doing one task at a time.
