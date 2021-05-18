import pytest
import json

from src.createPieChart import createPieChart
from src.influx import Influx

@pytest.fixture
def test_database():
    ''' Returns a InfluxDB object'''
    token = "ci_zJ9DSnTbO4fSjRVxKjn2956LhXDre0y8DkMNgMmpp1ptQDsNe_u5RMwxGr0XAN2pjyHOuJ5yAd1KfnQGQUg=="
    org = "cheekyagentpotter@gmail.com"
    bucket = "matches"
    url="https://eu-central-1-1.aws.cloud2.influxdata.com"
    
    return Influx(token=token, org=org, bucket=bucket, url=url)

def test_pie_chart_with_data(test_database):
    assert createPieChart(test_database, 'Pimp').layout.title.text == 'Maps played by Pimp'

def test_pie_chart_for_empty_games(test_database):
    fig_json = json.loads(createPieChart(test_database, 'TrilluXe').to_json())
    assert createPieChart(test_database, 'TrilluXe').layout.title.text == 'Maps played by TrilluXe'
    assert fig_json['data'][0]['labels'][0] == "hasn't played in the last month"