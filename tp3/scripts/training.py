"""Shared Gemma 3 training and evaluation for local Jupyter and Colab."""

from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import unicodedata

from .prepare_data import key, load_prepared
from .prepare_banking_v2 import load_prepared_v2

EXPERIMENTS = {
    "banking_v2_2epochs": ("dataasilida_cleaned.csv", "banking_v2", 2),
    "banking_v2_4epochs": ("dataasilida_cleaned.csv", "banking_v2", 4),
    "acleda_2epochs": ("dataasilida_cleaned.csv", "acleda", 2),
    "khmerqa_2epochs": ("khmer_wikipedia_qa.csv", "khmerqa", 2),
    "acleda_4epochs": ("dataasilida_cleaned.csv", "acleda", 4),
    "acleda_lr5e5_2epochs": ("dataasilida_cleaned.csv", "acleda", 2),
}

MODEL_NAME = "unsloth/gemma-3-4b-it-unsloth-bnb-4bit"
MAX_SEQ_LENGTH = 2048
LEARNING_RATE = 2e-4
BATCH_SIZE = 1
ACCUMULATION_STEPS = 8
EVAL_STEPS = 10
SEED = 3407

MAX_NEW_TOKENS = 768
REPETITION_PENALTY = 1.1
NO_REPEAT_NGRAM_SIZE = 8

LORA_RANK = 8
LORA_ALPHA = 8


@dataclass
class Run:
    experiment: str
    dataset: str
    path: Path
    epochs: int
    learning_rate: float
    splits: dict
    manifest: dict
    source_hash: str
    split_hash: str


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def prepare_run(experiment, output_root="outputs"):
    filename, policy, epochs = EXPERIMENTS[experiment]
    source = Path("data/raw") / filename
    loader = load_prepared_v2 if policy == "banking_v2" else load_prepared
    splits, manifest = loader(Path("data/prepared") / policy, source, banking_audit=policy != "khmerqa")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    path = Path(output_root) / f"{experiment}-{timestamp}"
    path.mkdir(parents=True)
    write_json(path / "cleaning_manifest.json", manifest)
    split_path = path / "splits.json"
    write_json(split_path, splits)
    learning_rate = 5e-5 if experiment == "acleda_lr5e5_2epochs" else LEARNING_RATE
    print("Dataset:", filename)
    print("Split sizes:", {name: len(rows) for name, rows in splits.items()})
    return Run(experiment, filename, path, epochs, learning_rate, splits, manifest,
               hashlib.sha256(source.read_bytes()).hexdigest(),
               hashlib.sha256(split_path.read_bytes()).hexdigest())


def load_model():
    from unsloth import FastModel
    import torch

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA unavailable. Select a GPU runtime or check the local NVIDIA driver.")
    print("GPU:", torch.cuda.get_device_name(0))
    print("PyTorch:", torch.__version__, "CUDA:", torch.version.cuda)


    model, tokenizer = FastModel.from_pretrained(
        model_name=MODEL_NAME,
        max_seq_length=MAX_SEQ_LENGTH,
        load_in_4bit=True,
        load_in_8bit=False,
        full_finetuning=False,
    )
    from unsloth.chat_templates import get_chat_template
    tokenizer = get_chat_template(
        tokenizer,
        chat_template="gemma-3",
    )
    return model, tokenizer


