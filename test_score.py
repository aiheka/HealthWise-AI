from src.analyzer.wellness_score import (
    calculate_wellness_score,
    get_wellness_category
)

score = calculate_wellness_score(
    sleep_hours=5,
    water_intake=2.5,
    exercise_minutes=10,
    energy_level=4,
    stress_level=8
)

print("Score:", score)
print("Category:", get_wellness_category(score))