-- ----------- Schema ----------------

-- Genre table
CREATE TABLE IF NOT EXISTS Genre (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(255) NOT NULL UNIQUE
);

-- -------------------------------------------------------

-- Book table
CREATE TABLE IF NOT EXISTS Book (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publication_year INT NOT NULL,
    genre_id INT NOT NULL,
    copy_count INT NOT NULL DEFAULT 1,
    FOREIGN KEY (genre_id) REFERENCES Genre (genre_id)
);

-- -------------------------------------------------------

-- Member table
CREATE TABLE IF NOT EXISTS Member (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    join_date DATE NOT NULL
);

-- -------------------------------------------------------

-- Loan table
CREATE TABLE IF NOT EXISTS Loan (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE NULL,
    FOREIGN KEY (book_id) REFERENCES Book (book_id),
    FOREIGN KEY (member_id) REFERENCES Member (member_id)
);
-- -------------------------------------------------------