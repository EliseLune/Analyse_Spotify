import pandas as pd
from .extraction_spotipy import *
import streamlit as sp

def recommandation_souflee(playlist_id, audiofeatures,sp):
    playlist_cible = pd.read_csv('data_o.csv')
    source = creat_df_audiofeatures(playlist_id,sp)
    playlist = [] #prendra l'énergie et l'accousticness de la musique
    for i in range (len(source)) :
        playlist.append([source["artist"][i]])
        for audio in audiofeatures:
            playlist[i].append(source[audio][i])
        #on enleve nos morceaux de la playlist de la base de données
        playlist_cible.drop(playlist_cible.loc[playlist_cible['id']==source['id'][i]].index, inplace=True)

    nouvelle_playlist = []
    for i in range(len(playlist)):
        artist = source["artist"][i]
        df = all_tracks_of_one_artist(playlist_cible,artist)
        #jusque là ça marche bien. Maintenant je veux selectionner un morceau adapté
        for j,audio in enumerate(audiofeatures):
            df = df[(df[audio] > playlist[i][j+1] -0.1) & (df[audio] > playlist[i][j+1] -0.1)]
        df.reset_index(drop=True, inplace=True)
        nouvelle_playlist.append(df["id"][0])
    return nouvelle_playlist

#maybe i'll have to define i with the id of the track
#returns a dataframe with only the first artist of the track
def get_artists_to_list(playlist_cible,i): 
    res = playlist_cible.iloc[i]['artists']
    res_list  = list(res[1:-1].split(","))
    final=[]
    for artist in res_list:
        if artist[0]=="'":
            final.append(artist[1:-1])
        if artist[0]==" ":
            final.append(artist[2:-1])
    return playlist_cible[playlist_cible["artists"].str.contains(get_artists_to_list(i)[0])]

#Renvoie une partie de paylist_cible avec seulement les morceaux de l'artiste demandé
def all_tracks_of_one_artist(playlist_cible,artist):
    return playlist_cible[playlist_cible["artists"].str.contains(artist)]