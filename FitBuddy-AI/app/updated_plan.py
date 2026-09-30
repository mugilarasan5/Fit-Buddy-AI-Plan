from app.gemini_generator import client


def update_workout_plan(original_plan: str, feedback: str):

    prompt = f"""
Update the following workout plan based on the user's feedback.

Original workout:
{original_plan}

User feedback:
{feedback}

Requirements:
- Keep the plan personalized.
- Keep it practical.
- Modify the workout according to the feedback.
- Preserve the 7-day structure where possible.
- Include warm-up, exercises, sets/reps, recovery and cooldown.
- Return only the updated workout plan.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text