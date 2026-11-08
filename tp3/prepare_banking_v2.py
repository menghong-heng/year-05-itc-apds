"""Prepare versioned, institution-scoped banking QA without changing source facts."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re
import unicodedata

from prepare_data import (
    CONTROL_TOKEN,
    DATE_OR_OFFER,
    FEE_WAIVER,
    GENERIC_QUESTION,
    MONEY_OR_TERMS,
    PRODUCT_REFERENCE,
    clean_text,
    group_key,
    read_csv_records,
)

POLICY = "banking-v2-institution-scope-frozen-holdouts"
BANKS = {
    "ACLEDA": ("អេស៊ីលីដា", r"អេស៊ីលីដា|(?<![a-z])acleda(?![a-z])"),
    "ABA": ("ABA", r"(?<![a-z])aba(?![a-z])"),
    "AEON": ("អ៉ីអន", r"អ៉ីអន|អ៊ីអន|(?<![a-z])aeon(?![a-z])"),
    "NBC": ("ធនាគារជាតិនៃកម្ពុជា", r"ធនាគារជាតិនៃកម្ពុជា"),
    "KB Daehan": ("ខេប៊ី ដេហាន", r"ខេប៊ី|ដេហាន|(?<![a-z])kb\s*daehan(?![a-z])"),
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    Path(path).write_text(
        json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def read_table(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_table(path, rows, columns):
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def bank_mentions(text):
    normalized = group_key(text)
    return [
        bank
        for bank, (_, pattern) in BANKS.items()
        if re.search(pattern, normalized, re.IGNORECASE)
    ]


def text_problems(text):
    problems = []
    if "\ufffd" in text or CONTROL_TOKEN.search(text):
        problems.append("invalid_text_or_reserved_token")
    for character in text:
        if unicodedata.category(character) == "Cc" and not character.isspace():
            problems.append("control_character")
            break
    for character in text:
        if not character.isalpha():
            continue
        if "\u1780" <= character <= "\u17ff":
            continue
        if unicodedata.name(character, "").startswith("LATIN "):
            continue
        problems.append("unexpected_alphabetic_script")
        break
    return problems


def fix_question_prefix(question):
    """Fix only literal, duplicated Khmer fragments; preserve financial meaning."""
    question = question.replace("តើសេតើ", "តើ")
    question = question.replace("ឥណទានឥណទាន", "ឥណទាន")
    return question


def review_flags(answer):
    flags = []
    if DATE_OR_OFFER.search(group_key(answer)):
        flags.append("date_or_offer_requires_source_check")
    if FEE_WAIVER.search(group_key(answer)):
        flags.append("fee_policy_requires_source_check")
    if re.search(r"\d", answer) and MONEY_OR_TERMS.search(group_key(answer)):
        flags.append("numeric_terms_require_source_check")
    return flags


def scope_question(question, answer):
    """Use only institution names explicitly present in the same source record."""
    question_banks = bank_mentions(question)
    answer_banks = bank_mentions(answer)
    if len(question_banks) == 1:
        bank = question_banks[0]
        evidence = "explicit_in_question"
    elif len(question_banks) > 1:
        return None, None, "multiple_institutions_in_question"
    elif len(answer_banks) == 1:
        bank = answer_banks[0]
        evidence = "explicit_in_answer_requires_scope_review"
    elif len(answer_banks) > 1:
        return None, None, "multiple_institutions_without_question_scope"
    else:
        return None, None, "institution_not_identified"

    compact = group_key(question).replace(" ", "")
    if PRODUCT_REFERENCE.search(compact) or GENERIC_QUESTION.search(compact):
        return bank, evidence, "product_context_not_resolved"
    return bank, evidence, None


def frozen_memberships(splits):
    question_splits = defaultdict(set)
    answer_splits = defaultdict(set)
    for split_name, records in splits.items():
        for record in records:
            question_splits[group_key(record["input"])].add(split_name)
            answer_splits[group_key(record["output"])].add(split_name)
    return question_splits, answer_splits


def assign_frozen_splits(records, old_splits):
    """Keep original question/answer groups in their old split; add new groups to train."""
    question_splits, answer_splits = frozen_memberships(old_splits)
    parents = list(range(len(records)))

    def root(index):
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    seen = {}
    for index, record in enumerate(records):
        for name, text in (
            ("question", record["original_question"]),
            ("question", record["question"]),
            ("answer", record["output"]),
        ):
            key = (name, group_key(text))
            if key in seen:
                parents[root(index)] = root(seen[key])
            else:
                seen[key] = index

    components = defaultdict(list)
    for index, record in enumerate(records):
        components[root(index)].append(record)

    splits = {name: [] for name in ("train", "validation", "test")}
    accepted = []
    excluded = []
    for component in components.values():
        anchors = set()
        for record in component:
            anchors.update(question_splits[group_key(record["original_question"])])
            anchors.update(question_splits[group_key(record["question"])])
            anchors.update(answer_splits[group_key(record["output"])])
        if len(anchors) > 1:
            for record in component:
                record["reason"] = "restored_group_crosses_frozen_splits"
                excluded.append(record)
            continue
        split_name = next(iter(anchors)) if anchors else "train"
        for record in component:
            record["split"] = split_name
            record["split_origin"] = "frozen_group" if anchors else "new_training_group"
            splits[split_name].append({"input": record["input"], "output": record["output"]})
            accepted.append(record)
    if not all(splits.values()):
        raise ValueError("One frozen split has no eligible records.")
    return splits, accepted, excluded


def validate_prepared(splits, annotations, old_splits):
    if set(splits) != {"train", "validation", "test"}:
        raise ValueError("Expected train, validation and test splits.")
    question_splits, answer_splits = frozen_memberships(old_splits)
    all_pairs = [
        (group_key(row["input"]), group_key(row["output"]))
        for records in splits.values()
        for row in records
    ]
    if len(set(all_pairs)) != len(all_pairs) or not all(q and a for q, a in all_pairs):
        raise ValueError("Prepared pairs are empty or duplicated.")
    seen_questions = set()
    seen_answers = set()
    for split_name, records in splits.items():
        questions = {group_key(record["input"]) for record in records}
        answers = {group_key(record["output"]) for record in records}
        if questions & seen_questions or answers & seen_answers:
            raise ValueError("Question or answer groups cross prepared splits.")
        seen_questions.update(questions)
        seen_answers.update(answers)
    for row in annotations:
        if row["split"] != "train":
            continue
        previous = set(question_splits[group_key(row["original_question"])])
        previous.update(question_splits[group_key(row["question"])])
        previous.update(answer_splits[group_key(row["output"])])
        if previous & {"validation", "test"}:
            raise ValueError("An original held-out group entered training.")


def write_split_accounting(destination, annotations, previous_candidates, previous_splits):
    old_rows = {
        (group_key(row["input"]), group_key(row["output"])): row["original_row"]
        for row in previous_candidates
    }
    new_memberships = {str(row["original_row"]): row["split"] for row in annotations}
    accounting = []
    for split_name, records in previous_splits.items():
        for record in records:
            row_number = old_rows[(group_key(record["input"]), group_key(record["output"]))]
            accounting.append({
                "original_row": row_number,
                "previous_split": split_name,
                "v2_status": new_memberships.get(str(row_number), "quarantined_for_review"),
            })
    write_table(
        destination / "previous_split_accounting.csv",
        accounting,
        ["original_row", "previous_split", "v2_status"],
    )


def prepare(source, destination, previous_directory, tokenizer_directory):
    source = Path(source).resolve()
    destination = Path(destination).resolve()
    previous_directory = Path(previous_directory).resolve()
    if destination.exists():
        raise FileExistsError(destination)
    old_manifest = json.loads((previous_directory / "manifest.json").read_text())
    if digest(source) != old_manifest["source_sha256"]:
        raise ValueError("Source differs from the previous preparation.")
    old_splits = json.loads((previous_directory / "splits.json").read_text())
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_directory, local_files_only=True)

    retained = []
    excluded = []
    source_count = 0
    seen_pairs = {}
    for start, end, values, parse_errors, _, raw in read_csv_records(source):
        source_count += 1
        original_question, original_answer = values
        question = fix_question_prefix(clean_text(original_question))
        answer = clean_text(original_answer)
        record = {
            "original_row": start,
            "original_end_row": end,
            "original_question": original_question,
            "question": question,
            "input": question,
            "output": answer,
            "bank": "",
            "scope_evidence": "",
            "review_flags": " | ".join(review_flags(answer)),
            "question_changed": question != original_question,
            "source_url": "",
            "source_date": "not_provided",
            "reason": "",
        }
        problems = list(parse_errors)
        if not group_key(question) or not group_key(answer):
            problems.append("empty_question_or_answer")
        problems.extend(text_problems(original_question + original_answer))
        bank, evidence, scope_problem = scope_question(question, answer)
        record["bank"] = bank or ""
        record["scope_evidence"] = evidence or ""
        if scope_problem:
            problems.append(scope_problem)
        if not problems:
            bank_name = BANKS[bank][0]
            record["input"] = f"ស្ថាប័ន៖ {bank_name}\n\nសំណួរ៖ {question}"
            pair = (group_key(record["input"]), group_key(answer))
            if pair in seen_pairs:
                problems.append(f"duplicate_of_source_row_{seen_pairs[pair]}")
            else:
                seen_pairs[pair] = start
            messages = [
                {"role": "user", "content": record["input"]},
                {"role": "assistant", "content": answer},
            ]
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
            record["tokens"] = len(tokenizer.encode(text, add_special_tokens=False))
            if record["tokens"] > 2048:
                problems.append("over_2048_formatted_tokens")
        if problems:
            record["reason"] = " | ".join(sorted(set(problems)))
            excluded.append(record)
        else:
            retained.append(record)

    answers = defaultdict(set)
    for row in retained:
        answers[group_key(row["input"])].add(group_key(row["output"]))
    conflicts = {question for question, values in answers.items() if len(values) > 1}
    eligible = []
    for row in retained:
        if group_key(row["input"]) in conflicts:
            row["reason"] = "conflicting_answers_after_institution_scoping"
            excluded.append(row)
        else:
            eligible.append(row)

    splits, annotations, crossing = assign_frozen_splits(eligible, old_splits)
    excluded.extend(crossing)
    validate_prepared(splits, annotations, old_splits)
    destination.mkdir(parents=True)
    candidate_rows = [
        {name: row[name] for name in ("input", "output", "original_row")}
        for row in annotations
    ]
    write_table(destination / "training_candidate.csv", candidate_rows, ["input", "output", "original_row"])
    annotation_columns = [
        "original_row", "bank", "scope_evidence", "review_flags", "source_url", "source_date",
        "split", "split_origin", "tokens", "question_changed", "original_question", "question", "input", "output",
    ]
    write_table(destination / "annotations.csv", [
        {name: row.get(name, "") for name in annotation_columns} for row in annotations
    ], annotation_columns)
    review_columns = [
        "original_row", "original_end_row", "reason", "bank", "scope_evidence", "review_flags",
        "source_url", "source_date", "original_question", "question", "output",
    ]
    write_table(destination / "needs_review.csv", [
        {name: row.get(name, "") for name in review_columns} for row in excluded
    ], review_columns)
    write_json(destination / "splits.json", splits)
    write_json(destination / "previous_splits.json", old_splits)

    previous_candidates = read_table(previous_directory / "dataasilida_training_candidate.csv")
    write_split_accounting(destination, annotations, previous_candidates, old_splits)
    old_ids = {int(row["original_row"]) for row in previous_candidates}
    restored = [row["original_row"] for row in annotations if row["original_row"] not in old_ids]
    counts = Counter(reason for row in excluded for reason in row["reason"].split(" | "))
    manifest = {
        "policy": POLICY,
        "scope": "multi_institution_banking_qa",
        "source_path": str(source),
        "source_sha256": digest(source),
        "previous_preparation_manifest_sha256": digest(previous_directory / "manifest.json"),
        "previous_splits_sha256": digest(previous_directory / "splits.json"),
        "preparation_script_sha256": digest(__file__),
        "source_records": source_count,
        "training_candidates": len(annotations),
        "review_rows": len(excluded),
        "restored_source_rows": restored,
        "retained_institution_counts": dict(Counter(row["bank"] for row in annotations)),
        "scope_evidence_counts": dict(Counter(row["scope_evidence"] for row in annotations)),
        "split_sizes": {name: len(records) for name, records in splits.items()},
        "review_reasons": dict(counts),
        "original_heldout_groups_in_training": 0,
        "formatted_token_range": [min(row["tokens"] for row in annotations), max(row["tokens"] for row in annotations)],
        "factual_status": "supplied_source_not_verified_as_current; flags_are_not_factual_errors",
        "comparison_note": "New eligible subset and institution-prefixed inputs; requires a fresh baseline. Do not directly compare with old test scores.",
        "files": {file.name: digest(file) for file in destination.iterdir() if file.is_file()},
    }
    if source_count != len(annotations) + len(excluded):
        raise ValueError("Source row accounting failed.")
    write_json(destination / "manifest.json", manifest)
    print(json.dumps({name: manifest[name] for name in (
        "source_records", "training_candidates", "review_rows", "split_sizes",
        "retained_institution_counts", "scope_evidence_counts", "review_reasons", "formatted_token_range"
    )}, ensure_ascii=False, indent=2))
    print("Restored previously excluded rows:", len(restored))
    return manifest


def load_prepared_v2(directory, source, banking_audit=True):
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text())
    if manifest.get("policy") != POLICY or not banking_audit:
        raise ValueError("Wrong preparation policy selected.")
    if digest(source) != manifest["source_sha256"]:
        raise ValueError("The original source changed; prepare a new version.")
    for name, expected in manifest["files"].items():
        if digest(directory / name) != expected:
            raise ValueError(f"Prepared file changed: {name}")
    splits = json.loads((directory / "splits.json").read_text())
    annotations = read_table(directory / "annotations.csv")
    previous_splits = json.loads((directory / "previous_splits.json").read_text())
    validate_prepared(splits, annotations, previous_splits)
    for split_name, records in splits.items():
        declared = Counter(
            (row["input"], row["output"])
            for row in annotations if row["split"] == split_name
        )
        actual_split = Counter((row["input"], row["output"]) for row in records)
        if declared != actual_split:
            raise ValueError(f"Split annotations disagree with records: {split_name}")
    expected = Counter((row["input"], row["output"]) for row in annotations)
    actual = Counter((row["input"], row["output"]) for records in splits.values() for row in records)
    candidates = Counter((row["input"], row["output"]) for row in read_table(directory / "training_candidate.csv"))
    if expected != actual or expected != candidates or any(count != 1 for count in actual.values()):
        raise ValueError("Prepared records differ between files.")
    return splits, manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("previous_directory", type=Path)
    parser.add_argument("tokenizer_directory", type=Path)
    arguments = parser.parse_args()
    prepare(arguments.source, arguments.destination, arguments.previous_directory, arguments.tokenizer_directory)
