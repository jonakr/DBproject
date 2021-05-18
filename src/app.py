import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.express as px

import base64

from mysqldb import Mysql
from influx import Influx
from addPlayer import addPlayer
from createPieChart import createPieChart
from config import dbPlayersLayout
from dbCredentials import token, org, url, bucket, host, user, password, database


# --------------- ON START ACTIONS ---------------

app = dash.Dash(__name__, title='Faceit Stats')

# initialize database connections
db = Mysql(host=host, user=user, password=password, database=database)
influx = Influx(token=token, org=org, bucket=bucket, url=url)

# check if table 'players' exists
result = db.checkIfTableExists('players')
if not result:
    db.addTable(dbPlayersLayout)

# select all names from the 'players' table
players = db.select('players', None, 'name')


# ------------------ APP LAYOUT ------------------

app.layout = html.Div([

    html.H1("Analyze your Faceit CS:GO Statistics and compare it with others!", style={
            "color": "#fff"}),
    dbc.Row([
        dbc.Col([
            dbc.Input(id='input', type='text',
                      placeholder='Enter a playername...       (Matches will be updated if the player already exists!)'),
        ]),
        dbc.Col([
            dbc.Button(id='submit-button-state',
                       n_clicks=0, children='Add Player'),
        ])
    ], style={"margin-bottom": "20px"}),

    dbc.Row([
        dbc.Col([
            dbc.Alert(
                "This player doesn't exist!",
                id="alert",
                color="danger",
                is_open=False,
                dismissable=True,
                duration=4000
            )
        ]),
    ], style={"margin-bottom": "20px"}),

    dbc.Row([

        dbc.Col([
            dcc.Dropdown(
                id='player1',
                options=[{'label': i['name'], 'value': i['name']}
                         for i in players],
                placeholder='Select player one...'
            ),
        ], md=4),

        dbc.Col([
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
                placeholder='Select the stat to compare...'
            ),
        ], md=4),

        dbc.Col([
            dcc.Dropdown(
                id='player2',
                options=[{'label': i['name'], 'value': i['name']}
                         for i in players],
                placeholder='Select player two...'
            ),
        ], md=4),

    ], no_gutters=True, style={"margin-bottom": "20px"}),

    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    dbc.CardImg(id='player1-img'),
                    dbc.CardBody([
                        html.H4(id='player1-name'),
                        dbc.Table(html.Tbody([
                            html.Tr([
                                html.Td(html.Img(id='player1-level',
                                    style={'width': '50px', 'height': '50px'})),
                                html.Td(id='player1-elo')
                            ]),
                            html.Tr([
                                html.Td(id='player1-label'),
                                html.Td(id='player1-average')
                            ]),
                        ])),
                        dbc.Button("Go to Steam Profile", id='player1-steam')
                    ])
                ], id='card-player1', color="dark", inverse=True),

                dbc.Card([
                    dbc.CardBody([
                        html.H1("VS", style={
                                "text-align": "center", "font-size": "80px"}),
                    ])
                ], id='card-vs', color="dark", inverse=True),

                dbc.Card([
                    dbc.CardImg(id='player2-img'),
                    dbc.CardBody([
                        html.H4(id='player2-name'),
                        dbc.Table(html.Tbody([
                            html.Tr([
                                html.Td(html.Img(id='player2-level',
                                    style={'width': '50px', 'height': '50px'})),
                                html.Td(id='player2-elo')
                            ]),
                            html.Tr([
                                html.Td(id='player2-label'),
                                html.Td(id='player2-average')
                            ]),
                        ])),
                        dbc.Button("Go to Steam Profile", id='player2-steam')
                    ])
                ], id='card-player2', color="dark", inverse=True)
            ]),
        ], id='card-column', width={"size": 6, "offset": 3})
    ]),

    dbc.Row([

        dbc.Col([
            dcc.Graph(id='pie-chart-1'),
        ],
            id='pie-chart-div1',
            width=6,
            style={'display': 'none'}),

        dbc.Col([
            dcc.Graph(id='pie-chart-2'),
        ],
            id='pie-chart-div2',
            width=6,
            style={'display': 'none'})
    ], no_gutters=True,),

    dbc.Row([
        dbc.Col(dcc.Graph(id='indicator-graphic')),
    ]),
])


# ------------------ APP CALLBACKS ------------------

@app.callback(
    Output('player1', 'options'),
    Output('player2', 'options'),
    Output('alert', 'is_open'),
    Output('input', 'value'),
    Input('submit-button-state', 'n_clicks'),
    State('input', 'value'),
)
def callbackAddPlayer(n_clicks, input):
    if input:
        if addPlayer(db, input):
            players = [{"label": i['name'], "value": i['name']}
                       for i in db.select('players', None, 'name')]
            return players, players, False, ''
        else:
            players = [{"label": i['name'], "value": i['name']}
                       for i in db.select('players', None, 'name')]
            return players, players, True, ''
    else:
        players = [{"label": i['name'], "value": i['name']}
                   for i in db.select('players', None, 'name')]
        return players, players, False, ''


