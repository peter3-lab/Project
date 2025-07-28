
DROP DATABASE IF EXISTS project_db;

CREATE DATABASE project_db CHARACTER SET utf8mb4;

USE project_db;

CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    height DECIMAL(5, 2)
);

INSERT INTO students (name, height) VALUES ('张三', 175.00);
INSERT INTO students (name, height) VALUES ('李四', 180.50);
INSERT INTO students (name, height) VALUES ('王五', 168.00);

SELECT * FROM students;

SELECT * FROM students WHERE name = '李四';

UPDATE students SET height = 176.50 WHERE name = '张三';

DELETE FROM students WHERE name = '王五';