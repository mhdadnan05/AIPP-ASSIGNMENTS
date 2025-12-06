# Task 3 – Fibonacci with Explanation & Transparency

def fibonacci(n):
    """
    Computes the nth Fibonacci number.

    Base cases:
        F(0) = 0
        F(1) = 1

    Recursive rule:
        F(n) = F(n-1) + F(n-2)
    """
    if n == 0:      # Base case 1
        return 0
    if n == 1:      # Base case 2
        return 1

    # Recursive computation
    return fibonacci(n-1) + fibonacci(n-2)


if __name__ == "__main__":
    n = int(input("Enter n (non-negative integer): "))
    print(f"Fibonacci({n}) = {fibonacci(n)}")
