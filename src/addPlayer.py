import json
import requests

from config import headers, dbPlayersLayout, avatarPng
from addMatches import addMatches

def addPlayer(db, name):
    player = json.loads(requests.get('https://open.faceit.com/data/v4/players?nickname=' + name + '&game=csgo', headers=headers).content)

    if not 'errors' in player:
        result = db.checkIfTableExists('players')
        if not result:
            db.addTable(dbPlayersLayout)

        playerExists = db.select('players', "name = '{}'".format(name), 'name')

        if not playerExists:

            if not player['avatar']:
                avatar = avatarPng
            else:
                avatar = player['avatar']

            db.insert('players', player['player_id'], player['nickname'], avatar, player['country'], player['games']['csgo']['skill_level'], player['games']['csgo']['faceit_elo'], player['steam_id_64'])

        addMatches(name, player['player_id'])
        return True

    else:
        return False
