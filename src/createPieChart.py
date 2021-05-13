import pandas as pd

import plotly.express as px

from config import token, org, bucket, url

from influx import Influx

from collections import Counter


def createPieChart(player):
    """
    Querys all maps played from the influx database for a specific player,
    creates and returns a plotly express pie chart figure.

    Parameters
    ----------
    player : str
        the player the data should be querried for

    Returns
    -------
    px.pie
        the created plotly express pie chart figure
    """

    influx = Influx(token=token, org=org, bucket=bucket, url=url)

    # query all maps played by the given player
    query = '''
            from(bucket: "{}")
                |> range(start: -30d)\
                |> filter(fn: (r) => r["_measurement"] == "stats")
                |> filter(fn: (r) => r["_field"] == "map")
                |> filter(fn: (r) => r["host"] == "{}")
                |> yield(name: "mean")
        '''.format(bucket, player)

    result = influx.query(query)

    # format result
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_value()))

    # count occurances of each map and convert to data frame
    df = pd.DataFrame(Counter(results).items())

    # create 100% pie chart data frame with error message
    if df.empty:
        df = pd.DataFrame(
            data={0: ["hasn't played in the last month"], 1: [1]})

    return px.pie(df, values=1, names=0, template="plotly_dark", 
                title="Maps played by " + player, color_discrete_sequence=px.colors.sequential.RdBu)
