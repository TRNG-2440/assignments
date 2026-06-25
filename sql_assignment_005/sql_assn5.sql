SELECT SUM(page_count) AS total_page_count FROM Books

WHERE author IN (
    SELECT author_id
    FROM Author
    WHERE author_name = 'Stephen King'
);