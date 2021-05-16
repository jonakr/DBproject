from src.mysqldb import Mysql


def test_init_value():
    db = Mysql(host="localhost", user="root", password="root", database="testing")  
    assert db.__host == "localhost"
    assert db.__user == "root"
    assert db.__password == "root"
    assert db.__database == "testing"