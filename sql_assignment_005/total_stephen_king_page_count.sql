SELECT SUM(Books.page_count) as total_page_count FROM Books
WHERE Book.author = (SELECT Author.author_id FROM Author
                    WHERE Author.author_name = 'Stephen King')
;
