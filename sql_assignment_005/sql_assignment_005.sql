set foreign_key_checks = 0;

drop database if exists Book_Database;

create database `Book_Database`;

set foreign_key_checks = 1;

use Book_Database;

create table Author
(
    author_id serial,
    author_name varchar(255) not null,

    primary key (author_id)
);

create table Books
(
    book_id serial,
    title varchar(255) not null,
    author int not null,
    publication int not null,
    page_count int not null, 

    primary key (book_id)
);

-- Insert into Authors table
INSERT INTO Author (author_id, author_name) VALUES
(1001, 'Agatha Christie'),
(1002, 'George Orwell'),
(1003, 'Kurt Vonnegut'),
(1004, 'Mark Twain'),
(1005, 'Stephen King');

-- Insert into Books table
INSERT INTO Books (book_id, title, author, publication, page_count) VALUES
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


SELECT
    author.*,
    books.*,
    SUM(books.page_count) OVER (PARTITION BY books.author) AS total_page_count
FROM author
JOIN books
    ON author.author_id = books.author
WHERE author.author_id = 1005;


SELECT
    books.author,
    SUM(books.page_count) AS total_page_count
FROM books
WHERE books.author = 1005
GROUP BY books.author;