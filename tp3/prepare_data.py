"""Offline dataset inspection and preparation. Uses only the Python standard library."""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from tempfile import NamedTemporaryFile
import csv
import random
import re
import unicodedata

SEED = 3407
QA_COLUMNS = ("input", "output")
CANDIDATE_COLUMNS = (*QA_COLUMNS, "original_row")
REVIEW_COLUMNS = (*CANDIDATE_COLUMNS, "original_end_row", "reasons", "raw_record")

# Match underspecified follow-up questions without guessing the missing product.
PRODUCT_REFERENCE = re.compile(
    r"(?:ឥណទាន|កម្ចី|គណនី|ប័ណ្ណ|កាត|សេវា|ផលិតផល|កម្មវិធី|កិច្ចសន្យា)(?:នេះ|នោះ)"
)
GENERIC_QUESTION = re.compile(
    r"^(?:តើ)?(?:ទំហំឥណទាននិងរយៈពេល|រយៈពេលដាក់ប្រាក់បញ្ញើ|"
    r"ការប្រាក់ទទួលបានដូចម្តេច|ធនាគារផ្តល់ការប្រាក់|ពេលបើកគណនីដំបូង|"
    r"ការស្នើសុំ(?:របាយការណ៍|បិទ)គណនីមានគិត|"
    r"(?:អតិថិជន)?អាចដក(?:សាច់)?ប្រាក់(?:ទាំងអស់ចេញ)?ពីគណនី(?:បញ្ញើ)?បាន|"
    r"(?:ដើម្បី)?បើកគណនី(?:ឯកត្តជន|ជនបរទេស|ក្រុមហ៊ុនឬស្ថាប័ន)បានត្រូវមានឯកសារ|"
    r"មូលប្បទានបត្រមួយក្បាលថ្លៃ|សៀវភៅប្រាក់បញ្ញើមួយក្បាលថ្លៃ|"
    r"(?:ខ្ញុំ)?(?:អាច)?(?:បញ្ឈប់ការប្រើប្រាស់សេវា|បង់ប្រាក់យឺត)|"
    r"រយៈពេលប៉ុន្មានថ្ងៃទើបធនាគារឆ្លើយតប|"
    r"លេខមួយណាដែលអាចទំនាក់ទំនងទៅកាន់ផ្នែកផ្តល់សេវាអតិថិជន)"
)
MONEY_OR_TERMS = re.compile(
    r"[$€៛%]|ដុល្លារ|អឺរ៉ូ|រៀល|(?:usd|khr|eur)\b|"
    r"អត្រាការប្រាក់|កម្រៃ|ថ្លៃសេវា|ពិន័យ|កំណត់|អតិបរមា|អប្បបរមា|"
    r"រយៈពេល|សុពលភាព|ក្នុងមួយថ្ងៃ|ប្រតិបត្តិការ|interest rate|\bfees?\b"
)
DATE_OR_OFFER = re.compile(
    r"(?<!\d)(?:19[5-9]\d|20\d{2}|១៩[៥-៩][០-៩]|២០[០-៩]{2})(?!\d)|"
    r"ប្រូម៉ូសិន|កម្មវិធីពិសេស|\bpromotion\b"
)
FEE_WAIVER = re.compile(r"មិន(?:មាន)?គិត(?:កម្រៃ|ថ្លៃសេវា)|\bno fees?\b")
CONTROL_TOKEN = re.compile(r"<(?:start_of_turn|end_of_turn|bos|eos|pad|unk|start_of_image|end_of_image)>")


