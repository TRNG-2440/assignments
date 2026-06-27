CREATE TABLE IF NOT EXISTS Genre (
    genre_id    SERIAL          PRIMARY KEY,
    name        varchar(255)    NOT NULL
);

CREATE TABLE IF NOT EXISTS Book (
    book_id         SERIAL          PRIMARY KEY,
    title           VARCHAR(1023)   NOT NULL,
    author          VARCHAR(255)    NOT NULL,
    publication_year DATE           NOT NULL,
    genre_id        int             NOT NULL,
    copy_count      int             DEFAULT 0 NOT NULL,
    CONSTRAINT fk_genre_id
    FOREIGN KEY (genre_id)
    REFERENCES Genre(genre_id)
);

CREATE TABLE IF NOT EXISTS Member (
    member_id       SERIAL          PRIMARY KEY,
    name            VARCHAR(1023)   NOT NULL,
    email           VARCHAR(255)    NOT NULL,
    join_date       DATE            NOT NULL
);

CREATE TABLE IF NOT EXISTS Loan (
    loan_id         SERIAL          PRIMARY KEY,
    book_id         int             NOT NULL,
    member_id       INT             NOT NULL,
    loan_date       DATE            NOT NULL,
    due_date        DATE            NOT NULL,
    return_date     DATE        DEFAULT NULL,
    CONSTRAINT fk_book_id
    FOREIGN KEY (book_id)
    REFERENCES Book(book_id),
    CONSTRAINT fk_member_id
    FOREIGN KEY (member_id)
    REFERENCES Member(member_id)
);

