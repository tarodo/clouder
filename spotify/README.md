# Spotify Service
Service for creation new playlist and release preparing

## .env
For using Spotify you need to create new App in [Spotify Dashboard](https://developer.spotify.com/dashboard/applications)

You need to create `.env` file with:
- SPOTIPY_CLIENT_ID - str, use [Spotify Dashboard](https://developer.spotify.com/dashboard/applications)
- SPOTIPY_CLIENT_SECRET - str, use [Spotify Dashboard](https://developer.spotify.com/dashboard/applications)
- SPOTIPY_REDIRECT_URI - str, Ex.: `http://localhost`

## Token registration
After docker-compose up use:
```shell
docker-compose exec spotify python reg.py
```