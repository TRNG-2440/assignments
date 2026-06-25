SELECT SUM(page_count) as "PageCount"
FROM Books
WHERE author IN (
    SELECT author_id
    FROM Author
    WHERE author_name = 'Stephen King'
);