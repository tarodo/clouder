# Clouder
A service to help me collect new music from beatport and create playlists on music platforms.

Service can read html file of your playlist from [Beatport](https://www.beatport.com/library/playlists) and create new playlist in Spotify

## .env
For using Spotify you need to create new App in [Spotify Dashboard](https://developer.spotify.com/dashboard/applications)

You need to create `.env` file with:
1. SPOTIPY_CLIENT_ID - str, use [Spotify Dashboard](https://developer.spotify.com/dashboard/applications)
2. SPOTIPY_CLIENT_SECRET - str, use [Spotify Dashboard](https://developer.spotify.com/dashboard/applications)
3. SPOTIPY_REDIRECT_URI - str, Ex.: `http://localhost`

You need to create `.env` file in `./backend` directory:
1. DB_URL - str, string for DB connection
2. FIRST_SUPERUSER - str, admin email
3. FIRST_SUPERUSER_PASSWORD - str, admin pass

You need to create `.env` file in './db' directory:
1. POSTGRES_USER - default user
2. POSTGRES_PASSWORD - pass of the user

You need to create `.env` file in './bot' directory:
1. BOT_TOKEN - str, token from [BotFather](https://t.me/botfather)
2. RELEASE_URL - str, github url about the last release, e.g. `https://api.github.com/repos/tarodo/clouder/releases/latest`


## Start
### Start in Docker-compose
1. `docker-compose up --build`

### Start test
1. `docker-compose exec back python -m pytest --cov app`

## Contribute
### Schemas changes
1. `docker-compose exec back alembic revision --autogenerate -m "msg"`
2. `docker-compose exec back alembic upgrade head`

### Before commit
1. `black .\beatport.py .\models.py .\spotify.py .\backend\app\api\ .\backend\app\core\ .\backend\app\crud\ .\backend\app\models\ .\backend\tests\ .\bot\`
2. `isort .\beatport.py .\models.py .\spotify.py .\backend\app\api\ .\backend\app\core\ .\backend\app\crud\ .\backend\app\models\ .\backend\tests\ .\bot\`