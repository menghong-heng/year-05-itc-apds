# Dataset preparation report

Source: dataasilida_cleaned.csv
Training candidates: 303; quarantined records: 218.

Checks passed: nonempty normalized fields, unique pairs, no conflicting grouped questions, disjoint question/answer groups across splits.

## Review reasons

Counts overlap because a record can have multiple reasons.

- different_bank_kb_daehan: 13
- exact_duplicate_of_row_79: 1
- missing_banking_product_context: 73
- multiple_distinct_answers: 52
- normalized_duplicate_of_row_213: 1
- normalized_duplicate_of_row_83: 1
- potentially_outdated_financial_information: 162
- repeated_question_prefix: 1

## Limits

Automated cleaning does not establish factual accuracy. Financial statements flagged as potentially outdated were quarantined rather than corrected. Review the remaining examples for domain accuracy before drawing conclusions. Token-length and assistant-label checks still run in the notebook after loading the tokenizer.