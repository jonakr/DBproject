import mysql.connector
from config import *

def getPlayerId(id):

    cursor = db.cursor(dictionary=True)

    sql = "SELECT playerId FROM players WHERE name = '{}'".format(id)
    cursor.execute(sql)
    return cursor.fetchall()[0]['playerId']