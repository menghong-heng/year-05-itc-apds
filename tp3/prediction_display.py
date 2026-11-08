"""Compact notebook display for recorded predictions; no metric interpretation."""
from html import escape

from IPython.display import HTML, display


def answer_block(title, text):
    content = escape(str(text))
    return (
        f'<h4>{escape(title)}</h4>'
        '<div style="white-space:pre-wrap;overflow-wrap:anywhere;'
        'max-height:22em;overflow:auto;line-height:1.7;padding:0.75em;'
        'border:1px solid #8886;border-radius:4px;text-align:left">'
        f'{content}</div>'
    )


def display_predictions(results, scores):
    """Show a score table followed by expandable, vertically stacked answers."""
    if not results:
        raise ValueError("No predictions to display.")

    rows = []
    exact_rows = []
    names = {"before": "Base model", "after": "Fine-tuned model"}

    for stage in ("before", "after"):
        score = scores[stage]
        limit_hits = score.get("token_limit_hits", "Not recorded")
        script_answers = score.get("unexpected_script_answers", "Not recorded")
        rows.append(
            f'<tr><td>{names[stage]}</td>'
            f'<td>{score["chrf"]:.2f}</td>'
            f'<td>{limit_hits}</td><td>{script_answers}</td></tr>'
        )
        exact_rows.append(
            f'<tr><td>{names[stage]}</td>'
            f'<td>{score["exact_matches"]} / {len(results)}</td></tr>'
        )

    change = scores["after"]["chrf"] - scores["before"]["chrf"]
    content = [
        '<div style="max-width:1000px;text-align:left">',
        '<table><thead><tr><th>Model</th><th>chrF / 100</th>'
        '<th>Token-limit hits</th><th>Unexpected-script answers</th>'
        '</tr></thead><tbody>',
        ''.join(rows),
        '</tbody></table>',
        f'<p>chrF change: {change:+.2f} points · {len(results)} test examples</p>',
        '<details><summary style="cursor:pointer">Exact-match check</summary>'
        '<p>Literal reference matches; paraphrases can score zero.</p>'
        '<table><thead><tr><th>Model</th><th>Exact matches</th></tr></thead><tbody>',
        ''.join(exact_rows),
        '</tbody></table></details>',
        '<p>Script checks allow Khmer and Latin letters. '
        'They do not identify every case of language mixing or check factual correctness.</p>',
        '<p>Open a group, then select a question to compare answers.</p>',
    ]

    for number, result in enumerate(results, start=1):
        if (number - 1) % 8 == 0:
            last = min(number + 7, len(results))
            content.append(
                f'<details><summary style="cursor:pointer;padding:0.5em">'
                f'Questions {number}–{last}</summary>'
            )
        prompt = result['input']
        question_text = prompt.split("\n\nសំណួរ៖")[-1]
        question = escape(question_text)
        content.append(
            '<details style="margin:0.8em 0;padding:0.8em;'
            'border:1px solid #8886;border-radius:4px">'
            f'<summary style="cursor:pointer;line-height:1.6">'
            f'<strong>{number}.</strong> {question}</summary>'
        )
        if prompt != question_text:
            content.append(answer_block('Input context', prompt.split("\n\nសំណួរ៖")[0]))
        content.append(answer_block('Reference', result['output']))
        for stage in ("before", "after"):
            content.append(answer_block(names[stage], result[stage]))
            details = []
            if f"{stage}_generated_tokens" in result:
                count = result[f"{stage}_generated_tokens"]
                budget = result[f"{stage}_token_budget"]
                details.append(f"Generated tokens: {count} / {budget}")
                reason = result[f"{stage}_stop_reason"].replace("_", " ")
                details.append(f"Stop: {reason}")
            scripts = result.get(f"{stage}_unexpected_scripts", [])
            if scripts:
                details.append("Unexpected scripts: " + ", ".join(scripts))
            if details:
                content.append('<p>' + escape(" · ".join(details)) + '</p>')
        content.append('</details>')
        if number % 8 == 0 or number == len(results):
            content.append('</details>')

    content.append('</div>')
    display(HTML(''.join(content)))
