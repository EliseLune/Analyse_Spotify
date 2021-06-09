import spotipy
import os
import sys
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import plotly
import plotly.graph_objs as go
import numpy as np
import json


def getTrackIDs(playlist_id,):
    ids = []
    playlist = sp.playlist(playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

def getTrackFeatures(id):
    meta = sp.track(id)
    features = sp.audio_features(id)
    return [meta['name'], 
            meta['album']['name'],
            meta['album']['artists'][0]['name'],
            meta['album']['release_date'],
            meta['duration_ms'], 
            meta['popularity'], 
            features[0]['acousticness'],
            features[0]['danceability'], 
            features[0]['energy'], 
            features[0]['instrumentalness'],
            features[0]['key'], 
             features[0]['liveness'], 
             features[0]['loudness'], 
             features[0]['mode'], 
             features[0]['speechiness'], 
             features[0]['tempo'], 
             features[0]['time_signature'], 
             features[0]['valence']]


def creat_df_audiofeatures(playlist_id):
    ids = getTrackIDs(playlist_id)
    tracks = []
    for i in range(len(ids)):
        track = getTrackFeatures(ids[i])
        tracks.append(track)
    return pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature','valence'])
    
def get_playlist_id(user_id):
    playlists = sp.user_playlists(user_id)
    res=[]
    ide=[]
    nom=[]
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            res.append((playlist['uri'].split(':')[2],playlist['name']))
            ide.append(playlist['uri'].split(':')[2])
            nom.append(playlist['name'])
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return res

# results = spotify.user_playlist(user=None, playlist_id="3cqDkXVInhOYPpJyVzvwux", fields="name")
# results["name"]

# Pour créer le plot de la playlist, pour l'instant seulement la dancebility
def create_plot(df):

    N,m = df.shape
    x = df['name'].tolist()
    y=df['danceability'].tolist()
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def get_playlists(items):
    name_playlists= []
    id_playlists=[]
    for dict in items:
        name_playlists.append(dict["name"])
        id_playlists.append(dict["id"])
    return name_playlists,id_playlists