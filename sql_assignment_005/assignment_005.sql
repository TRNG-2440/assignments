-- with subquery
SELECT SUM(b.page_count) 'total page count'
FROM books b
WHERE author = (
    SELECT author_id FROM author WHERE author_name = 'Stephen King'
);

-- with join
SELECT SUM(b.page_count) 'total page count'
FROM books b
JOIN author a ON a.id = b.author
WHERE a.author_name = 'Stephen King';

-- using group by, having. not recommended for this situation.
-- calls SUM() on every record then filters at end.
SELECT a.author_name, SUM(books.page_count) 'total page count'
FROM books b
JOIN author a ON a.id = b.author
GROUP BY a.author_name
HAVING a.author_name = 'Stephen King';