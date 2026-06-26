-- CREATE SCHEMA IF NOT EXISTS assign05;

-- CREATE TABLE IF NOT EXISTS assign05.Author(
-- 		author_id INTEGER PRIMARY KEY,
-- 		author_name VARCHAR(200)
-- );

-- CREATE TABLE IF NOT EXISTS assign05.Books(
-- 		book_id INTEGER PRIMARY KEY,
-- 		title VARCHAR(300),
-- 		author INTEGER,
-- 		publication_id INTEGER,
-- 		Page_Count INTEGER,

-- 		CONSTRAINT author_id_fk FOREIGN KEY (author) REFERENCES assign05.Author(author_id)
-- );

-- INSERT INTO assign05.Author VALUES (1001, 'Agatha Christie');
-- INSERT INTO assign05.Author VALUES (1002, 'George Orwell');
-- INSERT INTO assign05.Author VALUES (1003, 'Kurt Vonnegut');
-- INSERT INTO assign05.Author VALUES (1004, 'Mark Twain');
-- INSERT INTO assign05.Author VALUES (1005, 'Stephen King');

-- INSERT INTO assign05.Books VALUES (3050, 'Murder on the Orient Express', 1001, 1934, 256);
-- INSERT INTO assign05.Books VALUES (3051, 'It', 1005, 1986, 1138);
-- INSERT INTO assign05.Books VALUES (3052, 'And Then There Were None', 1001, 1939, 272);
-- INSERT INTO assign05.Books VALUES (3053, 'Pet Sematary', 1005, 1983, 373);
-- INSERT INTO assign05.Books VALUES (3054, 'Slaughterhouse-Five', 1003, 1969, 215);
-- INSERT INTO assign05.Books VALUES (3055, 'Nineteen Eighty-Four', 1002, 1949, 328);
-- INSERT INTO assign05.Books VALUES (3056, 'Adventures of Huckleberry Finn', 1004, 1884, 366);
-- INSERT INTO assign05.Books VALUES (3057, 'Death on the Nile', 1001, 1937, 288);
-- INSERT INTO assign05.Books VALUES (3058, 'Animal Farm', 1002, 1945, 112);
-- INSERT INTO assign05.Books VALUES (3059, 'The Adventures of Tom Sawyer', 1004, 1876, 274);
-- INSERT INTO assign05.Books VALUES (3060, 'The Shining', 1005, 1977, 447);
-- INSERT INTO assign05.Books VALUES (3061, 'Salem''s Lot', 1005, 1975, 439);
-- INSERT INTO assign05.Books VALUES (3062, 'Cat''s Cradle', 1003, 1963, 304);

-- Select * FROM assign05.Author;

-- Select * FROM assign05.Books;

SELECT author, sum(page_count) FROM assign05.Books WHERE author = 1005 GROUP BY author;