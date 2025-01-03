from sqlite3 import Date
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import codegym_db

class Exercise(BaseModel):
    name: str
    reps: int 
    workout_id: int
    exercise_id: int

class WorkoutPlan(BaseModel):
    workout_id: int
    workout_plan_name: str
    start_date: Date
    end_date: Date

class WorkoutSession(BaseModel):
    exercise_id: int
    weight: float
    session_date: Date

app = FastAPI()

origins = [ # what we want to be able to access the API
    "http://localhost:3000" # react frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# endpoint workout plans

@app.get("/workoutplans", response_model=List[WorkoutPlan])
def get_workout_plans(): # works
    workouts_list = codegym_db.get_workout_plans()
    workouts = []
    for workout in workouts_list:
        workouts.append(
            WorkoutPlan(
                end_date=workout.get("end_date"),
                start_date=workout.get("start_date"),
                workout_plan_name=workout.get("workout_plan_name"),
                workout_id=workout.get("workout_id")
            )
        )
    return workouts_list

@app.post("/workoutplans", response_model=WorkoutPlan)
def add_workout_plan(workout_plan: WorkoutPlan):
    workout_id = codegym_db.add_workout_plan(
        name=workout_plan.workout_plan_name,
        start_date=workout_plan.start_date,
        end_date=workout_plan.end_date
    )
    workout_plan.workout_id = workout_id
    return workout_plan


# endpoints for exercises

@app.get("/workoutplans/{workout_id}/exercises", response_model=List[Exercise])
def get_exercises(workout_id: int):
    exercises_list = codegym_db.get_exercises(workout_id) # TODO: get the exercise for an actual plan when lucia changes it
    exercises = []
    for exercise in exercises_list:
        exercises.append(
            Exercise(
                exercise_id=exercise.get("exercise_id"),
                name=exercise.get("exercise_name"),
                reps=exercise.get("reps"),
                workout_id=workout_id
            )
        )
    return exercises

@app.post("/exercises", response_model=Exercise)
def add_exercise(exercise: Exercise):
    id = codegym_db.add_exercise(
        exercise_name=exercise.name,
        reps=exercise.reps,
        workout_id=exercise.workout_id
    )
    exercise.exercise_id = id
    return exercise


# endpoints for sessions

@app.post("/sessions", response_model=WorkoutSession)
def add_workout_session(session: WorkoutSession):
    codegym_db.add_session(
        exercise_id=session.exercise_id,
        weight=session.weight,
        date=session.session_date
    )
    return session

@app.get("/exercises/{exercise_id}/sessions", response_model=List[WorkoutSession])
def get_workout_sessions_for_exercise(exercise_id: int):
    sessions_list = codegym_db.get_sessions(exercise_id)
    sessions = []
    for session in sessions_list:
        sessions.append(
            WorkoutSession(
                exercise_id=session.get("exercise_id"),
                session_id=session.get("session_id"),
                weight=session.get("weight"),
                session_date=session.get("session_date")
            )
        )
    return sessions



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)