-- Example: list books for member_id = 1

SELECT
    L.loan_id,
    B.book_id,
    B.title,
    B.author,
    L.loan_date,
    L.return_date
FROM Loans L
JOIN Books B ON L.book_id = B.book_id
WHERE L.member_id = 1;
