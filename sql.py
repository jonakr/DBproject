import mysql.connector
import pandas as pd

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="faceit"
)

cursor = db.cursor(dictionary=True)

sql = "SELECT playerId FROM players WHERE name = '{}'".format('Pimp')
cursor.execute(sql)
print(cursor.fetchall()[0]['playerId'])