@app.callback(
    Output('player1-name', 'children'),
    Output('player1-img', 'src'),
    Output('player1-steam', 'href'),
    Output('player1-elo', 'children'),
    Output('player1-level', 'src'),
    Output('player1-label', 'children'),
    Output('player1-average', 'children'),
    Input('player1', 'value'),
    Input('yaxis', 'value')
)
def callbackUpdatePlayer1Card(player1, value):
    if player1 and value:
        query = '''
            from(bucket: "{}")
                |> range(start: -30d)\
                |> filter(fn: (r) => r["_measurement"] == "stats")
                |> filter(fn: (r) => r["_field"] == "{}")
                |> filter(fn: (r) => r["host"] == "{}")
                |> yield(name: "mean")
                |> mean()
        '''.format(bucket, value, player1)

        average = round(influx.query(query)[1].records[0].get_value(), 2)

        player = db.select('players', "name = '{}'".format(
            player1), 'name', 'avatar', 'steamProfile', 'faceitElo', 'skillLevel')

        img_filename = "data/level_" + player[0]['skillLevel'] + ".png"

        encoded_img = base64.b64encode(open(img_filename, 'rb').read())

        return player[0]['name'], player[0]['avatar'], \
            "https://steamcommunity.com/profiles/{}".format(player[0]['steamProfile']), \
            player[0]['faceitElo'], 'data:image/png;base64,{}'.format(
            encoded_img.decode()), \
            "Average {}".format(value), average
    else:
        return '', '', '', '', '', '', ''


@app.callback(
    Output('player2-name', 'children'),
    Output('player2-img', 'src'),
    Output('player2-steam', 'href'),
    Output('player2-elo', 'children'),
    Output('player2-level', 'src'),
    Output('player2-label', 'children'),
    Output('player2-average', 'children'),
    Input('player2', 'value'),
    Input('yaxis', 'value')
)
def callbackUpdatePlayer2Card(player2, value):
    if player2 and value:
        query = '''
            from(bucket: "{}")
                |> range(start: -30d)\
                |> filter(fn: (r) => r["_measurement"] == "stats")
                |> filter(fn: (r) => r["_field"] == "{}")
                |> filter(fn: (r) => r["host"] == "{}")
                |> yield(name: "mean")
                |> mean()
        '''.format(bucket, value, player2)

        average = round(influx.query(query)[1].records[0].get_value(), 2)

        player = db.select('players', "name = '{}'".format(
            player2), 'name', 'avatar', 'steamProfile', 'faceitElo', 'skillLevel')
        img_filename = "data/level_" + player[0]['skillLevel'] + ".png"
        encoded_img = base64.b64encode(open(img_filename, 'rb').read())
        return player[0]['name'], player[0]['avatar'], \
            "https://steamcommunity.com/profiles/{}".format(player[0]['steamProfile']), \
            player[0]['faceitElo'], 'data:image/png;base64,{}'.format(
            encoded_img.decode()), \
            "Average {}".format(value), average
    else:
        return '', '', '', '', '', '', ''


@app.callback(
    Output('card-player1', 'style'),
    Output('card-vs', 'style'),
    Output('card-player2', 'style'),
    Output('card-column', 'width'),
    Input('player1', 'value'),
    Input('player2', 'value'),
    Input('yaxis', 'value')
)
def showHidePlayerCard(player1, player2, value):
    if player1 and not player2 and value:
        return {'display': 'inline'}, {'display': 'none'}, {'display': 'none'}, {"size": 2, "offset": 3}
    if not player1 and player2 and value:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'inline'}, {"size": 2, "offset": 7}
    if player1 and player2 and value:
        return {'display': 'inline'}, {'display': 'inline'}, {'display': 'inline'}, {"size": 6, "offset": 3}
    else:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {"size": 6, "offset": 3}


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('player1', 'value'),
    Input('player2', 'value'),
    Input('yaxis', 'value'),
)
def update_graph(player1, player2, yaxis):
    if yaxis and player1 or yaxis and player2:
        query = '''
            from(bucket: "{}")
                |> range(start: -30d)\
                |> filter(fn: (r) => r["_measurement"] == "stats")
                |> filter(fn: (r) => r["_field"] == "{}")
                |> filter(fn: (r) => r["host"] == "{}" or r["host"] == "{}")
                |> yield(name: "mean")
        '''.format(bucket, yaxis, player1, player2)

        df = influx.query(query, True)

        if not df.empty:
            fig = px.line(df, x='_time', y='_value', color='host', template="plotly_dark", title='',
                          labels=dict(_time="time", _value=yaxis,
                                      host='player'),
                          color_discrete_sequence=['#67001f', '#d6604d']
                          )
            fig.data[0].update(mode='markers+lines')

            if len(fig.data) > 1:
                fig.data[1].update(mode='markers+lines')

            return fig
        else:
            return px.line(template="plotly_dark")

    else:
        return px.line(template="plotly_dark")


@app.callback(
    Output('pie-chart-1', 'figure'),
    Output('pie-chart-div1', 'style'),
    Output('pie-chart-2', 'figure'),
    Output('pie-chart-div2', 'style'),
    Input('player1', 'value'),
    Input('player2', 'value'),
)
def update_piechart(player1, player2):

    if player1 and not player2:
        return createPieChart(influx, player1), {'display': 'inline'}, px.pie(), {'display': 'none'}
    if player2 and not player1:
        return px.pie(), {'display': 'none'}, createPieChart(influx, player2), {'display': 'inline'}
    if player1 and player2:
        return createPieChart(influx, player1), {'display': 'inline'}, createPieChart(influx, player2), {'display': 'inline'}
    else:
        return px.pie(), {'display': 'none'}, px.pie(), {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=True)
