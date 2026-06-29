-- Create Tables
CREATE TABLE Author (
    author_id INT PRIMARY KEY,
    author_name VARCHAR(100) NOT NULL
);

CREATE TABLE Books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    author INT,
    publication INT,
    page_count INT,
    FOREIGN KEY (author) REFERENCES Author(author_id)
);

-- Add authors
INSERT INTO Author (author_id, author_name) VALUES
(1001, 'Agatha Christie'),
(1002, 'George Orwell'),
(1003, 'Kurt Vonnegut'),
(1004, 'Mark Twain'),
(1005, 'Stephen King');

-- Add book created by George Orwell
INSERT INTO Books (title, author, publication, page_count)
VALUES ('Very good book!', 1002, 2072, 10000);

-- Add the books
INSERT INTO Books (book_id, title, author, publication, page_count) OVERRIDING SYSTEM VALUE VALUES
(3050, 'Murder on the Orient Express', 1001, 1934, 256),
(3051, 'It', 1005, 1986, 1138),
(3052, 'And Then There Were None', 1001, 1939, 272),
(3053, 'Pet Sematary', 1005, 1983, 373),
(3054, 'Slaughterhouse-Five', 1003, 1969, 215),
(3055, 'Nineteen Eighty-Four', 1002, 1949, 328),
(3056, 'Adventures of Huckleberry Finn', 1004, 1884, 366),
(3057, 'Death on the Nile', 1001, 1937, 288),
(3058, 'Animal Farm', 1002, 1945, 112),
(3059, 'The Adventures of Tom Sawyer', 1004, 1876, 274),
(3060, 'The Shining', 1005, 1977, 447),
(3061, 'Salem''s Lot', 1005, 1975, 439),
(3062, 'Cat''s Cradle', 1003, 1963, 304);

-- Delete MARK Twain's books, can also delete books written by other authors if the name is changed in the subquery.
DELETE FROM Books b
WHERE EXISTS (
    SELECT 1 
    FROM Author a 
    WHERE a.author_id = b.author
      AND a.author_name = 'Mark Twain'
);

-- Get total page count of all books written by Stephen King.
SELECT SUM(b.page_count) AS total_stephen_king_pages
FROM Books b
JOIN Author a ON b.author = a.author_id
WHERE a.author_name = 'Stephen King';