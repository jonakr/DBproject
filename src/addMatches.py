import json
import requests
import mysql.connector
from config import *

def addMatches(id):
    matches = json.loads(requests.get('https://open.faceit.com/data/v4/players/' + id + '/history?game=csgo&offset=0&limit=10', headers=headers).content)

    cursor = db.cursor()
    cursor.execute("SHOW TABLES LIKE 'matches'")
    result = cursor.fetchone()

    if not result:
        cursor.execute(dbMatchesLayout)

    for match in matches['items']:
        matchStats = json.loads(requests.get('https://open.faceit.com/data/v4/matches/' + match['match_id'] + '/stats', headers=headers).content)

        for team in matchStats['rounds'][0]['teams']:
            for player in team['players']:
                if player['player_id'] == id:
                    win = team['team_stats']['Team Win']
                    kills = player['player_stats']['Kills']
                    deaths = player['player_stats']['Deaths']
                    assists = player['player_stats']['Assists']
                    headshots = player['player_stats']['Headshots %']
                    triples = player['player_stats']['Triple Kills']
                    quads = player['player_stats']['Quadro Kills']
                    pentas = player['player_stats']['Penta Kills']

        sql = "INSERT INTO matches (matchId, playerId, map, result, win, kills, deaths, assists, headshots, triples, quads, pentas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (match['match_id'], id , matchStats['rounds'][0]['round_stats']['Map'], matchStats['rounds'][0]['round_stats']['Score'], win, kills, deaths, assists, headshots, triples, quads, pentas)
        
        cursor.execute(sql, val)
        db.commit()