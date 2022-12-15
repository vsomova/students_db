CREATE TABLE Authors (
    name VARCHAR(25) PRIMARY KEY,
    addr VARCHAR(25)
);

CREATE TABLE Books (
    title VARCHAR(30),
    authorName VARCHAR(25),
    year INTEGER,
    genre VARCHAR(25),
    format VARCHAR(7),
    coverType VARCHAR(10),
    PRIMARY KEY (title, authorName),
    FOREIGN KEY (authorName) REFERENCES Authors(name)
);