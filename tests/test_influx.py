import pytest
import urllib3
from src.influx import Influx

@pytest.fixture
def test_database():
    ''' Returns a InfluxDB object'''
    token = "ci_zJ9DSnTbO4fSjRVxKjn2956LhXDre0y8DkMNgMmpp1ptQDsNe_u5RMwxGr0XAN2pjyHOuJ5yAd1KfnQGQUg=="
    org = "cheekyagentpotter@gmail.com"
    bucket = "test"
    url="https://eu-central-1-1.aws.cloud2.influxdata.com"
    
    return Influx(token=token, org=org, bucket=bucket, url=url)

@pytest.fixture
def test_faulty_database():
    ''' Returns a faulty InfluxDB object'''
    token = "these"
    org = "credentials"
    bucket = "won't"
    url="work"
    
    return Influx(token=token, org=org, bucket=bucket, url=url)

def test_write_and_query(test_database):
    data = "mem,host=host1 used_percent=23.43234543"
    test_database.write(data)

    query = '''
            from(bucket: "test")
                |> range(start: -30d)\
                |> filter(fn: (r) => r["_measurement"] == "mem")
                |> filter(fn: (r) => r["_field"] == "used_percent")
                |> filter(fn: (r) => r["host"] == "host1")
                |> yield(name: "mean")
        '''
    assert test_database.query(query)[0].records[0].get_value() == 23.43234543

def test_faulty_db(test_faulty_database):
    with pytest.raises(urllib3.exceptions.NewConnectionError):
        data = "mem,host=host1 used_percent=23.43234543"
        test_faulty_database.write(data)

