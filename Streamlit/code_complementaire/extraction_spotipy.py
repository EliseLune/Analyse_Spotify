import os
import sys
import pandas as pd
import numpy as np
import json
import streamlit as st

#Récupère tous les ID des morceaux d'une playlist
def getTrackIDs(playlist_id,sp):
    ids = []
    playlist = sp.playlist(playlist_id)
    for item in playlist['tracks']['items']:
        ids.append(item["track"]['id'])
    return ids

#Récupère les audiofeatures d'un morceau à partir de son ID
def getTrackFeatures(id,sp):
    meta = sp.track(id)
    features = sp.audio_features(id)
    return [id, meta['name'], 
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

#Créé un dataframe des audiofeatures d'une playlist à partie de son ID
def creat_df_audiofeatures(playlist_id,sp):
    ids = getTrackIDs(playlist_id,sp)
    tracks = []
    for i in range(len(ids)):
        track = getTrackFeatures(ids[i],sp)
        tracks.append(track)
    return pd.DataFrame(tracks, columns = ['id','name', 'album', 'artist', 'release_date', 'length', 'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature','valence'])

#Récupère les playlists (publiques!) d'un utilisateur avec son ID
# Plus utilisé dans cette version du code    
def get_playlist_id(user_id,sp):
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

#Crée 2 listes avec les noms et les ID de toutes les playlists de l'utilisateur (privés et publiques)
def get_playlists(items):
    name_playlists= []
    id_playlists=[]
    for dict in items:
        name_playlists.append(dict["name"])
        id_playlists.append(dict["id"])
    return name_playlists,id_playlists

#A partir du nom de la playlist, donne l'ID de la playlist. A besoin des 2 listes de la fonction précédente
def name_to_id(names,ids,name_to_search):
    numero = names.index(name_to_search)
    return ids[numero]

#Liste d'ID recommandés avec l'outil recommandation de spotipy
def premiere_recommandation(playlist_id,sp):
    tracks = getTrackIDs(playlist_id,sp)
    reco = []
    for track in tracks:
        artist_id = sp.track(tracks[0])["artists"][0]["id"]
        res = sp.recommendations(seed_tracks = [tracks[0]],seed_artist=artist_id, limit=1, traget_valence=sp.audio_features(track)[0]['valence'])
        reco.append(res["tracks"][0]["id"])
    return reco

#Enumère les artistes d'un morceau sous forme d'un string
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

#Utilise première recommandation pour retourné un dataframe des morceaux recommandés
def mise_en_forme(id_to_change,sp):
    res = premiere_recommandation(id_to_change,sp)
    names = [sp.track(trackie)["name"] for trackie in res]
    return {'Track':names,
            'Artist':[get_artists(trackie,sp) for trackie in res],
            'Album':[sp.track(trackie)["album"]["name"] for trackie in res],
            'TrackId':res,}

#Retourne une liste avec tous les ID différents de l'utilisateur
def all_tracks(playlists,sp):
    all_tracks=[]
    for playlist in playlists:
        tracks = getTrackIDs(playlist,sp)
        all_tracks = all_tracks + tracks
    return list(set(all_tracks))

#Liste de tous les ID des artistes différents
def all_artists(playlists,sp):
    res=[]
    for playlist in playlists:
        intermediaire = sp.playlist(playlist)
        tracks=intermediaire["tracks"]["items"]
        for track in tracks:
            for artist in track["track"]["artists"]:
                res.append(artist["id"])
    return list(set(res))

#Enumere les top artistes de l'utilisateur
def top_artist_to_string(top_artists):
    tutu=top_artists["items"]
    res=""
    for artist in tutu[:-1]:
        res = res + artist["name"] + ', '
    res = res + tutu[-1]["name"]
    return res

#Associe l'abréviation du pays à son nom complet
def country(string):
    countries = {"AD": "Andorre", "AE": "Emirats Arabes Unis" , "AR" : "Argentine","AT": "Autriche", "AU": "Australie",
    "BE": "Belgique","BG": "Bulgarie","BH": "Barhain","BO": "Bolivie","BR": "Brésil","CA": "Canada","CH": "Suisse","CL": "Chili",
    "CO": "Colombie","CR": "Costa Rica","CY": "Chypre","CZ": "République Tchèque","DE": "Allemagne","DK": "Danemark","DO": "République Dominicaine","DZ": "Algérie",
    "EC": "Equateur","EE": "Estonie","EG": "Egypte","ES": "Espagne","FI": "Finland","FR": "France","GB": "Royaume Uni","GR": "Grèce",
    "GT": "Guatemala","HK": "Hong Kong","HN": "Honduras","HU": "Hongrie","ID": "Indonésie","IE": "Irlande","IL": "Israël","IN": "Inde","IS": "Islande",
    "IT": "Italie","JO": "Jordanie","JP": "Japon","KW": "Koweït","LB": "Liban","LI": "Liechtenstein","LT": "Lituanie","LU": "Luxembourg","LV": "Lettonie",
    "MA": "Maroc","MC": "Monaco","MT": "Malte","MX": "Mexique","MY": "Malaisie","NI": "Nicaragua","NL": "Pays-Bas","NO": "Norvège","NZ": "Nouvelle-Zélande",
    "OM": "Oman","PA": "Panama","PE": "Pérou","PH": "Philippines","PL": "Pologne","PS": "Palestine",
    "PT": "Portugal","PY": "Paraguay","QA": "Qatar","RO": "Roumanie","SA": "Arabie Saoudite","SE": "Suède",
    "SG": "Singapour","SK": "Slovaquie","SV": "El Salvador","TH": "Thaïlande","TN": "Tunisie","TR": "Turquie",
    "TW": "Taïwan","US": "États-Unis","UY": "Uruguay","VN": "Viet Nam","ZA": "Afrique du Sud",
    "RU":"Russie","BY":"Bélarus","KZ":"Kazakhstan","MD":"Moldavie","UA":"Ukraine","AL":"Albanie","BA":"Bosnie-Herzégovine",
    "HR":"Croatie","ME":"Monténégro","MK":"Macédoine du Nord","SM":"Saint-Marin","RS":"Serbie","SI":"Slovénie","XK":"Kosovo",
    "GY":"Guyana","SR":"Suriname","FJ":"Fiji","KI":"Kiribati","MH":"Iles Marshall","FM":"Micronésie","NR":"Nauru",
    "PW":"Palaos","PG":"Papouasie-Nouvelle-Guinée","WS":"Samoa","SB":"Iles Salomon","TV":"Tuvalu","VU":"Vanuatu",
    "AG":"Antigua-et-Barduba","BS":"Bahamas","BB":"Barbade","BZ":"Belize","CW":"Curaçao","DM":"Dominique","GD":"Grenade",
    "JM":"Jamaïque","KN":"Saint-Kitts-et-Nevis","LC":"Saint Lucie","VC":"Saint-Vincent-et-les-Grenadines","TT":"Trinité-et-Tobago","AO":"Angola","BJ":"Benin",
    "BW":"Botswana","BF":"Burkina Faso","BI":"Burundi","CM":"Cameroun","CV":"Cap-Vert","TD":"Tchad","KM":"Comores",
    "CI":"Côte d'Ivoire","DJ":"Djibouti","GQ":"Guinée Equatoriale","SZ":"Eswatini","GA":"Gabon","GM":"Gambie","GH":"Ghana",
    "GN":"Guinée","GW":"Guinée-Biseau","KE":"Kenya","LS":"Lesotho","LR":"Libéria","MG":"Madagascar","MW":"Malawi","TO":"Tonga",
    "ML":"Mali","MR":"Mauritanie","MU":"Maurice","MZ":"Mozambique","NA":"Namibie","NE":"Niger","NG":"Nigeria","RW":"Rwanda","ST":"São Tomé-et-Principe","SN":"Sénégal",
    "SC":"Seychelles","SL":"Sierra Leone","TZ":"Tanzanie","TG":"Togo","UG":"Ouganda","ZM":"Zambie","ZW":"Zimbabwe","AM":"Arménie","AZ":"Azebaïdjan",
    "BD":"Bangladesh","BT":"Bhoutan","BN":"Brunei","KH":"Cambodge","GE":"Géorgie","KG":"Kirgizistan","LA":"Laos","MO":"Macao","MV":"Maldives",
    "MN":"Mongolie","NP":"Nepal","PK":"Pakistan","KR":"Corée du Sud","LK":"Sri Lanka","TL":"Timor Oriental","UZ":"Ouzbékistan"}
    return countries[string]

#une autre possibilité de recommandation
#set = mise_en_forme(id_to_change,sp)
#n=len(set["Track"])
#st.dataframe(set, height=30*(n+1))