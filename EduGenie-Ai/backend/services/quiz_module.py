import json
import re
from typing import Any
from backend.gemini_client import generate_text


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]
    return text


def validate_quiz(data: Any) -> list[dict]:
    if not isinstance(data, list):
        raise ValueError("Quiz response must be a JSON list.")

    cleaned = []
    for item in data:
        if not isinstance(item, dict):
            continue
        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", "")).strip()

        if not question or not isinstance(options, list) or len(options) != 4 or not answer:
            continue

        options = [str(x).strip() for x in options]
        if answer not in options:
            # Accept a numeric answer such as 1-4 and convert it.
            if answer.isdigit() and 1 <= int(answer) <= 4:
                answer = options[int(answer) - 1]
            else:
                continue

        cleaned.append({
            "question": question,
            "options": options,
            "answer": answer,
            "explanation": str(item.get("explanation", "")).strip(),
        })

    if not cleaned:
        raise ValueError("No valid quiz questions were returned.")
    return cleaned


async def generate_quiz(text: str, count: int = 3) -> list[dict]:
    prompt = f"""
Create exactly {count} multiple-choice questions from the educational text below.

Return ONLY valid JSON. Do not use Markdown.
The JSON must be an array. Every item must have:
- "question": string
- "options": exactly four strings
- "answer": exactly one option string
- "explanation": short explanation

Make questions relevant to the supplied text and make incorrect options plausible.

Educational text:
{text}
"""
    raw = await generate_text(prompt, temperature=0.4, max_output_tokens=3000)
    data = json.loads(clean_json_block(raw))
    return validate_quiz(data)
