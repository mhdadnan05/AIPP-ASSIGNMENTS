def fibonacci(n):
    """
    Calculate the nth Fibonacci number using recursion.
    
    Parameters:
    n (int): The position in the Fibonacci sequence (n >= 0)
    
    Returns:
    int: The nth Fibonacci number
    """
    # Base case: 0th Fibonacci number is 0
    if n == 0:
        return 0
    # Base case: 1st Fibonacci number is 1
    elif n == 1:
        return 1
    # Recursive case: sum of the two previous Fibonacci numbers
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

# Take input from the user
n = int(input("Enter the position n to calculate the nth Fibonacci number: "))

# Validate input
if n < 0:
    print("Please enter a non-negative integer.")
else:
    result = fibonacci(n)
    print(f"The {n}th Fibonacci number is: {result}")
