import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def generate_nutrition_tip(
    age: int,
    weight: float,
    goal: str,
    intensity: str
):
    prompt = f"""
Give a concise nutrition and recovery tip for a fitness user.

User:
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Give practical advice about:
- Protein
- Hydration
- Recovery
- General nutrition

Keep it concise and easy to understand.
Do not provide a full meal plan.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text