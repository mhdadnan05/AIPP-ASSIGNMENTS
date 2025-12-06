# Task 2 – Inheritance using Python Classes

# Parent / Base Class
class College:
    def __init__(self, college_name, location):
        self.college_name = college_name
        self.location = location

    def display_college(self):
        print("\n----- College Details -----")
        print("College Name:", self.college_name)
        print("Location:", self.location)


# Derived / Child Class
class Student(College):
    def __init__(self, college_name, location, name, roll, department):
        super().__init__(college_name, location)   # Access base class attributes
        self.name = name
        self.roll = roll
        self.department = department

    def display_student(self):
        print("\n----- Student Details -----")
        print("Name:", self.name)
        print("Roll Number:", self.roll)
        print("Department:", self.department)


# Creating object and taking input
c_name = input("Enter college name: ")
loc = input("Enter college location: ")
name = input("Enter student name: ")
roll = input("Enter roll number: ")
dept = input("Enter department: ")

# Object of Student class
s = Student(c_name, loc, name, roll, dept)

# Display Details
s.display_college()
s.display_student()
