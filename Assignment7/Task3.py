# ❌ Buggy Code – ZeroDivisionError
# def divide(a, b):
#     return a / b

# Runtime fix using try/except

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero!"

# Test
print(divide(10, 0))
