import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="faceit"
)

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer 85c91c97-e563-4ee8-acc1-aea288b42369',
}

dbTableLayout = "CREATE TABLE players ( \
    playerId VARCHAR(255) NOT NULL,     \
    name VARCHAR(255),                  \
    avatar VARCHAR(255),                \
    country VARCHAR(255),               \
    skillLevel VARCHAR(255),            \
    faceitElo VARCHAR(255),             \
    steamProfile INT,                   \
    PRIMARY KEY(playerId))"