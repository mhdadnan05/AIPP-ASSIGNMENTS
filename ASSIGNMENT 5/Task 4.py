# Task 4 – Job Applicant Scoring System (Bias & Fairness)

# ❌ Example of biased scoring (gender used wrongly)
def biased_score_applicant(name, gender, skills, experience_years):
    score = 0

    # Skill score (0–100)
    score += skills

    # Experience weight
    score += experience_years * 2

    # ❌ Biased boost (unethical example)
    if gender.lower() == "male":
        score += 10   # unfair extra points

    return score


# ✅ Fair scoring (no gender, only skills + experience)
def fair_score_applicant(name, skills, experience_years):
    score = 0
    score += skills
    score += experience_years * 2
    return score


# Test data
candidates = [
    ("Adnan", "male", 80, 3),
    ("Riya", "female", 80, 3),
    ("Rahul", "male", 70, 5),
    ("Sneha", "female", 70, 5),
]

print("---- Biased Scoring ----")
for name, gender, skills, exp in candidates:
    print(
        f"{name} ({gender}) => Score: "
        f"{biased_score_applicant(name, gender, skills, exp)}"
    )

print("\n⚠ Observation: Male candidates get extra points only because of gender.\n")

print("---- Fair Scoring (No Gender Used) ----")
for name, gender, skills, exp in candidates:
    print(
        f"{name} ({gender}) => Score: "
        f"{fair_score_applicant(name, skills, exp)}"
    )

print("\n✅ Bias Mitigated: Gender is removed from scoring logic.")
