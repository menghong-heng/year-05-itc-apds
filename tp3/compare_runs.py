"""Export measured run results to a comparison CSV and Notion-ready reports."""
import argparse
import csv
import json
from pathlib import Path


def summarize_run(results):
    """Extract the same measurements from each completed run."""
    settings = results["settings"]
    scores = results["scores"]

    return {
        "run": results["run"],
        "data_sha256": results["data_sha256"],
        "split_sha256": results["split_sha256"],
        "steps": settings["steps"],
        "learning_rate": settings["lr"],
        "best_validation_loss": results["best_validation_loss"],
        "before_chrf": scores["before"]["chrf"],
        "after_chrf": scores["after"]["chrf"],
        "after_exact_matches": scores["after"]["exact_matches"],
        "evaluation_examples": results["evaluation_examples"],
        "runtime_seconds": results["runtime_seconds"],
        "peak_reserved_gb": results["peak_reserved_gb"],
    }


def write_run_report(run_directory, results, summary):
    """Save measurements and settings without interpreting the results."""
    lines = [
        f"# {results['run']}",
        "",
        "| Measure | Value |",
        "| --- | --- |",
    ]

    for measure, value in summary.items():
        lines.append(f"| {measure} | {value} |")

    for title, values in (
        ("Training settings", results["settings"]),
        ("Environment", results["environment"]),
    ):
        lines.extend([
            "",
            f"## {title}",
            "",
            "```json",
            json.dumps(values, indent=2),
            "```",
        ])

    lines.extend([
        "",
        f"Best checkpoint: `{results['best_checkpoint']}`",
        "",
        "Loss chart: `loss.png`.",
        "Predictions: `predictions.csv`.",
        "Saved adapter: `adapter/`.",
    ])

    report_path = run_directory / "notion_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_comparison(output_directory, summaries):
    """Write one CSV row per completed run."""
    comparison_path = output_directory / "comparison.csv"

    with comparison_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)


def build_comparison(output_dir):
    """Collect existing run files and export their recorded measurements."""
    output_directory = Path(output_dir)
    summaries = []

    for results_path in sorted(output_directory.glob("*/results.json")):
        results = json.loads(results_path.read_text(encoding="utf-8"))
        summary = summarize_run(results)
        summaries.append(summary)
        write_run_report(results_path.parent, results, summary)

    if summaries:
        write_comparison(output_directory, summaries)

    return summaries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output_dir",
        nargs="?",
        type=Path,
        default=Path(__file__).parent / "outputs",
    )
    arguments = parser.parse_args()
    summaries = build_comparison(arguments.output_dir)
    print(f"{len(summaries)} completed runs indexed.")


if __name__ == "__main__":
    main()
