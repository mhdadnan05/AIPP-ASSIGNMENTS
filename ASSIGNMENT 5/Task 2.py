# Task 2 – Detecting Bias in AI Decision Making

def loan_approval(name, gender, income):
    """
    Example showing gender bias in decision logic.
    Later we improve the logic to remove bias.
    """
    # ❌ BIased logic: males get easier approval
    if gender.lower() == "male" and income >= 30000:
        return "Loan Approved"
    elif income >= 50000:
        return "Loan Approved"
    else:
        return "Loan Rejected"


# Testing with different people
data = [
    ("Adnan", "Male", 30000),
    ("Riya", "Female", 30000),
    ("Rahul", "Male", 25000),
    ("Sneha", "Female", 50000)
]

for person in data:
    print(person, "=>", loan_approval(*person))

print("\n⚠ Bias Observed: Females need higher income to qualify.")

# ---------------- FIXED VERSION ----------------

def fair_loan_approval(name, income):
    """Unbiased version — gender removed from decision."""
    return "Loan Approved" if income >= 30000 else "Loan Rejected"

print("\nAfter Fix (No Gender Considered):")
for person in data:
    print(person[0], "=>", fair_loan_approval(person[0], person[2]))
