# Khmer Wikipedia QA dataset attribution

Source: [sengtha/khmer-qa](https://huggingface.co/datasets/sengtha/khmer-qa)

Pinned revision: `3ca26dc817cae20dc4c574e7027b581ec7cb73ae`.

Credit: sengtha / iAny (E-KHMER Technology), and Khmer Wikipedia contributors.

The upstream card describes Qwen2.5-generated questions and answers based on Khmer Wikipedia (`wikimedia/wikipedia`, `20231101.km`). These are synthetic QA pairs, not human-verified ground truth. See upstream_README.md for the original description and limitations.

License: **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.

[License summary](https://creativecommons.org/licenses/by-sa/4.0/)

[Legal text](https://creativecommons.org/licenses/by-sa/4.0/legalcode)

Changes: deterministic subset of 303 extractive examples; normalized Unicode and whitespace; removed invalid/control-token text, duplicates, repeated contexts/questions/answers, examples whose answer is absent from context, and examples exceeding 2048 formatted Gemma tokens. Context and question are combined into the input column. Prepared CSV, splits, and derived dataset content remain under CC BY-SA 4.0. Keep this attribution with redistributed dataset files. No endorsement is implied.

The raw source is saved as data.json. provenance.json records the URL, revision, source hash, selected row numbers and token counts. build_alternative_dataset.py reproduces the transformation.
