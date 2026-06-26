-- UPDATE employees SET salary = salary * 1.1 WHERE department = 'Sales';
-- DELETE FROM employees WHERE department = 'Sales';


DELETE FROM Books WHERE author = (SELECT author_id FROM Author WHERE author_name = 'Mark Twain');