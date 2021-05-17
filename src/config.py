# standard image if player has no avatar
avatarPng = "https://img.favpng.com/8/24/4/avatar-royalty-free-png-favpng-6920SU0BFdaEZTMCMSsrTTPws.jpg"

# header to connect to faceit API
headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer 85c91c97-e563-4ee8-acc1-aea288b42369',
}

# MySQL player table layout
dbPlayersLayout = "CREATE TABLE players ( \
    playerId VARCHAR(255) NOT NULL,       \
    name VARCHAR(255),                    \
    avatar VARCHAR(255),                  \
    country VARCHAR(255),                 \
    skillLevel VARCHAR(255),              \
    faceitElo VARCHAR(255),               \
    steamProfile VARCHAR(255),            \
    PRIMARY KEY (playerId))"
