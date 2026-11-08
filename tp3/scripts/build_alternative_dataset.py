"""Download a pinned Khmer QA source and build a cleaned 303-example subset."""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import random
import re
import urllib.request
import unicodedata

from transformers import AutoTokenizer
from .prepare_data import CONTROL_TOKEN, clean_text, group_key, prepare

REPOSITORY = "sengtha/khmer-qa"
REVISION = "3ca26dc817cae20dc4c574e7027b581ec7cb73ae"
SOURCE_URL = f"https://huggingface.co/datasets/{REPOSITORY}/resolve/{REVISION}/data.json"
SEED = 3407
SAMPLE_SIZE = 303


def build(project, tokenizer_directory, raw_file=None):
    project = Path(project)
    (project / "data" / "raw").mkdir(parents=True, exist_ok=True)
    csv_path = project / "data" / "raw" / "khmer_wikipedia_qa.csv"
    prepared_path = project / "data" / "prepared" / "khmerqa"
    source_directory = project / "data" / "sources" / "khmerqa"
    if csv_path.exists() or prepared_path.exists():
        raise FileExistsError("Alternative dataset already exists. Use a new project directory to rebuild.")
    source_directory.mkdir(parents=True, exist_ok=True)

    if raw_file is None:
        with urllib.request.urlopen(SOURCE_URL, timeout=60) as response:
            source_bytes = response.read()
    else:
        source_bytes = Path(raw_file).read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    raw_path = source_directory / "data.json"
    raw_path.write_bytes(source_bytes)
    rows = json.loads(source_bytes)

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_directory, local_files_only=True)
    source_rows = list(enumerate(rows, start=1))
    random.Random(SEED).shuffle(source_rows)
    selected = []
    rejected = Counter()
    seen = {name: set() for name in ("context", "question", "answer")}
    selected_sources = []

    for source_row, record in source_rows:
        if len(selected) == SAMPLE_SIZE:
            break
        if record.get("type") != "extract":
            rejected["not_extractive"] += 1
            continue
        values = {}
        for field in seen:
            value = record.get(field)
            values[field] = clean_text(value) if isinstance(value, str) else ""
        if not all(values.values()):
            rejected["missing_text"] += 1
            continue
        context = values["context"]
        question = values["question"]
        answer = values["answer"]
        if not question.startswith("តើ"):
            rejected["question_format"] += 1
            continue
        if not all(re.search(r"[\u1780-\u17ff]", value) for value in values.values()):
            rejected["missing_khmer"] += 1
            continue
        if any(
            "\ufffd" in text
            or CONTROL_TOKEN.search(text)
            or any(unicodedata.category(char) == "Cc" and not char.isspace() for char in text)
            for text in values.values()
        ):
            rejected["reserved_token"] += 1
            continue
        if group_key(answer) not in group_key(context):
            rejected["answer_not_in_context"] += 1
            continue
        if any(group_key(values[field]) in seen[field] for field in seen):
            rejected["repeated_context_question_or_answer"] += 1
            continue

        prompt = f"បរិបទ៖\n{context}\n\nសំណួរ៖ {question}"
        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": answer},
        ]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        token_count = len(tokenizer.encode(text, add_special_tokens=False))
        if token_count > 2048:
            rejected["over_2048_tokens"] += 1
            continue

        selected.append({"input": prompt, "output": answer})
        selected_sources.append({"source_row": source_row, "tokens": token_count})
        for field in seen:
            seen[field].add(group_key(values[field]))

    if len(selected) != SAMPLE_SIZE:
        raise ValueError(f"Only {len(selected)} acceptable examples; expected {SAMPLE_SIZE}.")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("input", "output"))
        writer.writeheader()
        writer.writerows(selected)

    manifest = prepare(csv_path, prepared_path, banking_audit=False)
    assert manifest["training_candidates"] == SAMPLE_SIZE
    provenance = {
        "repository": REPOSITORY,
        "revision": REVISION,
        "source_url": SOURCE_URL,
        "source_sha256": source_hash,
        "license": "CC-BY-SA-4.0",
        "attribution": "sengtha / iAny (E-KHMER Technology); Khmer Wikipedia contributors",
        "origin": "Qwen2.5-generated QA over Khmer Wikipedia 20231101.km passages; not human-verified",
        "seed": SEED,
        "selection": "303 extractive Khmer examples, unique context/question/answer groups, answer contained in context, <=2048 Gemma tokens",
        "source_rows": len(rows),
        "selected": selected_sources,
        "rejections_before_sample_complete": dict(rejected),
        "tokenizer_directory": str(tokenizer_directory),
    }
    (source_directory / "provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Alternative CSV:", csv_path)
    print("Token range:", min(row['tokens'] for row in selected_sources), max(row['tokens'] for row in selected_sources))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("tokenizer_directory", type=Path)
    parser.add_argument("--raw-file", type=Path)
    args = parser.parse_args()
    build(args.project, args.tokenizer_directory, args.raw_file)
