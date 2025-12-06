# Task 4 – File Handling (Write & Read Operations)

# Writing data to a file
def write_data():
    data = input("Enter text to write into file: ")
    with open("student_data.txt", "w") as file:
        file.write(data)
    print("\nData written to student_data.txt successfully!")

# Reading data from the file
def read_data():
    print("\nReading data from student_data.txt...")
    try:
        with open("student_data.txt", "r") as file:
            print("\n----- File Content -----")
            print(file.read())
    except FileNotFoundError:
        print("\nFile not found. Write data first!")


# Main Program Menu
print("1. Write to File")
print("2. Read from File")
choice = input("Enter choice (1/2): ")

if choice == "1":
    write_data()
elif choice == "2":
    read_data()
else:
    print("Invalid choice!")
