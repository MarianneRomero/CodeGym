import sqlite3

def db_connect():
    conn = sqlite3.connect("codegym_db.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db_connect()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS workout_plan (
            workout_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_name TEXT NOT NULL,
            reps INTEGER NOT NULL,
            FOREIGN KEY (workout_id) REFERENCES workout_plan (workout_id)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS workout_sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_date TEXT NOT NULL,
            weight INTEGER NOT NULL,
            FOREIGN KEY (exercise_id) REFERENCES exercises (exercise_id)
        )
    ''')
    conn.commit()
    conn.close()


def add_workout_plan(start_date: str, end_date: str):
    conn = db_connect()
    conn.execute('''INSERT INTO workout_plan (start_date, end_date) VALUES (?, ?)''', (start_date, end_date))
    conn.commit()
    conn.close()

def add_exercise(workout_id: int, exercise_name: str, reps: int):
    conn = db_connect()
    conn.execute('''INSERT INTO exercises (exercise_name, reps, workout_id) VALUES (?, ?, ?);''', (exercise_name, reps, workout_id))
    conn.commit()
    conn.close()

def get_exercises(workout_id: int):
    conn = db_connect()
    cursor = conn.execute('''SELECT * FROM exercises WHERE workout_id=?''', (workout_id,))
    exercises = cursor.fetchall()
    conn.close()
    return[dict(row) for row in exercises]


# # Initialize the database
# init_db()

add_workout_plan("2024-11-01", "2024-11-30")

# Add a workout
add_exercise(1,"Push Ups", 15)  # Example: Push-ups with no weight
add_exercise(2,"abs", 30)

# Retrieve workouts
exercises = get_exercises(1)
for exercise in exercises:
    print(exercise)