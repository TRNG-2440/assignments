DELETE FROM Books
WHERE author = (
    SELECT author_id 
    FROM Authors 
    WHERE name = 'George Orwell'
);