import re
import unittest

# ----------------------------------------------
# Password Strength Checker Function
# ----------------------------------------------

def check_password_strength(password):
    """
    Returns strength of password based on rules:
    Strong   -> length >= 8, contains letters + numbers + special char
    Moderate -> length >= 6, contains letters + numbers
    Weak     -> else (includes passwords containing spaces)
    """

    # ❗ Password containing spaces should be Weak
    if " " in password:
        return "Weak"

    # Strong condition
    if (len(password) >= 8 and
        re.search("[A-Za-z]", password) and
        re.search("[0-9]", password) and
        re.search("[@#$%^&*!]", password)):
        return "Strong"

    # Moderate condition
    elif len(password) >= 6 and re.search("[A-Za-z]", password) and re.search("[0-9]", password):
        return "Moderate"

    else:
        return "Weak"


# ----------------------------------------------
# Unit Test Cases
# ----------------------------------------------

class TestPasswordStrength(unittest.TestCase):

    def test_strong_password(self):
        self.assertEqual(check_password_strength("Abc@1234"), "Strong")

    def test_strong_special(self):
        self.assertEqual(check_password_strength("Test@2023"), "Strong")

    def test_moderate_password(self):
        self.assertEqual(check_password_strength("abc123"), "Moderate")

    def test_moderate_case2(self):
        self.assertEqual(check_password_strength("Hello12"), "Moderate")

    def test_weak_short(self):
        self.assertEqual(check_password_strength("abc"), "Weak")

    def test_weak_only_numbers(self):
        self.assertEqual(check_password_strength("123456"), "Weak")

    def test_weak_only_letters(self):
        self.assertEqual(check_password_strength("abcdef"), "Weak")

    def test_weak_with_space(self):
        self.assertEqual(check_password_strength("abc 123"), "Weak")

    def test_empty(self):
        self.assertEqual(check_password_strength(""), "Weak")

    def test_weak_no_special(self):
        self.assertEqual(check_password_strength("abcd1234"), "Moderate")


# Run tests
if __name__ == "__main__":
    unittest.main()
