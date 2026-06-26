
DELETE FROM Books
WHERE author = (
	SELECT author_id
	from Author
	where author_name = "Mark Twain"
);