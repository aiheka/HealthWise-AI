def generate_daily_plan(
    sleep_hours,
    stress_level,
    exercise_minutes,
    energy_level
):

    if sleep_hours < 6 and stress_level >= 7:
        return """
Today should be a recovery-focused day.

Priority Actions:
• Drink at least 2.5 liters of water
• Take a 20-minute walk
• Avoid intense workouts
• Aim to sleep 1 hour earlier tonight
"""

    if exercise_minutes < 15:
        return """
Today should be an activity-focused day.

Priority Actions:
• Take a 20–30 minute walk
• Stretch for 5 minutes
• Reduce long periods of sitting
"""

    if energy_level <= 4:
        return """
Today should focus on energy management.

Priority Actions:
• Stay hydrated
• Eat balanced meals
• Take short movement breaks
• Avoid late-night screen usage
"""

    return """
You are doing well today.

Priority Actions:
• Maintain current habits
• Stay active
• Continue healthy hydration and sleep routines
"""