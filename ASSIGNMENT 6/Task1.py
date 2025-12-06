# Task 1 – Student Class (Generated using AI Assistance)

class Student:
    def __init__(self, name, roll, dept):
        self.name = name
        self.roll = roll
        self.dept = dept

    def display_details(self):
        print("\n----- Student Details -----")
        print("Name:", self.name)
        print("Roll Number:", self.roll)
        print("Department:", self.dept)


# Taking input from user
name = input("Enter student name: ")
roll = input("Enter roll number: ")
dept = input("Enter department: ")

# Creating object
student1 = Student(name, roll, dept)
student1.display_details()
