import pandas as pd

import plotly.express as px

from config import token, org, bucket, url

from influx import Influx

from collections import Counter


influx = Influx(token=token, org=org, bucket=bucket, url=url)

def createPieChart(player):

    query = '''
            from(bucket: "{}")
                |> range(start: -30d)\
                |> filter(fn: (r) => r["_measurement"] == "stats")
                |> filter(fn: (r) => r["_field"] == "map")
                |> filter(fn: (r) => r["host"] == "{}")
                |> yield(name: "mean")
        '''.format(bucket, player)

    result = influx.query(query)

    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_value()))

    df = pd.DataFrame(Counter(results).items())

    if df.empty:
        df = pd.DataFrame(data={0: ["hasn't played in the last month"], 1: [1]})

    return px.pie(df, values=1, names=0, template="plotly_dark", title="Maps played by " + player, color_discrete_sequence=px.colors.sequential.RdBu)