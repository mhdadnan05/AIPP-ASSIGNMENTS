# Task 3 – Polymorphism using Method Overriding

class Animal:
    def sound(self):
        print("Animals make different sounds")

class Dog(Animal):
    def sound(self):
        print("Dog barks: Woof Woof 🐶")

class Cat(Animal):
    def sound(self):
        print("Cat meows: Meow Meow 🐱")


# Function to show polymorphism
def make_sound(animal):
    animal.sound()


# Main Execution
print("Choose an animal:")
print("1. Dog")
print("2. Cat")

choice = input("Enter choice (1/2): ")

if choice == "1":
    obj = Dog()
elif choice == "2":
    obj = Cat()
else:
    print("Invalid choice!")
    exit()

make_sound(obj)   # Same function works for different objects
