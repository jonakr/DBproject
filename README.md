# Project of the databases lecture 2021

Faceit Stats - Analyze your Faceit CS:GO Statistics and compare it with others!

Add faceit players to a [MySQL](https://www.mysql.com/de/) database and track their stats with [InfluxDB](https://www.influxdata.com/)!

## Getting Started

1. First you need a running MySQL Server!
    * Create a database called `faceit`.
    * Add [this](https://github.com/jonakrumrein/DBproject/blob/main/setup/players.sql) to your created database with the MySQL CLI.
        * `mysql -u username -p faceit < players.sql` 
    * Update the [dbCredentials.py](https://github.com/jonakrumrein/DBproject/blob/main/src/dbCredentials.py) with your MySQL Credentials.
    * (Optional) Create a `testing` databases to be able to execute test files later.
2. Install the required dependencies!
    * `requirments.txt` contains all required dependencies.
    * Execute `pip install -r requirements.txt`.
3. Start the localhost webapp!
    * Navigate to the `src`-folder.
    * Run `python app.py`.
    * Ctrl + Click on the URL shown in the console.
4. Now you are ready to go!

## Optional: Create own InfluxDB

1. Drop your current MySQl `player` table.
2. Setup a InfluxDB bucket called `matches`.
3. Update the [dbCredentials.py](https://github.com/jonakrumrein/DBproject/blob/main/src/dbCredentials.py) with your InfluxDB Credentials.

## Executing tests

1. Make sure you are inside the `src`-file.
2. Execute `python -m pytest --cov-config=tests/.coveragerc --cov=. tests/`.
3. The console shows passed tests and the coverage.
![Last Coverage (19.05.2021)](https://github.com/jonakrumrein/DBproject/blob/main/src/tests/coverage.png)

## Structure

* [src](https://github.com/jonakrumrein/DBproject/tree/main/src)
    * [assets](https://github.com/jonakrumrein/DBproject/tree/main/src/assets)
        * Contains css and js that is execute add app launch.
    * [data](https://github.com/jonakrumrein/DBproject/tree/main/src/data)
        * Contains faceit level pictures.
    * [tests](https://github.com/jonakrumrein/DBproject/tree/main/src/tests)
        * Contains all tests for the included py-files
