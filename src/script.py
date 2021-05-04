import json
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import mysql.connector
from addPlayer import addPlayer
from config import *
import plotly.express as px
import plotly.graph_objects as go
from getPlayerId import getPlayerId
import pandas as pd
from collections import Counter

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


cursor = db.cursor(dictionary=True)
cursor.execute("SHOW TABLES LIKE 'players'")
result = cursor.fetchone()

if not result:
    cursor.execute(dbPlayersLayout)

cursor.execute("SELECT name FROM players")
players = cursor.fetchall()

app.layout = html.Div([
    html.H3("Faceit Stat Checker"),
    html.Div([
        dcc.Dropdown(
            id='players-dd',
            options=[{"label": i['name'], "value": i['name']} for i in players],
        ),
        dcc.Input(id='input', type='text', placeholder='Enter nickname...'),
        html.Button(id='submit-button-state', n_clicks=0, children='Add Player')
    ]),
    
    html.Br(),
    html.Div([
        html.Img(id='profile-picture'),
        html.A(id='output-name'),
    ]),

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='player1',
                options=[{'label': i['name'], 'value': i['name']} for i in players],
            ),
        ],
        style={'width': '33%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis',
                options=[{'label': 'Kills', 'value': 'kills'},
                {'label': 'Deaths', 'value': 'deaths'},
                {'label': 'Assists', 'value': 'assists'},
                {'label': 'Headshot Rate', 'value': 'headshots'},
                {'label': 'Triple Kills', 'value': 'triples'},
                {'label': 'Quad Kills', 'value': 'quads'},
                {'label': 'Aces', 'value': 'pentas'},
                {'label': 'K/D', 'value': 'kpd'},
                {'label': 'KPR', 'value': 'kpr'},
                {'label': 'Win', 'value': 'win'}],
            ),
        ],
        style={'width': '33%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='player2',
                options=[{'label': i['name'], 'value': i['name']} for i in players],
            ),
        ],style={'width': '33%', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),
    html.Div([
        dcc.Graph(id='pie-chart-1'),
    ], id='pie-chart-div')
])


@app.callback(
    Output('players-dd', 'options'),
    Output('player1', 'options'),
    Output('player2', 'options'),
    Input('submit-button-state', 'n_clicks'),
    State('input', 'value'),
)
def update_output_div(nClicks, input_value):
    if input_value:
        addPlayer(input_value)
    
    cursor.execute("SELECT name FROM players")
    players = cursor.fetchall()
    return [{"label": i['name'], "value": i['name']} for i in players], [{"label": i['name'], "value": i['name']} for i in players], [{"label": i['name'], "value": i['name']} for i in players]


@app.callback(
    Output('output-name', 'children'),
    Output('profile-picture', 'src'),
    Output('output-name', 'href'),
    Input('players-dd', 'value'),
)
def update_output_div(input_value):
    if input_value:
        cursor.execute("SELECT * FROM players WHERE name = '{}'".format(input_value))
        player = cursor.fetchall()
        return player[0]['name'], player[0]['avatar'], "https://steamcommunity.com/profiles/{}".format(player[0]['steamProfile'])
    else:
        return '', '', ''


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('player1', 'value'),
    Input('player2', 'value'),
    Input('yaxis', 'value'),
)
def update_graph(player1, player2, yaxis):
    
    if player1 and yaxis:
        player1Id = getPlayerId(player1)
    else: 
        player1Id = ''
    if player2 and yaxis:
        player2Id = getPlayerId(player2)
    else: 
        player2Id = ''

    if yaxis and player1 or yaxis and player2 :
        query = '''
            from(bucket: "{}")
                |> range(start: -30d)\
                |> filter(fn: (r) => r["_measurement"] == "stats")
                |> filter(fn: (r) => r["_field"] == "{}")
                |> filter(fn: (r) => r["host"] == "{}" or r["host"] == "{}")
                |> yield(name: "mean")
        '''.format(bucket, yaxis, player1Id, player2Id)

        df = client.query_api().query_data_frame(query, org=org)

        fig = px.line(df, x='_time', y='_value', color='host')
        fig.data[0].update(mode='markers+lines')
        if len(fig.data) > 1:
            fig.data[1].update(mode='markers+lines')
    
        return fig
    else:
        return px.line()
    

@app.callback(
    Output('pie-chart-1', 'figure'),
    Output('pie-chart-div', 'style'),
    Input('player1', 'value'),
)
def update_piechart(player1):

    if player1:
        player1Id = getPlayerId(player1)

        query = '''
                from(bucket: "{}")
                    |> range(start: -30d)\
                    |> filter(fn: (r) => r["_measurement"] == "stats")
                    |> filter(fn: (r) => r["_field"] == "map")
                    |> filter(fn: (r) => r["host"] == "{}")
                    |> yield(name: "mean")
            '''.format(bucket, player1Id)

        result = client.query_api().query(query, org=org)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_value()))

        df = pd.DataFrame(Counter(results).items())

        return px.pie(df, values=1, names=0), {'display': 'inline'}
    else:
        return px.pie(), {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=True)