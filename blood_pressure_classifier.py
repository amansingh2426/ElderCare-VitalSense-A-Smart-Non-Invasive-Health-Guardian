def classify_bp(systolic, diastolic, age, gender):
    gender = gender.lower()
    
    if gender not in ['male', 'female']:
        return "Invalid gender. Please enter 'male' or 'female'."

    # Slight adjustment by gender
    systolic_adjust = 0
    diastolic_adjust = 0

    if gender == 'female':
        systolic_adjust = -2  # Women tend to have slightly lower BP
        diastolic_adjust = -1

    systolic += systolic_adjust
    diastolic += diastolic_adjust

    # Blood pressure classification
    if systolic < 90 or diastolic < 60:
        category = "Low Blood Pressure (Hypotension)"
    elif 90 <= systolic <= 120 and 60 <= diastolic <= 80:
        category = "Normal Blood Pressure"
    elif 121 <= systolic <= 129 and diastolic < 80:
        category = "Elevated Blood Pressure"
    elif 130 <= systolic <= 139 or 80 <= diastolic <= 89:
        category = "High Blood Pressure (Hypertension Stage 1)"
    elif systolic >= 140 or diastolic >= 90:
        category = "High Blood Pressure (Hypertension Stage 2)"
    else:
        category = "Unusual Blood Pressure Reading"

    # Special note for older adults
    if age >= 60 and category == "High Blood Pressure (Hypertension Stage 1)":
        category += " – Common in older adults, monitor regularly"

    return {
        "Adjusted Systolic": systolic,
        "Adjusted Diastolic": diastolic,
        "Category": category
    }


if __name__ == "__main__":
    bp_reading = classify_bp(systolic=135, diastolic=85, age=65, gender='Male')
    for k, v in bp_reading.items():
        print(f"{k}: {v}")
