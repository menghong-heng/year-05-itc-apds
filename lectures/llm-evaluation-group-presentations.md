# APDS Group Presentations — LLM Performance Evaluation

A **reference** is the expected answer or transcript. A **candidate** is the model output being scored. The first nine groups cover metrics for exact answers, classification, word overlap, semantic similarity, and transcription errors. Group 10 brings them together by task.

## 1. Exact Match (EM)

**Exact Match** awards 1 when the candidate equals the reference and 0 otherwise. The dataset score is the number of matches divided by the number of examples. In the five-question demo, four matches give 80% EM.

- **Strict EM** treats case, punctuation, and whitespace as part of the answer. With `Phnom Penh` as the reference, `The answer is Phnom Penh` scores 0.
- **Normalized EM** applies documented rules to both texts before checking equality. Lowercasing, for example, lets `Paris` match `paris`. Remove punctuation or articles only when those distinctions are irrelevant to the task.

EM is fast and reproducible for short-answer or extractive question answering and fixed-format outputs. It gives binary scores, so a valid rephrasing or a partly correct answer can receive 0.

## 2. Accuracy

**Accuracy** is the fraction of predictions judged correct under the task's scoring rule. In binary classification, `Accuracy = (TP + TN) / (TP + TN + FP + FN)`. True positives (TP) and true negatives (TN) are correct predictions. False positives (FP) are false alarms, and false negatives (FN) are missed positives.

In the five-review sentiment demo, Gemini 1.5 and Llama 3 each score 80% (4/5) while missing different reviews. Accuracy is useful for multiple-choice questions and classification with reasonably balanced classes. On an imbalanced dataset, a model can score well by predicting the majority class and still miss most minority cases.

## 3. Precision, Recall, and F1

| Metric | Formula | What it measures |
| --- | --- | --- |
| **Precision** | `TP / (TP + FP)` | How many predicted positives are actually positive |
| **Recall** | `TP / (TP + FN)` | How many actual positives the model finds |
| **F1** | `2PR / (P + R)` | The harmonic mean of precision and recall |

With 8 true positives, 2 false positives, and 12 false negatives, precision is 80%, recall is 40%, and F1 is 53.3%. The low recall pulls F1 down. In spam filtering, high precision helps avoid hiding legitimate messages. In the screening example, high recall helps reduce missed cases.

F1 omits true negatives. For multiclass tasks, report per-class scores or specify the averaging method, since a single aggregate can hide performance on individual classes. In Python, scikit-learn provides the three scores and the confusion matrix.

## 4. BLEU

**Bilingual Evaluation Understudy** measures overlap with one or more reference translations. An **n-gram** is a sequence of `n` consecutive tokens. Standard BLEU takes a weighted geometric mean of modified n-gram precisions, typically for n = 1 through 4, then multiplies it by a **brevity penalty**.

- **Clipping** caps each candidate n-gram's match count at its highest count in any single reference. This prevents repeated words from inflating precision.
- The **brevity penalty** is 1 when candidate length `c` is at least the effective reference length `r`. For a shorter, nonempty candidate it is `exp(1 - r/c)`.

For `the cat is on mat` against `the cat is on the mat`, five of five unigrams and three of four bigrams match. Simplified BLEU-2 is `exp(1 - 6/5) × √(1 × 0.75) ≈ 0.709`, or 70.9 on a 0–100 scale. BLEU is most useful for corpus-level translation comparisons with the same references, tokenization, and scoring settings. Correct paraphrases can score low, and high overlap can coexist with factual errors.

## 5. ROUGE

**Recall-Oriented Understudy for Gisting Evaluation** is used mainly in summarization. **Recall** divides the overlap by the number of reference units, **precision** divides by the number of candidate units, and **F1** balances both. Reporting F1 helps expose padding that recall alone would overlook.

| Variant | Matching units |
| --- | --- |
| **ROUGE-N** | Clipped consecutive n-grams. ROUGE-1 counts tokens and ROUGE-2 counts adjacent pairs. |
| **ROUGE-L** | Longest common subsequence (LCS). Tokens must occur in the same order, with gaps allowed. |
| **ROUGE-Lsum** | Summary-level union of sentence-level LCS matches. |
| **ROUGE-W** | Weighted LCS that gives extra credit to consecutive runs. |
| **ROUGE-S** | Ordered pairs with gaps allowed, called skip-bigrams. |
| **ROUGE-SU** | Skip-bigrams plus individual tokens. |

Changing `the cat sat on the mat` to `the cat lay on the mat` gives ROUGE-1 and ROUGE-L F1 of 0.833, with ROUGE-2 at 0.600 because the change breaks two adjacent pairs. In the 10-question class experiment, Gemma 3 1B scored higher than Gemma 3 270M on ROUGE-1, ROUGE-2, and ROUGE-L F1. ROUGE scores depend on references and preprocessing, especially tokenization and stemming. Shared wording alone gives limited evidence about paraphrases, factuality, or readability.

## 6. METEOR

