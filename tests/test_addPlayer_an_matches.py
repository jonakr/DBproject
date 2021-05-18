import pytest

from src.addPlayer import addPlayer

from src.mysqldb import Mysql

@pytest.fixture
def test_database():
    ''' Returns a MySql DB object '''
    return Mysql(host="localhost", user="root", password="root", database="faceit")

def test_adding_not_existing_player(test_database):
    assert addPlayer(test_database, 'thisPlayerDoesntExist') == False

def test_adding_player(test_database):
    assert addPlayer(test_database, 'Pimp') == True