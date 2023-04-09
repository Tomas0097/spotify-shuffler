DROP DATABASE IF EXISTS spotify_shuffler;
CREATE DATABASE spotify_shuffler;

CREATE USER IF NOT EXISTS 'spotify_shuffler'@'%' IDENTIFIED BY '1122';
GRANT ALL PRIVILEGES ON spotify_shuffler.* TO 'spotify_shuffler'@'%';