import unittest

# ---------------------------------------
# Calculator Functions
# ---------------------------------------

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return a / b


# ---------------------------------------
# Unit Test Class for Calculator
# ---------------------------------------

class TestCalculator(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(10, 5), 15)

    def test_add_negative(self):
        self.assertEqual(add(-2, -3), -5)

    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)

    def test_subtract_negative(self):
        self.assertEqual(subtract(-5, -5), 0)

    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)

    def test_multiply_zero(self):
        self.assertEqual(multiply(0, 99), 0)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)

    def test_divide_error(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)


# Run Tests
if __name__ == "__main__":
    unittest.main()
