# Task 5 – Exception Handling in Python

try:
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))

    result = num1 / num2
    print(f"\nResult = {result}")

except ZeroDivisionError:
    print("\n❌ Error: Division by zero is not allowed!")

except ValueError:
    print("\n❌ Error: Please enter valid numeric values only!")

except Exception as e:
    print("\n❌ Unexpected Error:", e)

finally:
    print("\nProgram Completed Successfully!")

