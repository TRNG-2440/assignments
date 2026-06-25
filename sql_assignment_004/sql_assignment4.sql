DELETE FROM books
WHERE author = (
    SELECT author_id
    FROM author
    WHERE author_name = 'Mark Twain'
)
