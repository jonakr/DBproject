from influx import Influx 

token = "ci_zJ9DSnTbO4fSjRVxKjn2956LhXDre0y8DkMNgMmpp1ptQDsNe_u5RMwxGr0XAN2pjyHOuJ5yAd1KfnQGQUg=="
org = "cheekyagentpotter@gmail.com"
bucket = "test"
url = "https://eu-central-1-1.aws.cloud2.influxdata.com"

query = '''
                from(bucket: "test")
                    |> range(start: -30d)\
                    |> filter(fn: (r) => r["_measurement"] == "stats")
                    |> filter(fn: (r) => r["_field"] == "map")
                    |> filter(fn: (r) => r["host"] == "26fc6f28-4374-4339-9b5e-01a26340fb12")
                    |> yield(name: "mean")
            '''

connection = Influx(token=token, org=org, bucket=bucket, url=url)

print(connection.query(query))