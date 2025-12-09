UPDATE Books
SET available = FALSE
WHERE book_id = 101;


DELETE FROM Members
WHERE member_id = 3
  AND member_id NOT IN (
        SELECT member_id FROM Loans WHERE return_date IS NULL
  );
