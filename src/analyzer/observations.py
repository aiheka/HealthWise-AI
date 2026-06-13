def generate_observations(
    sleep_hours,
    stress_level,
    energy_level
):

    observations = []

    if sleep_hours < 6:
        observations.append(
            "Sleep duration is below recommended levels."
        )

    if stress_level >= 7:
        observations.append(
            "Stress levels appear elevated."
        )

    if energy_level <= 4:
        observations.append(
            "Low energy may be linked to sleep or stress patterns."
        )

    if len(observations) == 0:
        observations.append(
            "Your wellness indicators look stable today."
        )

    return observations