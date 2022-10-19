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

## Start
### Start in Docker-compose
1. `docker-compose up`

### Start test
1. `docker-compose exec quiz-back python -m pytest --cov app`

### Before commit
1. `black .\beatport.py .\models.py .\spotify.py .\backend\app\api\ .\backend\app\core\ .\backend\app\crud\ .\backend\app\models\ .\backend\tests\`
2. `isort .\beatport.py .\models.py .\spotify.py .\backend\app\api\ .\backend\app\core\ .\backend\app\crud\ .\backend\app\models\ .\backend\tests\`