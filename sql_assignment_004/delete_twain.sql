-- get id for mark twain with subquery
DELETE FROM books WHERE author IN (SELECT author_id FROM author WHERE author_name = 'Mark Twain');