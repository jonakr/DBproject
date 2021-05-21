# Project of the databases lecture 2021

Matrikelnummer: 8366074
## Overview

Faceit Stats - Analyze your Faceit CS:GO Statistics and compare it with others!

Add faceit players to a [MySQL](https://www.mysql.com/de/) database and track their stats with [InfluxDB](https://www.influxdata.com/)!

Front- and Backend: [Dash](https://dash.plotly.com/)

## Functions

* add a player and his matches
* select a player to show his stats as line and pie chart
* compare stats of two players
## Structure

* [src](https://github.com/jonakrumrein/DBproject/tree/main/src)
    * [assets](https://github.com/jonakrumrein/DBproject/tree/main/src/assets)
        * Contains css and js that is execute add app launch.
    * [data](https://github.com/jonakrumrein/DBproject/tree/main/src/data)
        * Contains faceit level pictures.
    * [tests](https://github.com/jonakrumrein/DBproject/tree/main/src/tests)
        * Contains all tests for the included py-files
## Getting Started

1. Install the required dependencies!
    * `requirments.txt` contains all required dependencies.
    * Execute `pip install -r requirements.txt`.
2. Start the localhost webapp!
    * Navigate to the `src`-folder.
    * Run `python app.py`.
    * Ctrl + Click on the URL shown in the console.
3. Now you are ready to go!

## Optional: Create own InfluxDB

1. First you need a running MySQL Server!
2. Create a database called `faceit`.
3. Add [this](https://github.com/jonakrumrein/DBproject/blob/main/setup/players.sql) to your created database with the MySQL CLI.
    * `mysql -u username -p faceit < players.sql` 
4. Update the [dbCredentials.py](https://github.com/jonakrumrein/DBproject/blob/main/src/dbCredentials.py) with your MySQL Credentials.
## Optional: Create own InfluxDB

1. Drop your current MySQl `player` table (if created locally).
2. Setup a InfluxDB bucket called `matches`.
3. Update the [dbCredentials.py](https://github.com/jonakrumrein/DBproject/blob/main/src/dbCredentials.py) with your InfluxDB Credentials.

## Executing tests

1. Make sure you are inside the `src`-file.
2. Execute `python -m pytest --cov-config=tests/.coveragerc --cov=. tests/`.
3. The console shows passed tests and the coverage.
![Last Coverage (19.05.2021)](https://github.com/jonakrumrein/DBproject/blob/main/src/tests/coverage.png)

The `app.py` isn't tested because its only used as UI.
