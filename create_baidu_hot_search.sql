USE project_db;

CREATE TABLE IF NOT EXISTS baidu_hot_search (
    id INT PRIMARY KEY AUTO_INCREMENT,
    `rank` INT,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(512),
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
