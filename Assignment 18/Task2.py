def check_number(num):
    if num < 0:
        print("The number is negative")
    elif num > 0:
        print("The number is positive")
    else:
        print("The number is zero")

# Get input from user and call the function
number = int(input("Enter a number: "))
check_number(number)