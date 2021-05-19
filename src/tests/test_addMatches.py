import pytest

from addMatches import addMatches

from influx import Influx

@pytest.fixture
def test_database():
    ''' Returns a InfluxDB object'''
    token = "ci_zJ9DSnTbO4fSjRVxKjn2956LhXDre0y8DkMNgMmpp1ptQDsNe_u5RMwxGr0XAN2pjyHOuJ5yAd1KfnQGQUg=="
    org = "cheekyagentpotter@gmail.com"
    bucket = "test"
    url="https://eu-central-1-1.aws.cloud2.influxdata.com"
    
    return Influx(token=token, org=org, bucket=bucket, url=url)

def test_add_existing_players_matches(test_database):
    assert addMatches(test_database, 'Pimp', '26fc6f28-4374-4339-9b5e-01a26340fb12') == True
    
def test_faulty_id(test_database):
    assert addMatches(test_database, 'Pimp', 'this id is wrong') == False