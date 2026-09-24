from backend.gemini_client import generate_text


async def explain_topic(topic: str) -> str:
    prompt = f"""
Explain the following educational topic as if you are teaching a beginner.

Topic:
{topic}

Format:
1. Simple definition
2. How it works
3. Easy example
4. Key points to remember

Use simple language and avoid unnecessary jargon.
"""
    return await generate_text(prompt, temperature=0.25, max_output_tokens=1200)
