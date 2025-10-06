-- Create DataBase
CREATE DATABASE IF NOT EXISTS test_db;

-- Active DataBase
USE test_db;

-- Drop Table If Exists
DROP TABLE IF EXISTS test;

-- Create Test Table
CREATE TABLE test (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(30),
    description VARCHAR(50),
    cost INTEGER
);

-- Inject Test Data
INSERT INTO
    test (id, title, description, cost)
VALUES
    (1, 'Title 1', 'Description 1', 100),
    (2, 'Title 2', 'Description 2', 100),
    (3, 'Title 3', 'Description 3', 100),
    (4, 'Title 4', 'Description 4', 200),
    (5, 'Title 5', 'Description 5', 200),
    (6, 'Title 6', 'Description 6', 200),
    (7, 'Title 7', 'Description 7', 300),
    (8, 'Title 8', 'Description 8', 300),
    (9, 'Title 9', 'Description 9', 300),
    (10, 'Title 10', 'Description 10', 400),
    (11, 'Title 11', 'Description 11', 400),
    (12, 'Title 12', 'Description 12', 400),
    (13, 'Title 13', 'Description 13', 500),
    (14, 'Title 14', 'Description 14', 500),
    (15, 'Title 15', 'Description 15', 600);