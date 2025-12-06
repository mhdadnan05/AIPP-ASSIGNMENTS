# Task 1 – Privacy & Data Security
# Insecure vs Secure Login System Example

# ----------------- ❌ Insecure Login (Risky) -----------------
def insecure_login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Hardcoded credentials (very unsafe)
    if username == "admin" and password == "12345":
        print("Login Successful (Insecure)")
    else:
        print("Invalid credentials")


# ----------------- ✅ Secure Login (Better) -----------------
import hashlib

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

# Secure storage using hashing
users = {
    "user1": hash_password("mypassword123"),
    "testuser": hash_password("securepass"),
}

def secure_login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    hashed_input = hash_password(password)

    # Compare hashed passwords for security
    if username in users and users[username] == hashed_input:
        print("Secure Login Successful ✔")
    else:
        print("Invalid Credentials ❌")


# ----------------- Program Menu -----------------
print("\nSelect Login Type:")
print("1. Insecure Login (For Risk Analysis)")
print("2. Secure Login (Improved Version)\n")

choice = input("Enter option (1/2): ")

if choice == "1":
    insecure_login()
else:
    secure_login()
