import unittest

# ---------- Implementation to be tested ----------

def is_valid_email(email: str) -> bool:
    """
    Valid email rules (from assignment):
    1. Must contain '@' and '.' characters.
    2. Must NOT start or end with special characters.
       (We treat non-alphanumeric as special for start/end).
    3. Should not allow multiple '@'.
    """
    if not isinstance(email, str):
        return False

    email = email.strip()

    # must contain @ and .
    if "@" not in email or "." not in email:
        return False

    # only one @ allowed
    if email.count("@") != 1:
        return False

    # no spaces
    if " " in email:
        return False

    # not start or end with special char
    if not email[0].isalnum() or not email[-1].isalnum():
        return False

    # dot must appear after '@'
    at_index = email.index("@")
    if "." not in email[at_index:]:
        return False

    return True


# ---------- TEST CASES (TDD style) ----------

class TestEmailValidator(unittest.TestCase):

    def test_valid_simple_email(self):
        self.assertTrue(is_valid_email("test@example.com"))

    def test_valid_with_dots_and_numbers(self):
        self.assertTrue(is_valid_email("user.name123@domain.co"))

    def test_valid_subdomain(self):
        self.assertTrue(is_valid_email("user_name@sub.domain.org"))

    def test_missing_at_symbol(self):
        self.assertFalse(is_valid_email("test.example.com"))

    def test_missing_dot(self):
        self.assertFalse(is_valid_email("user@domaincom"))

    def test_multiple_ats(self):
        self.assertFalse(is_valid_email("user@@example.com"))

    def test_starts_with_special_char(self):
        self.assertFalse(is_valid_email(".user@example.com"))

    def test_ends_with_special_char(self):
        self.assertFalse(is_valid_email("user@example.com."))

    def test_space_not_allowed(self):
        self.assertFalse(is_valid_email("user name@example.com"))

    def test_non_string_input(self):
        self.assertFalse(is_valid_email(12345))


if __name__ == "__main__":
    unittest.main()