def clean_text(text):
    # The source encodes paragraph breaks as literal backslash-n sequences.
    # Keep Khmer word breaks (ZWSP), joiners and diacritics in the training text.
    text = unicodedata.normalize("NFC", text)
    text = text.replace(r"\r\n", "\n").replace(r"\n", "\n")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(" ".join(line.split()) for line in text.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def key(text):
    """Compare answers and questions without changing the stored Khmer text."""
    text = clean_text(text).translate({0x200B: None, 0xFEFF: None})
    return " ".join(text.casefold().split())


def group_key(text):
    """Also ignore Khmer layout spaces and trailing sentence punctuation."""
    text = re.sub(r"(?<=[\u1780-\u17ff]) (?=[\u1780-\u17ff])", "", key(text))
    return text.rstrip(" ?!.？។៕")


def read_csv_records(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        lines = handle.readlines()
    reader = csv.reader(lines, strict=True)
    header = next(reader, [])
    legacy_header = len(header) == 1 and header[0].split(",") == list(QA_COLUMNS)
    columns = list(QA_COLUMNS) if legacy_header else [field.strip().lower() for field in header]
    if len(columns) != len(set(columns)) or not set(QA_COLUMNS).issubset(columns):
        raise ValueError(f"{path}: expected input and output columns, found {header!r}")
    indexes = [columns.index(name) for name in QA_COLUMNS]
    while reader.line_num < len(lines):
        start = reader.line_num + 1
        reasons = []
        recovered = False
        try:
            fields = next(reader)
        except csv.Error:
            fields = []
            reasons.append("malformed_csv_quoting")
        if legacy_header and len(fields) == 1 and fields[0].count(",") == 1:
            fields = fields[0].split(",", 1)
            recovered = True
        if len(fields) != len(columns) and not reasons:
            reasons.append("malformed_field_count" if fields else "empty_record")
        values = [fields[i] if i < len(fields) else "" for i in indexes]
        end = reader.line_num
        yield start, end, values, reasons, recovered, "".join(lines[start - 1:end])


def write_audit_csv(path, columns, rows):
    with NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="", dir=path.parent, delete=False
    ) as handle:
        temporary = Path(handle.name)
        try:
            writer = csv.DictWriter(handle, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
            handle.close()
            temporary.replace(path)
        finally:
            handle.close()
            temporary.unlink(missing_ok=True)


def audit_dataset(path, output_dir=None, banking_audit=True):
    """Keep one copy of each usable pair and quarantine records for review."""
    path = Path(path)
    output_dir = Path(output_dir) if output_dir is not None else path.parent
    candidate_path = output_dir / "dataasilida_training_candidate.csv"
    review_path = output_dir / "dataasilida_needs_review.csv"
    if path.resolve() in {candidate_path.resolve(), review_path.resolve()}:
        raise ValueError("Pass the source CSV, which must be separate from the audit outputs.")
    output_dir.mkdir(parents=True, exist_ok=True)

    records = []
    raw_pairs = {}
    normalized_pairs = {}
    answers_by_question = defaultdict(set)
    answers_by_group = defaultdict(set)
    stats = Counter()
    for start, end, original, reasons, recovered, raw_record in read_csv_records(path):
        stats["source_records"] += 1
        stats["recovered_single_field"] += recovered
        question, answer = map(clean_text, original)
        q_key, a_key = key(question), key(answer)
        q_group, a_group = group_key(question), group_key(answer)
        if not reasons:
            if not q_group:
                reasons.append("missing_or_empty_input")
            if not a_group:
                reasons.append("missing_or_empty_output")
            if any(
                "\ufffd" in value or CONTROL_TOKEN.search(value)
                or any(unicodedata.category(c) == "Cc" and not c.isspace() for c in value)
                for value in original
            ):
                reasons.append("invalid_text_or_reserved_chat_token")
            compact_question = q_group.replace(" ", "")
            if compact_question.startswith("តើ") and compact_question[:16] in compact_question[16:]:
                reasons.append("repeated_question_prefix")
        if reasons:
            stats["invalid_records"] += 1
        else:
            raw_pair = tuple(original)
            normalized_pair = (q_key, a_key)
            if raw_pair in raw_pairs:
                stats["exact_duplicate_pairs"] += 1
                reasons.append(f"exact_duplicate_of_row_{raw_pairs[raw_pair]}")
            elif normalized_pair in normalized_pairs:
                stats["normalized_duplicate_pairs"] += 1
                reasons.append(f"normalized_duplicate_of_row_{normalized_pairs[normalized_pair]}")
            raw_pairs.setdefault(raw_pair, start)
            normalized_pairs.setdefault(normalized_pair, start)
            answers_by_question[q_key].add(a_key)
            answers_by_group[q_group].add(a_group)
        records.append((start, end, original, question, answer, reasons, raw_record))

    conflicts = {q for q, answers in answers_by_question.items() if len(answers) > 1}
    group_conflicts = {q for q, answers in answers_by_group.items() if len(answers) > 1}
    stats["conflicting_question_groups"] = len(conflicts)
    stats["equivalent_question_conflict_groups"] = len(group_conflicts)
    candidates, review = [], []
    for start, end, original, question, answer, reasons, raw_record in records:
        if key(question) in conflicts or group_key(question) in group_conflicts:
            reasons.append("multiple_distinct_answers")
            stats["conflicting_records"] += 1
        q_compact = group_key(question).replace(" ", "")
        if banking_audit and (PRODUCT_REFERENCE.search(q_compact) or GENERIC_QUESTION.search(q_compact)):
            reasons.append("missing_banking_product_context")
            stats["missing_product_context"] += 1
        if banking_audit and re.search(r"ខេប៊ី|ដេហាន|\bkb\s*daehan\b", question + " " + answer, re.IGNORECASE):
            reasons.append("different_bank_kb_daehan")
        a_normalized = group_key(answer)
        if banking_audit and (DATE_OR_OFFER.search(a_normalized) or FEE_WAIVER.search(a_normalized) or (
            re.search(r"\d", a_normalized) and MONEY_OR_TERMS.search(a_normalized)
        )):
            reasons.append("potentially_outdated_financial_information")
            stats["potentially_outdated"] += 1
        if reasons:
            review.append(dict(
                input=original[0], output=original[1], original_row=start,
                original_end_row=end, reasons=" | ".join(reasons),
                raw_record=raw_record if any(
                    reason.startswith(("malformed_", "empty_record")) for reason in reasons
                ) else "",
            ))
        else:
            candidates.append(dict(input=question, output=answer, original_row=start))
    write_audit_csv(candidate_path, CANDIDATE_COLUMNS, candidates)
    write_audit_csv(review_path, REVIEW_COLUMNS, review)
    fields = (
        "source_records", "recovered_single_field", "invalid_records", "exact_duplicate_pairs",
        "normalized_duplicate_pairs", "conflicting_question_groups",
        "equivalent_question_conflict_groups", "conflicting_records",
        "missing_product_context", "potentially_outdated",
    )
    print("Dataset audit:", {**{name: stats[name] for name in fields},
                             "training_candidates": len(candidates), "review_rows": len(review)})
    return candidate_path



def load_splits(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        if tuple(reader.fieldnames or ()) != CANDIDATE_COLUMNS:
            raise ValueError(f"{path}: expected a training-candidate CSV from audit_dataset()")
        records = list(reader)

    # A shared question or answer connects entire groups, including indirect matches.
    # Keep each connected component in exactly one split.
    parents = list(range(len(records)))

    def root(index):
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    first_seen = {}
    seen_pairs = set()
    for index, row in enumerate(records):
        if None in row or not all(row.values()) or not row["original_row"].isdecimal():
            raise ValueError(f"{path}: invalid candidate record at index {index}")
        pair = tuple(key(row[column]) for column in QA_COLUMNS)
        if not all(pair) or pair in seen_pairs:
            raise ValueError(f"{path}: empty field or duplicate at source row {row['original_row']}")
        seen_pairs.add(pair)
        for column in QA_COLUMNS:
            group = (column, group_key(row[column]))
            parents[root(index)] = root(first_seen.setdefault(group, index))

    components = defaultdict(list)
    for index, row in enumerate(records):
        components[root(index)].append({column: row[column] for column in QA_COLUMNS})
    groups = list(components.values())
    if len(groups) < 3:
        raise ValueError(f"{path}: need at least three independent question/answer groups")
    random.Random(SEED).shuffle(groups)
    first = min(max(1, int(len(groups) * .8)), len(groups) - 2)
    second = min(max(first + 1, int(len(groups) * .9)), len(groups) - 1)
    splits = {
        name: [record for group in subset for record in group]
        for name, subset in zip(
            ("train", "validation", "test"),
            (groups[:first], groups[first:second], groups[second:]),
        )
    }
    for column in QA_COLUMNS:
        seen_groups = set()
        for rows in splits.values():
            split_groups = {group_key(row[column]) for row in rows}
            if seen_groups & split_groups:
                raise ValueError(f"{path}: {column} group appears in multiple splits")
            seen_groups.update(split_groups)
    print("Split sizes:", {name: len(rows) for name, rows in splits.items()})
    return splits



def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, data):
    """Save readable UTF-8 JSON, preserving Khmer characters."""
    content = json.dumps(data, ensure_ascii=False, indent=2)
    Path(path).write_text(content, encoding="utf-8")


def validate_candidates(rows):
    """Check normalized, unique examples and reject conflicting questions."""
    pairs = [(key(row["input"]), key(row["output"])) for row in rows]
    assert all(question and answer for question, answer in pairs) and len(set(pairs)) == len(pairs)
    assert all(clean_text(row[c]) == row[c] for row in rows for c in QA_COLUMNS)
    answers = defaultdict(set)
    for row in rows:
        answers[group_key(row["input"])].add(group_key(row["output"]))
    assert all(len(values) == 1 for values in answers.values())


def write_cleaning_report(destination, source_name, candidate_count, review_count, reasons):
    """Write counts and cleaning checks; no model-result interpretation."""
    report = ["# Dataset preparation report", "", f"Source: {source_name}",
              f"Training candidates: {candidate_count}; quarantined records: {review_count}.",
              "", "Checks passed: nonempty normalized fields, unique pairs, no conflicting grouped questions, disjoint question/answer groups across splits.",
              "", "## Review reasons", "", "Counts overlap because a record can have multiple reasons.", ""]
    report += [f"- {reason}: {count}" for reason,count in sorted(reasons.items())]
    report += ["", "## Limits", "", "Automated cleaning does not establish factual accuracy. Financial statements flagged as potentially outdated were quarantined rather than corrected. Review the remaining examples for domain accuracy before drawing conclusions. Token-length and assistant-label checks still run in the notebook after loading the tokenizer."]
    (destination / "cleaning_report.md").write_text("\n".join(report), encoding="utf-8")


def prepare(source, destination, banking_audit=True):
    source = Path(source).resolve()
    destination = Path(destination).resolve()
    if destination.exists():
        raise FileExistsError(f"Prepared directory already exists: {destination}. Use a new directory to preserve prior audits.")
    destination.mkdir(parents=True)
    candidate = audit_dataset(source, destination, banking_audit=banking_audit)
    splits = load_splits(candidate)
    write_json(destination / "splits.json", splits)
    with (destination / "dataasilida_needs_review.csv").open(encoding="utf-8", newline="") as handle:
        review = list(csv.DictReader(handle))
    reasons = Counter(reason for row in review for reason in row["reasons"].split(" | "))
    # Independently check the prepared candidate records and split disjointness.
    with candidate.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    validate_candidates(rows)
    manifest = {
        "source_path": str(source),
        "source_sha256": sha256(source),
        "seed": SEED,
        "banking_audit": banking_audit,
        "training_candidates": len(rows),
        "review_rows": len(review),
        "review_reasons": dict(reasons),
        "split_sizes": {
            name: len(records)
            for name, records in splits.items()
        },
        "files": {
            file.name: sha256(file)
            for file in destination.iterdir()
            if file.is_file()
        },
    }
    write_json(destination / "manifest.json", manifest)
    write_cleaning_report(
        destination,
        source.name,
        len(rows),
        len(review),
        reasons,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return manifest


def load_prepared(directory, source, banking_audit=True):
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if sha256(source) != manifest["source_sha256"] or manifest["banking_audit"] != banking_audit or manifest["seed"] != SEED:
        raise ValueError("Source, cleaning policy or seed changed. Prepare a new version before training.")
    for name, expected in manifest["files"].items():
        if sha256(directory / name) != expected:
            raise ValueError(f"Prepared file changed: {name}. Prepare a new version before training.")
    splits = json.loads((directory / "splits.json").read_text(encoding="utf-8"))
    if splits != load_splits(directory / "dataasilida_training_candidate.csv"):
        raise ValueError("Prepared split records do not match the candidate dataset.")
    return splits, manifest


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--generic", action="store_true", help="Disable banking-specific review rules for the original dataset")
    args = parser.parse_args()
    prepare(args.source, args.destination, banking_audit=not args.generic)
