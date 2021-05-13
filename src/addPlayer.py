import json
import requests

from config import headers, dbPlayersLayout, avatarPng
from addMatches import addMatches

def addPlayer(db, name):
    """
    Pulls player data from the API and inserts it into the MySQL DB.

    Parameters
    ----------
    db : object
        the database a new player should be added to
    name : str
        the name of the new player

    Returns
    -------
    boolean
        true if players was added, false otherwise
    """

    # pulls the data from the API
    player = json.loads(requests.get('https://open.faceit.com/data/v4/players?nickname=' + name + '&game=csgo', headers=headers).content)

    # check if player exists, else return false
    if not 'errors' in player:

        # if there is no table players, add it
        result = db.checkIfTableExists('players')
        if not result:
            db.addTable(dbPlayersLayout)

        # check if player already exists
        playerExists = db.select('players', "name = '{}'".format(name), 'name')

        if not playerExists:
            
            # check if player data contains an avatar or set default
            if not player['avatar']:
                avatar = avatarPng
            else:
                avatar = player['avatar']

            # insert all the pulled data into the players table
            db.insert('players', player['player_id'], player['nickname'], avatar, player['country'], player['games']['csgo']['skill_level'], player['games']['csgo']['faceit_elo'], player['steam_id_64'])

        # call the addMatches function to add the last 20 played matches
        addMatches(name, player['player_id'])
        return True

    else:
        return False
