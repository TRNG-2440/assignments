SELECT SUM(page_count) AS "Total Pages of Stephen King Books" FROM books.books
	WHERE author = (SELECT author_id FROM books.author
		WHERE author_name = 'Stephen King')