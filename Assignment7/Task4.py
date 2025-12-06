# ❌ Buggy Code
# class Student:
#     def __init__(name, roll):
#         name = name
#         roll = roll

# No self keyword → attributes not assigned

# ✅ Fixed version
class Student:
    def __init__(self, name, roll):
        self.name = name
        self.roll = roll

    def display(self):
        print("Name:", self.name)
        print("Roll:", self.roll)

s = Student("Adnan", 107)
s.display()
