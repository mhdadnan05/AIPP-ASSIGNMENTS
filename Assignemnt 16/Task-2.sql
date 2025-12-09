-- Insert sample Members
INSERT INTO Members (member_id, name, email, join_date) VALUES
(1, 'Amit Sharma', 'amit@example.com', '2023-01-10'),
(2, 'Priya Patel', 'priya@example.com', '2023-02-15'),
(3, 'Ravi Kumar', 'ravi@example.com', '2023-03-20');

-- Insert sample Books
INSERT INTO Books (book_id, title, author, available) VALUES
(101, 'The Alchemist', 'Paulo Coelho', TRUE),
(102, 'Clean Code', 'Robert C. Martin', TRUE),
(103, 'The Power of Habit', 'Charles Duhigg', TRUE);

-- Insert sample Loans
INSERT INTO Loans (loan_id, member_id, book_id, loan_date, return_date) VALUES
(1001, 1, 101, '2024-01-05', NULL),
(1002, 2, 102, '2024-01-10', '2024-01-20'),
(1003, 3, 103, '2024-01-12', NULL);
