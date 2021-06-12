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
import streamlit as st


def getTrackIDs(playlist_id,sp):
    ids = []
    playlist = sp.playlist(playlist_id)
    for item in playlist['tracks']['items']:
        ids.append(item["track"]['id'])
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

def name_to_id(names,ids,name_to_search):
    numero = names.index(name_to_search)
    return ids[numero]


def premiere_recommandation(playlist_id,sp):
    tracks = getTrackIDs(playlist_id,sp)
    reco = []
    for track in tracks:
        artist_id = sp.track(tracks[0])["artists"][0]["id"]
        res = sp.recommendations(seed_tracks = [tracks[0]],seed_artist=artist_id, limit=1, traget_valence=sp.audio_features(track)[0]['valence'])
        reco.append(res["tracks"][0]["id"])
    return reco

def get_artists(track_id,sp):
    liste_artists = sp.track(track_id)["artists"]
    res= []
    for truc in liste_artists:
        res.append(truc["name"])
    str = ''
    for artist in res[:-1]:
        str = str + artist +', '
    str = str + res[-1]
    return str

def mise_en_forme(id_to_change,sp):
    res = premiere_recommandation(id_to_change,sp)
    names = [sp.track(trackie)["name"] for trackie in res]
    return {'Track':names,
            'Artist':[get_artists(trackie,sp) for trackie in res],
            'Album':[sp.track(trackie)["album"]["name"] for trackie in res],
            'TrackId':res,}

def all_tracks(playlists,sp):
    all_tracks=[]
    for playlist in playlists:
        tracks = getTrackIDs(playlist,sp)
        all_tracks = all_tracks + tracks
    return list(set(all_tracks))

def liste_playlists_id(truc,sp):
    res=[]
    for dico in truc["items"]:
        res.append(dico["id"])
    return res

def all_artists(playlists,sp):
    res=[]
    for playlist in playlists:
        intermediaire = sp.playlist(playlist)
        tracks=intermediaire["tracks"]["items"]
        for track in tracks:
            for artist in track["track"]["artists"]:
                res.append(artist["id"])
    return list(set(res))

def artists_to_list(top_artists):
    tutu=top_artists["items"]
    res=""
    for artist in tutu[:-1]:
        res = res + artist["name"] + ', '
    res = res + tutu[-1]["name"]
    return res
