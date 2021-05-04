from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import json, requests

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer 85c91c97-e563-4ee8-acc1-aea288b42369',
}

# You can generate a Token from the "Tokens Tab" in the UI
token = "ci_zJ9DSnTbO4fSjRVxKjn2956LhXDre0y8DkMNgMmpp1ptQDsNe_u5RMwxGr0XAN2pjyHOuJ5yAd1KfnQGQUg=="
org = "cheekyagentpotter@gmail.com"
bucket = "test"

client = InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

matches = json.loads(requests.get('https://open.faceit.com/data/v4/players/26fc6f28-4374-4339-9b5e-01a26340fb12/history?game=csgo&offset=0&limit=20', headers=headers).content)
for match in matches['items']:
    matchStats = json.loads(requests.get('https://open.faceit.com/data/v4/matches/' + match['match_id'] + '/stats', headers=headers).content)

    id = match['match_id']
    timestamp = match['started_at']

    for team in matchStats['rounds'][0]['teams']:
        for player in team['players']:
            if player['player_id'] == '26fc6f28-4374-4339-9b5e-01a26340fb12':
                win = team['team_stats']['Team Win']
                kills = player['player_stats']['Kills']
                deaths = player['player_stats']['Deaths']

    data = 'stats,host={} win={},kills={},deaths={} {}'.format('26fc6f28-4374-4339-9b5e-01a26340fb12', win, kills, deaths, timestamp)
    write_api.write(bucket, org, data, write_precision='s')

query = '''
    from(bucket: "test")
        |> range(start: -7d)\
        |> filter(fn: (r) => r["_measurement"] == "stats")
        |> filter(fn: (r) => r["_field"] == "kills")
        |> yield(name: "mean")
'''

result = client.query_api().query_data_frame(query, org=org)

print(result)

# results = []
# for table in result:
#   for record in table.records:
#     results.append((record.get_field(), record.get_value()))

# print(results)