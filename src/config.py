token = "ci_zJ9DSnTbO4fSjRVxKjn2956LhXDre0y8DkMNgMmpp1ptQDsNe_u5RMwxGr0XAN2pjyHOuJ5yAd1KfnQGQUg=="
org = "cheekyagentpotter@gmail.com"
bucket = "test"
url="https://eu-central-1-1.aws.cloud2.influxdata.com"

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer 85c91c97-e563-4ee8-acc1-aea288b42369',
}

dbPlayersLayout = "CREATE TABLE players ( \
    playerId VARCHAR(255) NOT NULL,       \
    name VARCHAR(255),                    \
    avatar VARCHAR(255),                  \
    country VARCHAR(255),                 \
    skillLevel VARCHAR(255),              \
    faceitElo VARCHAR(255),               \
    steamProfile VARCHAR(255),            \
    PRIMARY KEY (playerId))"