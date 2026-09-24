from backend.gemini_client import generate_text


async def get_learning_recommendations(
    topic: str, level: str = "beginner", weekly_hours: int = 5
) -> str:
    prompt = f"""
Create a personalized learning path for the topic "{topic}".

Learner level: {level}
Available study time: {weekly_hours} hours per week

Organize the path from beginner to advanced where appropriate.
Include:
1. Learning stages
2. Concepts to study at each stage
3. Suggested timeline
4. Practice ideas
5. Types of resources to use (videos, articles, books, documentation)
6. A simple weekly routine
7. A milestone/checkpoint for each stage

Do not invent specific URLs. Keep the plan practical for a student.
"""
    return await generate_text(prompt, temperature=0.35, max_output_tokens=2400)