def tokenize_splits(splits, tokenizer):
    from datasets import Dataset, DatasetDict

    text_tokenizer = getattr(tokenizer, "tokenizer", tokenizer)
    ASSISTANT_PREFIX = "<start_of_turn>model\n"
    END_OF_TURN = "<end_of_turn>"


    def formatting_prompts_func(example):
        user = {"role": "user", "content": example["input"]}
        assistant = {"role": "assistant", "content": example["output"]}
        prompt = tokenizer.apply_chat_template([user], add_generation_prompt=True, tokenize=False)
        text = tokenizer.apply_chat_template(
            [user, assistant], add_generation_prompt=False, tokenize=False
        )
        answer_start = len(prompt)
        answer_end = answer_start + len(example["output"])
        stop_end = answer_end + len(END_OF_TURN)
        if (not prompt.endswith(ASSISTANT_PREFIX)
                or text[:stop_end] != prompt + example["output"] + END_OF_TURN
                or text[stop_end:].strip()):
            raise ValueError(f"Unexpected Gemma 3 chat template for {example['input']!r}")

        encoded = text_tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
        input_ids = encoded["input_ids"]
        offsets = encoded["offset_mapping"]
        if len(input_ids) > MAX_SEQ_LENGTH:
            raise ValueError(f"{len(input_ids)} tokens exceeds {MAX_SEQ_LENGTH}: {example['input']!r}")
        # Offsets come from the full text. Separate tokenization of the answer can
        # change its first token when whitespace merges at the template boundary.
        labels = [-100] * len(input_ids)
        for index, (start, end) in enumerate(offsets):
            if start < stop_end and end > answer_start:
                if text[start:answer_start].strip() or text[stop_end:end].strip():
                    raise ValueError("A token crosses the assistant turn boundary")
                labels[index] = input_ids[index]
        stop_id = text_tokenizer.convert_tokens_to_ids(END_OF_TURN)
        supervised = [label for label in labels if label != -100]
        if len(supervised) < 2 or supervised[-1] != stop_id or stop_id == text_tokenizer.unk_token_id:
            raise ValueError(f"Missing supervised answer or end-of-turn token: {example['input']!r}")
        return {"text": text, "input_ids": input_ids, "labels": labels}


    dataset = DatasetDict({name: Dataset.from_list(rows) for name, rows in splits.items()})
    return dataset.map(formatting_prompts_func)


def unexpected_scripts(text):
    scripts = set()
    for character in text:
        if not character.isalpha():
            continue
        if "\u1780" <= character <= "\u17ff":
            continue
        name = unicodedata.name(character, "")
        if name.startswith("LATIN "):
            continue
        scripts.add(name.split()[0] if name else "UNKNOWN")
    return sorted(scripts)




def generate_answers(model, tokenizer, rows):
    from unsloth import FastModel
    import torch

    text_tokenizer = getattr(tokenizer, "tokenizer", tokenizer)
    FastModel.for_inference(model)
    stop_ids = [
        text_tokenizer.eos_token_id,
        text_tokenizer.convert_tokens_to_ids("<end_of_turn>"),
    ]
    stop_ids = sorted({
        token_id
        for token_id in stop_ids
        if token_id is not None and token_id != text_tokenizer.unk_token_id
    })


    @torch.inference_mode()
    def answer(question):
        messages = [{"role": "user", "content": question}]
        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = text_tokenizer(
            prompt,
            return_tensors="pt",
            add_special_tokens=False,
        ).to("cuda")

        input_length = inputs["input_ids"].shape[1]
        token_budget = min(MAX_NEW_TOKENS, MAX_SEQ_LENGTH - input_length)
        if token_budget <= 0:
            raise ValueError("The question leaves no space for an answer.")

        output = model.generate(
            **inputs,
            max_new_tokens=token_budget,
            do_sample=False,
            repetition_penalty=REPETITION_PENALTY,
            no_repeat_ngram_size=NO_REPEAT_NGRAM_SIZE,
            eos_token_id=stop_ids,
            pad_token_id=text_tokenizer.pad_token_id,
        )
        generated_ids = output[0, input_length:]
        text = text_tokenizer.decode(
            generated_ids,
            skip_special_tokens=True,
        ).strip()

        ended_turn = (
            len(generated_ids) > 0
            and generated_ids[-1].item() in stop_ids
        )
        hit_limit = len(generated_ids) >= token_budget and not ended_turn

        if hit_limit:
            stop_reason = "generation_limit"
        elif ended_turn:
            stop_reason = "end_of_turn"
        else:
            stop_reason = "other"

        return {
            "text": text,
            "generated_tokens": len(generated_ids),
            "token_budget": token_budget,
            "hit_token_limit": hit_limit,
            "stop_reason": stop_reason,
            "unexpected_scripts": unexpected_scripts(text),
        }

    return [answer(row["input"]) for row in rows]


