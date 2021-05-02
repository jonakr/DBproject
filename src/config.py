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

dbPlayersLayout = "CREATE TABLE players ( \
    playerId VARCHAR(255) NOT NULL,       \
    name VARCHAR(255),                    \
    avatar VARCHAR(255),                  \
    country VARCHAR(255),                 \
    skillLevel VARCHAR(255),              \
    faceitElo VARCHAR(255),               \
    steamProfile VARCHAR(255),                 \
    PRIMARY KEY (playerId))"

dbMatchesLayout = "CREATE TABLE matches ( \
    matchId VARCHAR(255) NOT NULL,        \
    playerId VARCHAR(255),                \
    map VARCHAR(255),                     \
    result VARCHAR(255),                  \
    win INT,                              \
    kills INT,                            \
    deaths INT,                           \
    assists INT,                          \
    headshots INT,                        \
    triples INT,                          \
    quads INT,                            \
    pentas INT,                           \
    PRIMARY KEY (matchId),                \
    FOREIGN KEY (playerId) REFERENCES players(playerId))"