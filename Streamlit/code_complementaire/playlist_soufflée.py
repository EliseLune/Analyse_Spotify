import pandas as pd
from .extraction_spotipy import *

def recommandation_souflee(playlist_id, audiofeatures,sp):
    playlist_cible = pd.read_csv('data_o.csv')
    
    source = creat_df_audiofeatures(playlist_id,sp)
    playlist = [] #prendra l'énergie et l'accousticness de la musique
    for i in range (len(source)) :
        playlist.append([source["artist"][i]])
        for audio in audiofeatures:
            playlist[i].append(source[audio][i])
        playlist_cible.drop(playlist_cible.loc[playlist_cible['id']==source['id'][i]].index, inplace=True)
    return playlist