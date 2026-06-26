--Mark White
--2026-06-25
--Assignment#5
--Provide an SQL statement that will return the total page count of all books written by Stephen King.



--Sum using JOIN
SELECT SUM(b.page_count)
FROM library.books b
JOIN library.authors a
    ON b.author = a.author_id
WHERE a.author_name = 'Stephen King'; --2397

--Sum using subquery
SELECT SUM(b.page_count)
FROM library.books b
WHERE b.auther = (
    SELECT author_id
    FROM library.authors
    WHERE author_name = 'Stephen King' --2397
);