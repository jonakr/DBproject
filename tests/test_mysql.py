import pytest
from src.mysqldb import Mysql

@pytest.fixture
def test_database():
    ''' Returns a MySql DB object '''
    return Mysql(host="localhost", user="root", password="root", database="testing")

@pytest.fixture
def test_error_database():
    ''' Returns a faulty MySql DB object '''
    return Mysql(host="these", user="credentials", password="are", database="wrong")

def test_addTable(test_database):
    test_database.addTable("CREATE TABLE tests (testname VARCHAR(255), testvalue VARCHAR(255))")
    assert test_database.checkIfTableExists('tests') == True

def test_insert(test_database):
    assert test_database.insert('tests', 'insert_test', 'true') == 0

def test_select(test_database):
    assert test_database.select('tests', "testname = 'insert_test'", 'testvalue') == [{'testvalue': 'true'}]
    assert test_database.select('tests', None, 'testvalue') == [{'testvalue': 'true'}]

def test_drop_table(test_database):
    test_database.dropTable('tests')
    assert test_database.checkIfTableExists('tests') == False

def test_error_on_open(test_error_database):
    with pytest.raises(AttributeError):
        test_error_database.addTable("CREATE TABLE tests (testname VARCHAR(255), testvalue VARCHAR(255))")