function printStudents(students){
    console.log("Student List:");
    students.forEach(student => {
        console.log(student);
    });
}

printStudents(["Alice", "Bob", "Charlie"]);