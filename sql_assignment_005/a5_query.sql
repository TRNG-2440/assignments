-- get total page count for all books written by Stephen King
SELECT SUM(page_count) AS total_page_count
FROM books
WHERE author IN (
    SELECT author_id 
    FROM author
    WHERE author_name = 'Stephen King'
);