def build_trainer(run, model, tokenizer, dataset, *, track=False):
    from unsloth import FastModel

    FastModel.for_training(model)
    model = FastModel.get_peft_model(
        model,
        finetune_vision_layers=False,
        finetune_language_layers=True,
        finetune_attention_modules=True,
        finetune_mlp_modules=True,
        r=LORA_RANK,
        lora_alpha=LORA_ALPHA,
        lora_dropout=0,
        bias="none",
        random_state=SEED,
    )

    from trl import SFTTrainer, SFTConfig
    from unsloth import is_bfloat16_supported

    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        args=SFTConfig(
            dataset_text_field="text",
            dataset_kwargs={"skip_prepare_dataset": True},
            max_length=MAX_SEQ_LENGTH,
            dataset_num_proc=1,
            packing=False,
            per_device_train_batch_size=BATCH_SIZE,
            per_device_eval_batch_size=1,
            gradient_accumulation_steps=ACCUMULATION_STEPS,
            warmup_steps=5,
            num_train_epochs=run.epochs,
            learning_rate=run.learning_rate,
            fp16=False,
            bf16=is_bfloat16_supported(),
            logging_steps=1,
            eval_strategy="steps",
            eval_steps=EVAL_STEPS,
            prediction_loss_only=True,
            save_strategy="steps",
            save_steps=EVAL_STEPS,
            save_total_limit=2,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            optim="adamw_8bit",
            weight_decay=0.01,
            lr_scheduler_type="linear",
            seed=SEED,
            output_dir=str(run.path / "checkpoints"),
            report_to="wandb" if track else "none",
            run_name=run.path.name,
        ),
    )

    # Verify that the trainer and collator preserve every prepared assistant label.
    for name, split in (("train", trainer.train_dataset), ("validation", trainer.eval_dataset)):
        columns = ["input_ids", "labels"]
        expected = dataset[name].select_columns(columns)
        actual = split.select_columns(columns)
        if len(expected) != len(actual) or any(a != b for a, b in zip(expected, actual)):
            raise ValueError(f"{name}: SFTTrainer changed token IDs or assistant labels")
        # Use different lengths so the check also covers masked padding.
        short = min(actual, key=lambda row: len(row["input_ids"]))
        long = max(actual, key=lambda row: len(row["input_ids"]))
        rows = [short, long]
        batch = trainer.data_collator(rows)
        for i, row in enumerate(rows):
            active = batch["attention_mask"][i].bool()
            if (batch["input_ids"][i][active].tolist() != row["input_ids"]
                    or batch["labels"][i][active].tolist() != row["labels"]
                    or (batch["labels"][i][~active] != -100).any()
                    or len(active) > MAX_SEQ_LENGTH):
                raise ValueError(f"{name}: the data collator changed assistant labels or padding")
        print(f"{name}: verified assistant-only labels for {len(actual)} examples and checked padding")

    return trainer


def evaluate_answers(rows, before, after):
    from sacrebleu.metrics import CHRF
    from .prediction_display import display_predictions

    results = []

    for row, base_generation, tuned_generation in zip(rows, before, after, strict=True):
        result = {
            **row,
            "before": base_generation["text"],
            "after": tuned_generation["text"],
        }

        for stage, generation in (
            ("before", base_generation),
            ("after", tuned_generation),
        ):
            result[f"{stage}_exact_match"] = key(generation["text"]) == key(row["output"])
            result[f"{stage}_generated_tokens"] = generation["generated_tokens"]
            result[f"{stage}_token_budget"] = generation["token_budget"]
            result[f"{stage}_hit_token_limit"] = generation["hit_token_limit"]
            result[f"{stage}_stop_reason"] = generation["stop_reason"]
            result[f"{stage}_unexpected_scripts"] = generation["unexpected_scripts"]

        results.append(result)

    references = [key(row["output"]) for row in results]
    chrf = CHRF()
    scores = {}

    for stage in ("before", "after"):
        predictions = [key(row[stage]) for row in results]
        scores[stage] = {
            "chrf": chrf.corpus_score(predictions, [references]).score,
            "exact_matches": sum(row[f"{stage}_exact_match"] for row in results),
            "token_limit_hits": sum(row[f"{stage}_hit_token_limit"] for row in results),
            "unexpected_script_answers": sum(bool(row[f"{stage}_unexpected_scripts"]) for row in results),
        }

    display_predictions(results, scores)

    return results, scores


