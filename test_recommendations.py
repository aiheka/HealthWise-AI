from src.recommendations.recommendation_engine import (
    generate_recommendations
)

insights, action = generate_recommendations(
    sleep_hours=5,
    water_intake=2.5,
    exercise_minutes=10,
    energy_level=4,
    stress_level=8
)

print("Today's Insights:")
for item in insights:
    print("-", item)

print("\nMost Impactful Action Today:")
print(action)