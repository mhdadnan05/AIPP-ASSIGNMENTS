# BIASED VERSION
def score_applicant(years, education, skills, gender):
    score = years * 5
    if education == "PhD":
        score += 20
    score += skills * 0.5
    if gender == "male":  # ⚠️ Gender bias
        score += 5
    return "Hire" if score > 50 else "No Hire"

print("Biased Decision 1:", score_applicant(8, "Masters", 30, "male"))  # Hire (due to +5 for male)
print("Biased Decision 2:", score_applicant(8, "Masters", 10, "female"))  # No Hire (bias visible)


# UNBIASED VERSION
def score_applicant(years, education, skills):
    score = years * 5
    if education == "PhD":
        score += 20
    score += skills * 0.5
    return "Hire" if score > 50 else "No Hire"

print("Unbiased Decision 1:", score_applicant(8, "Masters", 30))  # Hire
print("Unbiased Decision 2:", score_applicant(7, "Bachelors", 30))  # No Hire