def plot_losses(run, trainer):
    import matplotlib.pyplot as plt

    history = trainer.state.log_history
    train_loss = []
    val_loss = []

    for record in history:
        step = record.get("step")

        if "loss" in record:
            train_loss.append((step, record["loss"]))

        if "eval_loss" in record:
            val_loss.append((step, record["eval_loss"]))

    plt.figure()
    train_steps, train_values = zip(*train_loss)


    plt.plot(train_steps, train_values, label="Training loss")
    if val_loss:
        plt.plot(*zip(*val_loss), label="Validation loss", marker=".")
    plt.xlabel("Optimizer step")
    plt.ylabel("Loss")
    plt.title(run.experiment)
    plt.legend()
    plt.savefig(run.path / "loss.png", dpi=160, bbox_inches="tight")
    plt.show()


    return train_loss, val_loss


def save_run(run, trainer, tokenizer, stats, results, scores, tracking=None):
    import pandas as pd
    import torch

    train_loss, val_loss = plot_losses(run, trainer)
    settings = {
        "seed": SEED,
        "lr": run.learning_rate,
        "batch": BATCH_SIZE,
        "accumulation": ACCUMULATION_STEPS,
        "duration_control": "epochs",
        "num_train_epochs": run.epochs,
        "steps": trainer.state.global_step,
        "completed_epochs": trainer.state.epoch,
        "eval_steps": EVAL_STEPS,
        "model": MODEL_NAME,
        "max_seq_length": MAX_SEQ_LENGTH,
        "lora_rank": LORA_RANK,
        "lora_alpha": LORA_ALPHA,
        "experiment": run.experiment,
        "dataset": run.dataset,
        "banking_audit": run.experiment != "khmerqa_2epochs",
        "preparation_policy": run.manifest.get("policy", "legacy"),
        "evaluation_limit": None,
        "generation": {
            "max_new_tokens": MAX_NEW_TOKENS,
            "repetition_penalty": REPETITION_PENALTY,
            "no_repeat_ngram_size": NO_REPEAT_NGRAM_SIZE,
            "do_sample": False,
            "context_limit": MAX_SEQ_LENGTH,
        },
    }
    report = run.path / "results.json"
    run_results = {
        "run": run.path.name,
        "settings": settings,
        "optimizer_steps": trainer.state.global_step,
        "completed_epochs": trainer.state.epoch,
        "data_sha256": run.source_hash,
        "split_sha256": run.split_hash,
        "split_sizes": {name: len(rows) for name, rows in run.splits.items()},
        "evaluation_examples": len(results),
        "environment": {
            name: version(name)
            for name in ("unsloth", "transformers", "trl", "torch")
        },
        "gpu": torch.cuda.get_device_name(0),
        "runtime_seconds": stats.metrics["train_runtime"],
        "peak_reserved_gb": round(torch.cuda.max_memory_reserved() / 1024**3, 3),
        "best_validation_loss": trainer.state.best_metric,
        "train_loss": train_loss,
        "validation_loss": val_loss,
        "best_checkpoint": trainer.state.best_model_checkpoint,
        "scores": scores,
        "results": results,
        "wandb_url": tracking.url if tracking else None,
    }

    report_content = json.dumps(run_results, ensure_ascii=False, indent=2)
    report.write_text(report_content, encoding="utf-8")

    pd.DataFrame(results).to_csv(run.path / "predictions.csv", index=False)
    adapter_path = run.path / "adapter"
    trainer.save_model(str(adapter_path))
    tokenizer.save_pretrained(str(adapter_path))
    print("Adapter and results saved.")

    if tracking:
        tracking.summary.update({
            f"heldout/{stage}/{metric}": value
            for stage, metrics in scores.items()
            for metric, value in metrics.items()
        })
        tracking.summary["heldout/examples"] = len(results)
        print("W&B:", tracking.url)
    print("Saved:", run.path)

@contextmanager
def track_run(run, project):
    """Log trainer metrics and aggregate scores only."""
    if not project:
        yield None
        return

    os.environ["WANDB_LOG_MODEL"] = "false"
    os.environ["WANDB_WATCH"] = "false"
    os.environ["WANDB_DISABLE_CODE"] = "true"
    os.environ["WANDB_DISABLE_GIT"] = "true"
    import wandb

    with wandb.init(project=project, name=run.path.name, dir=str(run.path),
                    config={"experiment": run.experiment, "dataset": run.dataset,
                            "epochs": run.epochs, "data_sha256": run.source_hash,
                            "split_sha256": run.split_hash},
                    settings=wandb.Settings(save_code=False)) as tracking:
        yield tracking
