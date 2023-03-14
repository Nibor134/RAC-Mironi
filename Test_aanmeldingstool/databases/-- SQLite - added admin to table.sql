-- SQLite
CREATE TABLE admin (
admin_id int NOT NULL,
username TEXT,
password TEXT,
PRIMARY KEY (admin_id)
);

INSERT INTO admin (admin_id, username, password)
VALUES (1, 'admin1', 'password'); 