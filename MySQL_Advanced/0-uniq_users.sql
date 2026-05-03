-- "users" cədvəlini yaradırıq
-- Əgər cədvəl artıq mövcuddursa, script xəta verməməlidir (IF NOT EXISTS)
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
