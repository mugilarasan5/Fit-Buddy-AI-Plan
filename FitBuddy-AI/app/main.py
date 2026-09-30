from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates

from app.database import (
    SessionLocal,
    User,
    get_original_plan,
    update_plan
)

from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip
from app.updated_plan import update_workout_plan

app = FastAPI(title="FitBuddy")

templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"username": "Sarbudeen"}
    )


@app.post("/generate-workout")
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    workout_plan = generate_workout_gemini(
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    nutrition_tip = generate_nutrition_tip(
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    db = SessionLocal()

    user = User(
        username=username,
        user_id=user_id,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
        original_plan=workout_plan
    )

    db.add(user)
    db.commit()
    db.close()

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": username,
            "user_id": user_id,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip
        }
    )


@app.get("/view-all-users")
def view_all_users(request: Request):
    db = SessionLocal()

    users = db.query(User).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"users": users}
    )


@app.post("/submit-feedback")
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):
    original_plan = get_original_plan(user_id)

    if not original_plan:
        raise HTTPException(
            status_code=404,
            detail="User or workout plan not found"
        )

    updated_plan = update_workout_plan(
        original_plan=original_plan,
        feedback=feedback
    )

    update_plan(
        user_id=user_id,
        updated_plan=updated_plan,
        feedback=feedback
    )

    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    db.close()

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": user.username,
            "user_id": user.user_id,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": updated_plan,
            "nutrition_tip": "Workout updated based on your feedback."
        }
    )