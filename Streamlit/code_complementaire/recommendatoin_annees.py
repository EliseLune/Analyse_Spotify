import pandas as pd
from .extraction_spotipy import *
import streamlit as sp

def recommendation_year(id_to_change,year,sp):

    year = int(year)

    #On ouvre la base de données dans playlist_cible
    playlist_cible = pd.read_csv('data_o.csv')
    
    #source est le dataframe des audiofeatures de la playlist pour faire la recommandation
    source = creat_df_audiofeatures(id_to_change,sp)
    
    audiofeatures = ['valence','danceability','energy','instrumentalness','speechiness','acousticness'  ]

    playlist = [] #liste avec les artistes et les audiofeatures à changer
    for i in range (len(source)) : #pour chaque morceau de la playlist initiale
        playlist.append([release_date_to_year(source["release_date"][i])])
        for audio in audiofeatures:#On boucle sur les audiofeatures pour les ajoutés à playlist
            playlist[i].append(source[audio][i])
        
        #on enleve nos morceaux de la playlist de la base de données
        playlist_cible.drop(playlist_cible.loc[playlist_cible['id']==source['id'][i]].index, inplace=True)

    nouvelle_playlist = [] #Liste des ID recommandés
    for track in playlist:
        
        #df est un dataframe avec seulemnt les morceaux de l'artiste en question
        df = tracks_around_year(playlist_cible,year, 5)

        for i in range(len(track) -1):
            df_verife = df[(df[audiofeatures[i]] > track[i+1] -0.1) & (df[audiofeatures[i]] < track[i+1] +0.1)]
            a,b = df_verife.shape
            if a==0:
                break
            else:
                df=df_verife
        
        #On reset les indices de df
        df.reset_index(drop=True, inplace=True)

        nouvelle_playlist.append(df["id"][0])
        playlist_cible.drop(playlist_cible.loc[playlist_cible['id']==df["id"][0]].index, inplace=True)
    nouvelle_playlist = drop_doubles(nouvelle_playlist)
    return nouvelle_playlist

def tracks_around_year(playlist_cible,year, delta):
    return playlist_cible[(playlist_cible['year'] >= year -delta) & (playlist_cible['year'] <= year + delta)]

#on enlève les morceaux en double mais on garde l'ordre
def drop_doubles(playlist):
    res=[]
    for x in playlist:
        if x not in res:
            res.append(x)
    return res

def release_date_to_year(rd):
    year = rd[:4]
    return int(year)

def affichage_playlist_annees(nouvelle_playlist,sp):
    st.subheader('Voici les morceaux que vous nous recommendons.')
    names = [sp.track(trackie)["name"] for trackie in nouvelle_playlist]
    df = {'Track':names,
                'Artist':[get_artists(trackie,sp) for trackie in nouvelle_playlist],
                'Album':[sp.track(trackie)["album"]["name"] for trackie in nouvelle_playlist],
                'Release Date':[sp.track(trackie)['album']['release_date'] for trackie in nouvelle_playlist],
                'TrackId':nouvelle_playlist,}
    n=len(df["Track"])
    st.dataframe(df, height=30*(n+1))
    return 0