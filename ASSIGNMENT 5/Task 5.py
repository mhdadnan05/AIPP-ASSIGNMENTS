# Task 5 – Inclusive & Gender Neutral Code Design

# ❌ Non-inclusive statement example
def old_welcome_message(name, gender):
    if gender.lower() == "male":
        return f"Welcome Mr. {name}, he is successfully logged in."
    else:
        return f"Welcome Ms. {name}, she is successfully logged in."


# ✅ Inclusive & gender-neutral version
def inclusive_welcome(name, pronoun="they"):
    return f"Welcome {name}! {pronoun.capitalize()} are now logged in successfully."


# Testing both
print("---- Non-Inclusive Output ----")
print(old_welcome_message("Adnan", "male"))
print(old_welcome_message("Riya", "female"))

print("\n---- Inclusive Output ----")
print(inclusive_welcome("Adnan", "he"))
print(inclusive_welcome("Riya", "she"))
print(inclusive_welcome("Alex"))      # Default neutral pronoun
