import pandas as pd
from .extraction_spotipy import *
import streamlit as sp

def recommandation_souflee(playlist_id, audiofeatures,sp):
    
    #On ouvre la base de données dans playlist_cible
    playlist_cible = pd.read_csv('data_o.csv')

    #source est le dataframe des audiofeatures de la playlist pour faire la recommandation
    source = creat_df_audiofeatures(playlist_id,sp)
    playlist = [] #liste avec les artistes et les audiofeatures à changer
    for i in range (len(source)) : #pour chaque morceau de la playlist initiale
        playlist.append([source["artist"][i]]) #on ajoute l'artiste
        
        for audio in audiofeatures:#On boucle sur les audiofeatures pour les ajoutés à playlist
            playlist[i].append(source[audio][i])
        
        #on enleve nos morceaux de la playlist de la base de données
        playlist_cible.drop(playlist_cible.loc[playlist_cible['id']==source['id'][i]].index, inplace=True)

    nouvelle_playlist = [] #Liste des ID recommandés
    for i in range(len(playlist)):
        artist = source["artist"][i] #artiste cible

        #df est un dataframe avec seulemnt les morceaux de l'artiste en question
        df = all_tracks_of_one_artist(playlist_cible,artist)
        
        #Pour chaque audiofeature selectioné, on ne garde dans df que des morceaux similaires
        for j,audio in enumerate(audiofeatures):
            df = df[(df[audio] > playlist[i][j+1] -0.1) & (df[audio] > playlist[i][j+1] -0.1)]
        
        #On reset les indices de df
        df.reset_index(drop=True, inplace=True)

        n,m=df.shape
        if n!=0: #Si le dataframe est non vide après avoir éliminer les morceaux qui ne correspondent pas
            nouvelle_playlist.append(df["id"][0])
    return list(set(nouvelle_playlist))

#Renvoie une partie de paylist_cible avec seulement les morceaux de l'artiste demandé
def all_tracks_of_one_artist(playlist_cible,artist):
    return playlist_cible[playlist_cible["artists"].str.contains(artist)]