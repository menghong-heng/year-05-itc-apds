# Banking dataset v2 preparation

Scope: multi-institution banking QA. Original CSV and prior prepared data are preserved.

## Prepared records

- 521 original records inspected.
- 276 structurally prepared examples: 234 training, 20 validation, 22 test.
- 245 records quarantined for missing institution/product context, conflicting answers, or duplicates.
- 88 previously excluded records restored under the new policy.
- Institution counts: ACLEDA 186, AEON 62, KB Daehan 11, NBC 10, ABA 7.
- Formatted Gemma token lengths: 65–1273, below the 2048-token limit.

## What changed

The input identifies the institution before the question. Names are extracted only from the same source record; neighboring rows are not used to guess scope. 148 records explicitly name the institution in the question. Another 128 have a single institution mention in the answer; their scope evidence is marked as requiring review. This is evidence-based annotation, not independent verification of the source or product attribution.

Numeric terms, fees, dates and offers are flagged for source review rather than automatically removed. No financial values, product names or answer facts were rewritten. Only two literal duplicated question fragments are eligible for correction: តើសេតើ and ឥណទានឥណទាន. Every record retains its original source-row number.

All institutions follow the same policy; KB Daehan is no longer uniquely excluded. Records without enough institution/product evidence remain quarantined. Missing source URLs and dates are recorded as missing, not invented. Prepared examples are not verified current financial advice.

## Evaluation integrity

Old question/answer-group memberships are frozen. Eligible previously held-out groups remain held out; no original validation/test group was moved into training. New eligible groups with no prior membership are added to training. Groups that would cross prior splits are rejected.

The v2 test set has 22 records rather than 32 because some old records do not meet the declared scope policy. Institution prefixes also change the inputs. This is a new evaluation setup and requires a fresh base-model evaluation. Do not directly attribute a score change from the old runs to better fine-tuning. previous_split_accounting.csv makes every prior candidate's disposition visible.

The fixed-deposit category question at source row 229 remains quarantined because its bank is not identified in the record itself. It has not been copied into training. V2 cannot teach facts that are still absent from training.

## Files

- training_candidate.csv: scoped input, normalized output, original row.
- annotations.csv: institution, evidence, flags, source/date status and split.
- needs_review.csv: excluded records and reasons.
- splits.json: saved train/validation/test examples.
- previous_splits.json and previous_split_accounting.csv: frozen-holdout evidence.
- manifest.json: hashes, policy, counts and review flags.

No training has been performed on v2 during preparation.
