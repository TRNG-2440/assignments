DELETE FROM Books
WHERE author IN (
    SELECT author_id
    FROM Author
    WHERE author_name = 'Mark Twain'
);