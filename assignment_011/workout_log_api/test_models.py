#dummy test file for models.py

from models import WorkoutCreate


workout = WorkoutCreate(
    exercise_name = "Bench Press",
    category = "Strength",
    sets = 3,
    reps = 10,
    weight = 135
)


print(workout)
print(workout.model_dump())