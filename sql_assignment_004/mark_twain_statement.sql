--Mark White
--2026-06-25
--SQL Assignment 4
--SQL statement to delete all books written by Mark Twain

-- Manual Delete
DELETE FROM library.books
WHERE author_id = 1004;

--Using Subquery
DELETE FROM library.books
WHERE author = (
    SELECT author.id
    FROM library.authors
    WHERE author_name = 'Mark Twain'
)