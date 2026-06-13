def generate_recommendations(
    sleep_hours,
    water_intake,
    exercise_minutes,
    energy_level,
    stress_level
):
    insights = []

    if sleep_hours < 7:
        insights.append(
            "Sleep is below the recommended range."
        )

    if water_intake >= 2:
        insights.append(
            "Hydration is good."
        )
    else:
        insights.append(
            "Hydration may need improvement."
        )

    if exercise_minutes < 30:
        insights.append(
            "Physical activity is lower than recommended."
        )

    if stress_level >= 7:
        insights.append(
            "Stress levels are elevated."
        )

    if energy_level <= 4:
        insights.append(
            "Energy levels are lower than expected."
        )

    action = determine_best_action(
        sleep_hours,
        exercise_minutes,
        stress_level
    )

    return insights, action


def determine_best_action(
    sleep_hours,
    exercise_minutes,
    stress_level
):
    if sleep_hours < 6 and stress_level >= 7:
        return (
            "Focus on recovery today. "
            "Prioritize hydration, a short walk, "
            "and an earlier bedtime."
        )

    if exercise_minutes < 15:
        return (
            "Try a 20-minute walk before sunset "
            "to improve activity levels."
        )

    if stress_level >= 7:
        return (
            "Schedule a short relaxation or "
            "mindfulness session today."
        )

    return (
        "Maintain your current healthy habits "
        "and stay consistent."
    )