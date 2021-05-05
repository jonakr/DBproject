import json
import requests

from config import token, org, bucket, client, headers

def addMatches(id):
    matches = json.loads(requests.get('https://open.faceit.com/data/v4/players/' + id + '/history?game=csgo&offset=0&limit=20', headers=headers).content)

    write_api = client.write_api(write_options=SYNCHRONOUS)

    for match in matches['items']:
        matchStats = json.loads(requests.get('https://open.faceit.com/data/v4/matches/' + match['match_id'] + '/stats', headers=headers).content)

        timestamp = match['started_at']

        if 'rounds' in matchStats:
            map = matchStats['rounds'][0]['round_stats']['Map']

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

            data = 'stats,host={} map="{}",win={},kills={},deaths={},assists={},headshots={},triples={},quads={},pentas={},kpr={},kpd={} {}'.format(id, map, win, kills, deaths, assists, headshots, triples, quads, pentas, kpr, kpd, timestamp)
            write_api.write(bucket, org, data, write_precision='s')