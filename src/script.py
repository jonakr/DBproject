import json
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import mysql.connector
from addPlayer import addPlayer
from config import *

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
        mycursor.execute("SELECT * FROM players WHERE name = '{}'".format(input_value))
        player = mycursor.fetchall()
        return player[0]['name'], player[0]['avatar'], "https://steamcommunity.com/profiles/{}".format(player[0]['steamProfile'])
    else:
        return '', '', ''
    

if __name__ == '__main__':
    app.run_server(debug=True)