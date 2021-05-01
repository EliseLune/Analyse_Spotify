import os
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from spotipy.cache_handler import CacheHandler

# os.chdir("data_collector")
# print(os.getcwd())
from data_collector.secrets_spotify import client_id,client_secret,redirect_uri
from data_collector.spotify_connector import get_spotipy



sp = get_spotipy("playlist-read-private", client_id,client_secret,redirect_uri)

res2 = sp.current_user()
print(res2)
res = sp.current_user_playlists()
print(res['items'])