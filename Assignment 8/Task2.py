import unittest

# -------- Function to Test --------

def assign_grade(score):
    """
    Assigns grade based on score.
    - 90-100 -> A
    - 80-89  -> B
    - 70-79  -> C
    - 60-69  -> D
    - <60    -> F
    Invalid if score not between 0-100 or non-numeric.
    """
    if not isinstance(score, (int, float)):
        return "Invalid"
    if score < 0 or score > 100:
        return "Invalid"

    if score >= 90: return "A"
    elif score >= 80: return "B"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    else: return "F"


# ----------- Test Cases -----------

class TestGradeAssignment(unittest.TestCase):

    def test_grade_A(self):
        self.assertEqual(assign_grade(95), "A")

    def test_grade_B(self):
        self.assertEqual(assign_grade(85), "B")

    def test_grade_C(self):
        self.assertEqual(assign_grade(72), "C")

    def test_grade_D(self):
        self.assertEqual(assign_grade(65), "D")

    def test_grade_F(self):
        self.assertEqual(assign_grade(40), "F")

    def test_invalid_negative(self):
        self.assertEqual(assign_grade(-5), "Invalid")

    def test_invalid_high(self):
        self.assertEqual(assign_grade(120), "Invalid")

    def test_invalid_string(self):
        self.assertEqual(assign_grade("85"), "Invalid")

    def test_boundary_100(self):
        self.assertEqual(assign_grade(100), "A")

    def test_boundary_59(self):
        self.assertEqual(assign_grade(59), "F")


if __name__ == "__main__":
    unittest.main()
