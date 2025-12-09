def greet_user():
    name = input("Enter your name: ")
    gender = input("Enter your gender (male/female/non-binary/prefer not to say): ").lower()

    # Assign titles based on gender
    if gender == "male":
        title = "Mr."
    elif gender == "female":
        title = "Ms."
    elif gender in ["non-binary", "prefer not to say", "other"]:
        title = "Mx."
    else:
        title = ""  # fallback if user types something unexpected

    # Greeting message
    print(f"Hello {title} {name}!")

# Run the function
greet_user()
