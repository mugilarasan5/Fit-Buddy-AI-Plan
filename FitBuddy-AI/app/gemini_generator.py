import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def generate_workout_gemini(
    age: int,
    weight: float,
    goal: str,
    intensity: str
):
    prompt = f"""
Create a personalized 7-day workout plan.

User:
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Include:
- 7 days
- Warm-up
- Main exercises
- Sets and repetitions
- Rest/recovery
- Cooldown

Make the plan practical and clear.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text