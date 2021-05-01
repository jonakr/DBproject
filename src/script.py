import json
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import mysql.connector
from addPlayer import addPlayer

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="faceit"
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer 85c91c97-e563-4ee8-acc1-aea288b42369',
    }

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



mycursor = db.cursor(dictionary=True)
mycursor.execute("SELECT name FROM players")
players = mycursor.fetchall()

app.layout = html.Div([
    html.H6("Input a Faceit Nickname!"),
    html.Div([
        dcc.Dropdown(
            id='players-dd',
            options=[{"label": i['name'], "value": i['name']} for i in players],
        )
    ]),
    html.Div([
        dcc.Input(id='input', type='text'),
        html.Button(id='submit-button-state', n_clicks=0, children='Submit')]),
    html.Br(),
    html.Div(id='output-state'),
    html.Div(id='test'),

])


@app.callback(
    Output('test', 'children'),
    Input('submit-button-state', 'n_clicks'),
    State('input', 'value'),
)
def update_output_div(nClicks, input_value):
    if input_value:
        addPlayer(input_value)
        return 1
    else: 
        return 0

@app.callback(
    Output('output-state', 'children'),
    Input('players-dd', 'value'),
)
def update_output_div(input_value):
    if input_value:
        mycursor.execute("SELECT * FROM players WHERE name = '{}'".format(input_value))
        player = mycursor.fetchall()
        return 'Output: {} '.format(player[0]['name'])
    else:
        return ''
    

if __name__ == '__main__':
    app.run_server(debug=True)