**METEOR** aligns candidate and reference words through exact matches, stems, and synonyms where supported by the language resources. Each word can align at most once. The score combines precision and recall with a **fragmentation penalty** for breaking matched words into separate runs.

Using the settings in Group 6's NLTK demo, the recall-weighted score is `F = 10PR / (R + 9P)` and the penalty is `0.5 × (chunks / matched words)³`. The final score is `F × (1 - penalty)`. Against `the cat sleeps`, the identical candidate scores 0.9815, while `sleeps cat the` scores 0.5000. Every word still matches, but the reversed order creates three chunks.

METEOR is useful for translation and other reference-based tasks where some word forms and synonyms should receive credit. Its coverage depends on language resources such as WordNet, and a high score can coexist with factual errors.

## 7. BERTScore

**BERTScore** compares tokens using contextual embeddings from a pretrained encoder such as BERT or RoBERTa. It calculates pairwise cosine similarities and takes each token's best match in the other text. **Precision** averages the best matches for candidate tokens, **recall** does the same for reference tokens, and **F1** is their harmonic mean. Optional IDF weighting gives more weight to rarer tokens, and baseline rescaling spreads out scores.

In the paraphrasing demo, Qwen2.5-0.5B earns BERTScore F1 of 0.9133, BLEU of 27.34/100, and ROUGE-L F1 of 0.6316. SmolLM2-135M repeats the reference and earns full marks on all three. In a second example, SmolLM2's summary omits Wi-Fi and study rooms, lowering BERTScore recall to 0.7136 versus Qwen's 0.9181.

BERTScore gives credit for wording changes in paraphrasing, summarization, and open-ended question answering. Scores depend on the encoder and layer, and computing embeddings costs more than counting overlaps. Negation, factual claims, and task requirements such as actually rephrasing the answer still need separate checks.

## 8. Word Error Rate (WER)

**WER** aligns a transcript with a reference at the word level using minimum edit distance. `WER = (S + D + I) / N`, where `S` is substitutions, `D` is deletions, `I` is insertions, and `N` is the number of reference words. Lower is better. A perfect match scores 0%, and enough extra words can push WER above 100%.

Replacing `books` with `book` in `I love to read books` yields one substitution across five words, or 20% WER. In the class comparison on five sentences with 32 reference words, Whisper-base made 3 edits (9.4%) and Whisper-tiny made 6 (18.8%). WER is useful for speech recognition, including subtitles and voice assistants. Word segmentation and text normalization affect the score, which gives equal cost to word edits with very different effects on meaning.

## 9. Character Error Rate (CER)

**CER** uses the same edit-rate formula as WER, with characters as the alignment units and reference length measured in characters. `cat` to `cut` is one substitution, and `cat` to `cart` is one insertion. Both give `1/3 = 33.3%` CER. Lower is better, and insertions can push the score above 100%.

CER is useful for OCR, spelling correction, transcription, and exact names or codes. It detects small spelling errors and works without word segmentation. Spaces, punctuation, Unicode normalization, and the choice of character unit can change the result. In the OCR results shown in class, Chakkhu had 4.50% CER, Netra-OCR had 5.87%, and Tesseract 5 had 20.55%.

## 10. Comparative Evaluation of LLM Metrics

Choose metrics based on the expected output and the errors that matter. For example, `The capital is Paris` can be judged correct under a task rubric and still receive strict EM of 0 against `Paris`. For a one-word reference of `hello`, the prediction `helo` yields 100% WER and 20% CER because the same edit changes one of one words and one of five characters.

| Task | Metrics | What to look for |
| --- | --- | --- |
| Extractive question answering | EM + token-level F1 | Exact answers and partial token overlap |
| Text classification | Accuracy + precision, recall, and F1 | Overall correctness, false alarms, and missed cases |
| Machine translation | BLEU + METEOR or BERTScore | Phrase overlap and similarity when wording changes |
| Text summarization | ROUGE + BERTScore + factuality review | Reference coverage, paraphrases, and whether claims are supported |
| Speech recognition | WER + CER | Whole-word mistakes and smaller spelling errors |
| OCR | CER + WER | Character fidelity and whether whole words survive |

Keep the test set, reference answers, preprocessing, and scoring settings consistent when comparing systems. Use human or task-specific checks when factual correctness matters, since overlap and embedding similarity can remain high when a claim changes.

## Slides

Source decks from the APDS Group Presentations folder, in group order.

1. `Exact_Match_EM_Evaluation_for_Large_Language_Models_no_gamma.pptx`
2. `2026.11.13 - ADV Group 2 Presentation (1).pdf`
3. `Precision_Recall_F1_Research_Presentation.pptx (1).pdf`
4. `Group_4_BLEU_Score_10_Slides (1).pptx`
5. `ROUGE SCORE Group5.pdf` and `ROUGE_Score_Group5_final.pdf`
6. `Group 6 METEOR Score (2).pdf`
7. `BERTScore - Group 07.pptx`
8. `Group8_Word_Error_Rate_WER_13_Slides.pdf`
9. `Group9-CER (2).pdf`
10. `Group10_Comparative_LLM_Evaluation (2).pdf`
