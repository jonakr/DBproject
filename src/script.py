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
from getPlayerId import getPlayerId
import pandas as pd

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
        )
    ]),
    html.Div([
        dcc.Input(id='input', type='text', placeholder='Enter a playername...'),
        html.Button(id='submit-button-state', n_clicks=0, children='Submit')]),
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
                {'label': 'K/D', 'value': 'K/D'},
                {'label': 'KPR', 'value': 'KPR'},
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
])


@app.callback(
    Output('players-dd', 'options'),
    Input('submit-button-state', 'n_clicks'),
    State('input', 'value'),
)
def update_output_div(nClicks, input_value):
    if input_value:
        addPlayer(input_value)
        
    # TODO: wait until addPlayer is done
    
    cursor.execute("SELECT name FROM players")
    return [{"label": i['name'], "value": i['name']} for i in cursor.fetchall()]


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
    Output('player1', 'options'),
    Output('player2', 'options'),
    Input('player1', 'value'),
    Input('player2', 'value'),
    Input('yaxis', 'value'),
)
def update_graph(player1, player2, yaxis):
    
    # TODO: maybe safe playname as foreign key
    #       add if to prevent errors
    player1Id = getPlayerId(player1)
    player2Id = getPlayerId(player2)

    df = pd.read_sql("SELECT * FROM matches WHERE playerId = '{}' OR playerId = '{}'".format(player1Id, player2Id), con=db)

    if yaxis == 'K/D':
        print()

    if yaxis == 'KPR':
        print()

    # TODO: find good solution for x values

    fig = px.line(df, y=yaxis, color='playerId')
    fig.data[0].update(mode='markers+lines')
    fig.data[1].update(mode='markers+lines')

    cursor.execute("SELECT name FROM players")
    players = cursor.fetchall()
    return fig, [{"label": i['name'], "value": i['name']} for i in players], [{"label": i['name'], "value": i['name']} for i in players]
    

if __name__ == '__main__':
    app.run_server(debug=True)