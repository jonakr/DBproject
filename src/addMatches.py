import json
import requests

from influx import Influx

from config import token, org, bucket, url, headers

def addMatches(name, id):
    """
    Pulls all matches the given player has played from the API
    and writes it to the InfluxDB.

    Parameters
    ----------
    id : str
        the id of the player
    name : str
        the name of the player
    """

    # initialize INfluxDB connection
    influx = Influx(token=token, org=org, bucket=bucket, url=url)

    # pull the last 20 matches of a player via the API
    matches = json.loads(requests.get('https://open.faceit.com/data/v4/players/' + id + '/history?game=csgo&offset=0&limit=20', headers=headers).content)

    # iterate over every match and pull specific data for each match from the API
    for match in matches['items']:
        matchStats = json.loads(requests.get('https://open.faceit.com/data/v4/matches/' + match['match_id'] + '/stats', headers=headers).content)

        # set the timestamp
        timestamp = match['started_at']

        # check if match has stats
        if 'rounds' in matchStats:
            map = matchStats['rounds'][0]['round_stats']['Map']

            # get the team the player has played in and get all his stats
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
                        kpr = player['player_stats']['K/R Ratio']
                        kpd = player['player_stats']['K/D Ratio']

            # write data to the database
            data = 'stats,host={} map="{}",win={},kills={},deaths={},assists={},headshots={},triples={},quads={},pentas={},kpr={},kpd={} {}'.format(name, map, win, kills, deaths, assists, headshots, triples, quads, pentas, kpr, kpd, timestamp)
            influx.write(data)