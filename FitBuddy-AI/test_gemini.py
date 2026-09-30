from app.gemini_generator import generate_workout_gemini

plan = generate_workout_gemini(
    age=21,
    weight=70,
    goal="muscle gain",
    intensity="beginner"
)

print(plan)