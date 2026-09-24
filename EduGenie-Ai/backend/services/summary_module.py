from backend.gemini_client import generate_text


async def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational passage for quick revision.

Requirements:
- Keep the important facts and ideas.
- Remove repetition and unnecessary wording.
- Use simple language.
- Use headings and bullet points when useful.
- Do not introduce information that is not present in the passage.

Passage:
{text}
"""
    return await generate_text(prompt, temperature=0.2, max_output_tokens=1600)
