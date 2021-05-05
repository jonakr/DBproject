import json
import requests
import mysql.connector

from config import db, headers, dbPlayersLayout
from addMatches import addMatches

def addPlayer(arg):
    player = json.loads(requests.get('https://open.faceit.com/data/v4/players?nickname=' + arg + '&game=csgo', headers=headers).content)
    # stats = json.loads(requests.get('https://open.faceit.com/data/v4/players/' + player['player_id'] + '/stats/csgo', headers=headers).content)

    cursor = db.cursor(buffered=True)
    cursor.execute("SHOW TABLES LIKE 'players'")
    result = cursor.fetchone()

    if not result:
        cursor.execute(dbPlayersLayout)

    sql = "SELECT name FROM players WHERE name = '(%s)'"
    val = arg
    result = cursor.execute(sql, val)

    if result:
        sql = "INSERT INTO players (playerId, name, avatar, country, skillLevel, faceitElo, steamProfile) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (player['player_id'], player['nickname'], player['avatar'], player['country'], player['games']['csgo']['skill_level'], player['games']['csgo']['faceit_elo'], player['steam_id_64'])
        
        cursor.execute(sql, val)
        db.commit()

    addMatches(player['player_id'])
