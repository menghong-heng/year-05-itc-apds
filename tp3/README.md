# TP03 · Gemma 3 fine-tuning results

Gemma 3 4B was fine-tuned separately on the original Khmer banking dataset and a Khmer Wikipedia QA subset. Both runs started from the same checkpoint and used 60 optimizer steps with identical LoRA settings. The base and fine-tuned models answered the same held-out questions within each dataset.

## Results

| Dataset | Test examples | chrF before | chrF after | Change | Exact matches before → after |
| --- | ---: | ---: | ---: | ---: | ---: |
| Original banking | 32 | 20.78 | 19.08 | −1.71 | 0 → 0 |
| Khmer Wikipedia QA | 31 | 18.90 | 32.88 | +13.99 | 0 → 8 |

**Original banking.** Validation loss fell from 2.034 at step 10 to 1.450 at step 60. On the test set, chrF fell by 1.71 points and exact matches stayed at zero. Answers hit the generation limit 8 times before fine-tuning and zero times afterward. Lower validation loss and fewer truncations coincided with lower reference overlap on held-out questions.

**Khmer Wikipedia QA.** Fine-tuning improved chrF by 13.99 points and matched 8 of 31 references exactly. Validation loss reached its minimum of 0.257 at step 50, then rose slightly to 0.260 at step 60. The evaluation used the step-50 checkpoint, selected by validation loss.

## Limitations

- **Different tasks.** Banking questions ask the model to recall information without a passage. Wikipedia questions provide the source passage. The before-to-after change within each dataset is more informative than comparing the two final scores.
- **Small test sets.** The test sets contain 32 and 31 examples. This comparison reports one run per dataset with one seed and one set of hyperparameters, so it gives a limited view of how consistently the results would repeat.
- **Text overlap.** chrF measures character n-gram overlap and exact match requires the same normalized wording. Both can underrate correct paraphrases. Factual accuracy requires checking the answers against their sources.
- **Reference quality.** The Wikipedia QA pairs were generated from source passages. The banking references have incomplete provenance and may contain outdated details.
