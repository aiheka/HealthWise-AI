def calculate_wellness_score(
    sleep_hours,
    water_intake,
    exercise_minutes,
    energy_level,
    stress_level
):
    score = 0

    if sleep_hours >= 8:
        score += 25
    elif sleep_hours >= 7:
        score += 20
    elif sleep_hours >= 6:
        score += 15
    elif sleep_hours >= 5:
        score += 10
    else:
        score += 5

    if water_intake >= 2.5:
        score += 20
    elif water_intake >= 2:
        score += 15
    elif water_intake >= 1.5:
        score += 10
    else:
        score += 5

    if exercise_minutes >= 45:
        score += 20
    elif exercise_minutes >= 30:
        score += 15
    elif exercise_minutes >= 15:
        score += 10
    else:
        score += 5

    score += energy_level * 1.5

    if stress_level <= 2:
        score += 20
    elif stress_level <= 4:
        score += 18
    elif stress_level <= 6:
        score += 14
    elif stress_level <= 8:
        score += 10
    else:
        score += 5

    return round(score)


def get_wellness_category(score):
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Needs Attention"
    else:
        return "High Risk"