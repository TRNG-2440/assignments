SELECT SUM(page_count) AS total_pages
FROM Books
WHERE author = (
    SELECT author_id
    FROM Author
    WHERE author_name = 'Stephen King'
);