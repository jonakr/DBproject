import json
import requests
import mysql.connector

headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer 85c91c97-e563-4ee8-acc1-aea288b42369',
    }

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="faceit"
)

dbTableLayout = "CREATE TABLE players ( \
    playerId VARCHAR(255) NOT NULL,     \
    name VARCHAR(255),                  \
    avatar VARCHAR(255),                \
    country VARCHAR(255),               \
    skillLevel VARCHAR(255),            \
    faceitElo VARCHAR(255),             \
    steamProfile INT,                   \
    PRIMARY KEY(playerId))"

def addPlayer(arg):
    player = json.loads(requests.get('https://open.faceit.com/data/v4/players?nickname=' + arg + '&game=csgo', headers=headers).content)
    stats = json.loads(requests.get('https://open.faceit.com/data/v4/players/' + player['player_id'] + '/stats/csgo', headers=headers).content)

    cursor = db.cursor()
    cursor.execute("SHOW TABLES LIKE 'players'")
    result = cursor.fetchone()

    if not result:
        cursor.execute(dbTableLayout)

    sql = "INSERT INTO players (playerId, name, avatar, country, skillLevel, faceitElo, steamProfile) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (player['player_id'], player['nickname'], player['avatar'], player['country'], player['games']['csgo']['skill_level'], player['games']['csgo']['faceit_elo'], player['steam_id_64'])
    
    cursor.execute(sql, val)
    db.commit()
