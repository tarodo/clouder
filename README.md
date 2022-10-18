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