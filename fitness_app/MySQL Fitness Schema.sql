CREATE DATABASE IF NOT EXISTS fitness_app;
USE fitness_app;

-- Create the Write Side Schema
CREATE TABLE IF NOT EXISTS gym_members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    member_name VARCHAR(255) NOT NULL
);

INSERT INTO gym_members (member_name) VALUES
('Alice'),
('Bob'),
('Charlie'),
('Diana'),
('Evan'),
('Fiona'),
('George'),
('Hannah'),
('Isaac'),
('Jasmine'),
('Kevin'),
('Luna'),
('Miles'),
('Nina'),
('Oscar'),
('Paula'),
('Quinn'),
('Ryan'),
('Sophie'),
('Tyler'),
('Uma'),
('Victor'),
('Wendy'),
('Xander'),
('Yara'),
('Zane'),
('Liam'),
('Noah'),
('Olivia'),
('Zoe');

CREATE TABLE gym_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_name VARCHAR(100) NOT NULL,
    check_in_time TIME NOT NULL,
    check_out_time TIME DEFAULT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    counter INT NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


#ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';