from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "ci_zJ9DSnTbO4fSjRVxKjn2956LhXDre0y8DkMNgMmpp1ptQDsNe_u5RMwxGr0XAN2pjyHOuJ5yAd1KfnQGQUg=="
org = "cheekyagentpotter@gmail.com"
bucket = "test"
query = 'from(bucket: "test")\
|> range(start: -10m)\
|> filter(fn:(r) => r._measurement == “h2o_level”)\
|> filter(fn: (r) => r.location == "coyote_creek")\
|> filter(fn:(r) => r._field == "water_level" )'

client = InfluxDBClient(url="https://eu-central-1-1.aws.cloud2.influxdata.com", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

#create and write the point
p = Point("h2o_level").tag("location", "coyote_creek").field("water_level", 1)
write_api.write(bucket=bucket,org=org,record=p)
#return the table and print the result
result = client.query_api().query(org=org, query=query)
results = []
for table in result:
    for record in table.records:
        results.append((record.get_value(), record.get_field()))
print(results)



