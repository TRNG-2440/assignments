DELETE FROM books.books
	WHERE author = (SELECT author_id FROM books.author
		WHERE author_name = 'Mark Twain')