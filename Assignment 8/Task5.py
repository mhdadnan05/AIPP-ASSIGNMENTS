import unittest

# ---------------------------------------
# BankAccount implementation
# ---------------------------------------

class BankAccount:
    def __init__(self, owner, balance=0.0):
        self.owner = owner
        self.balance = float(balance)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        return self.balance

    def get_balance(self):
        return self.balance


# ---------------------------------------
# Unit Tests (TDD style)
# ---------------------------------------

class TestBankAccount(unittest.TestCase):

    def setUp(self):
        # runs before every test
        self.acc = BankAccount("Adnan", 100.0)

    def test_initial_balance(self):
        self.assertEqual(self.acc.get_balance(), 100.0)

    def test_deposit_valid(self):
        self.acc.deposit(50)
        self.assertEqual(self.acc.get_balance(), 150.0)

    def test_deposit_negative_raises(self):
        with self.assertRaises(ValueError):
            self.acc.deposit(-10)

    def test_withdraw_valid(self):
        self.acc.withdraw(40)
        self.assertEqual(self.acc.get_balance(), 60.0)

    def test_withdraw_all(self):
        self.acc.withdraw(100.0)
        self.assertEqual(self.acc.get_balance(), 0.0)

    def test_withdraw_more_than_balance(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(200.0)

    def test_withdraw_negative_raises(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(-5)

    def test_multiple_operations(self):
        self.acc.deposit(50)   # 150
        self.acc.withdraw(20)  # 130
        self.acc.deposit(70)   # 200
        self.assertEqual(self.acc.get_balance(), 200.0)


if __name__ == "__main__":
    unittest.main()
