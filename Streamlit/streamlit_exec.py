import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_une_page import MultiApp
import os
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from spotipy.cache_handler import CacheHandler
from data_collector.secrets_spotify import client_id,client_secret,redirect_uri
from data_collector.spotify_connector import get_spotipy
from streamlit import caching
import numpy as np
from code_complementaire.extraction_spotipy import *

@st.cache(allow_output_mutation=True)
def get_spotipy_ready():
    scope = "playlist-read-private user-read-email user-read-private playlist-modify-private user-top-read"
    sp = get_spotipy(scope, client_id,client_secret,redirect_uri)
    res=sp.current_user
    return sp

def recup_noms_playlists_user(ident,secret,nombre):
    client_credentials_manager = SpotifyClientCredentials(client_id=ident, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlists = sp.user_playlists(nombre)
    L=[]
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            tab= playlist['uri'].split(':')
            L.append(playlist['name'])
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return L

#Test de laffichage dun graphique avec un playlist:
def test_data(data_csv,liste_feat):
    data=pd.read_csv(data_csv)
    data["release_year"]=date_to_year(data['release_date'])
    y = data['release_year'].value_counts()
    for aud_feat in liste_feat:
        #On peut faire une boucle for pour afficher les graphs de tous les audiofeatures sélectionnés
        #Et faire des if pour afficher un type de graph différent selon l'audiofeature?
        if aud_feat=='release_year':
            fig2,ax2=plt.subplots()
            ax2.bar(y.index,y)
            ax2.set_title('release_date')
            st.pyplot(fig2)
        else:
            fig1,ax1=plt.subplots()
            ax1.hist(data[aud_feat])
            ax1.set_title(aud_feat)
            st.pyplot(fig1)
    return None

def date_to_year(date):
    return int(date[:4])
date_to_year = np.vectorize(date_to_year)

def accueil():
    caching.clear_cache()
    st.title('SpotData')
    st.write('Par P.Vehrlé, J.Delaplace, C.Nothhelfer, E.Lei')
    st.write('SpotData est une Webapp vous proposant de faire analyser vos playlists Spotify, et de découvrir encore plus de musiques qui vous correspondent.')
    st.write("Vous allez être redirigé vers une page d'autentification. Une fois cette dernière finie, revenez sur cette page")
    textPlaceholder = st.empty()
    click = textPlaceholder.button("Se connecter à Spotify")
    if click:
        textPlaceholder.text("Vous êtes connecté. Vous pouvez allez naviguer sur le reste de l'application.")
        sp = get_spotipy_ready()
        res = sp.current_user()
    return None

def apres_auth():
    st.title('SpotData')
    sp = get_spotipy_ready()
    user_info = sp.current_user()
    st.header("Bienvenue, {}".format(user_info['display_name']))
    # st.image('Desktop/spotify_profil_mockup.png')

    st.subheader('Mes informations')
    if user_info["images"]!=[]:
        st.image(user_info["images"][0]["url"])
    if user_info["email"]!=[]:
        st.write("E-mail : {}".format(user_info["email"]))
    if user_info["country"]!=[]:
        st.write("Pays : {}".format(user_info["country"]))

    playlists = liste_playlists_id(sp.current_user_playlists(),sp)
    st.subheader('Pour commencer, une vision d\'ensemble de votre musique')
    st.write('Statistiques globales:')
    st.write('  - Nombre de playlists : {}'.format(len(playlists)))
    st.write('  - Nombre de titres enregistrés : {}'.format(len(all_tracks(playlists,sp))))
    st.write('  - Nombre d\'artistes écoutés : {}'.format(len(all_artists(playlists,sp))))
    st.write('Top 5 des artistes écoutés')
    st.write('Musique la plus écoutée:')
    st.write('Petit texte "Votre musique semble plutôt" [adjectif déterminé à partir de moyennes d\'audio-features]')
    return None


def analyse():
    sp = get_spotipy_ready()
    playlists = sp.current_user_playlists()
    name_playlists, id_playlists = get_playlists(playlists["items"])
    st.title('SpotData')
    st.header('Analyse de vos playlists')
    st.write('Nombre dans la playlist+durée d\'écoute totale')
    st.write('(Texte d\'analyse=>Playlist sport/tranquille etc.-pas prioritaire-)')
    box=st.selectbox('Vos playlists: ',name_playlists)
    a=st.multiselect('Audio-Features',['dansability','energy','speechiness','acousticness','instrumentalness','popularity','release_year','valence'])
    if a!=[]:
        test_data('df_example_01-Copy1.csv',a)
    #if a!=[]:
        #st.subheader('Vous avez choisi: **{}**'.format(a))
        #l=len(a)
        #if l==1:
            #fig,ax=plt.subplots()
            #ax.set_title('Histogramme de: '+a[0])   
        #else:
            #fig,ax=plt.subplots(1,l,figsize=(10,l//2))
            #i=0
            #for value in a:
                #ax[2*i//l].set_title('Histogramme de: '+value)
                #i+=1
                #if i==l:
                    #break
        #st.pyplot(fig)
        #if l>2:
            #st.write('Nuage de points')
            #fig,ax=plt.subplots(1,l,figsize=(10,l//2))
            #for j in (0,l-1):
                #ax[2*j//l].set_title('Nuage de points de: '+a[j]+', '+a[j+1])
                #ax[2*j//l].set_xlabel(a[j])
                #ax[2*j//l].set_ylabel(a[j+1])
            #st.pyplot(fig)
        #elif l==2:
            #st.write('Nuage de points')
            #fig,ax=plt.subplots(1,l-1,figsize=(10,l//2))
            #ax.set_title('Nuage de points de: '+a[0]+', '+a[1])
            #ax.set_xlabel(a[0])
            #ax.set_ylabel(a[1])
            #i+=1
            #st.pyplot(fig)  
    return None

def recommandation():
    sp = get_spotipy_ready()
    playlists = sp.current_user_playlists()
    name_playlists, id_playlists = get_playlists(playlists["items"])
    st.title('SpotData')
    st.header('Recommandation de playlists')
    st.subheader('A partir de vos playlists, nous vous en proposons des nouvelles, de plusieurs manières différentes.')

    #Choix de la playlist
    st.subheader('A partir de quelle playlist souhaitez-vous en obtenir une nouvelle?')
    playlist_to_change=st.selectbox('Vos playlists: ',name_playlists)
    recommande=st.button("C'est parti !")
    id_to_change=name_to_id(name_playlists,id_playlists,playlist_to_change)
    
    # if recommande:
    st.write('Pour l\'instant, 1 seul type de recommandations')
    data={'Track':['Track 1','Track 2','...'],
            'Artist':['Artist 1','Artist 2','...'],
            'Album':['Album 1','Album 2','...'],
            'TrackId':['TrackId 1','TrackId 2','...'],}
    pd_data=pd.DataFrame(data)
    st.dataframe(pd_data)

    st.dataframe(mise_en_forme(id_to_change,sp))

    # Création de la playlist sur Spotify
    nom_playlist = st.text_input('Nom de ma nouvelle playlist', value="New {}".format(playlist_to_change))
    textPlaceholder = st.empty()
    click = textPlaceholder.button("Ajouter cette playlist dans Spotify")
    if click:
        textPlaceholder.text("Votre playlist a bien été créée. Allez sur Spotify pour l'écouter.")
        st.write(nom_playlist)
        sp = get_spotipy_ready()
        user_info = sp.current_user()
        new_playlist = sp.user_playlist_create(user_info["id"],nom_playlist, public=False)
        new_playlist_id = new_playlist["id"]
        # a décommenter quand on aura toute l'analyse
        # sp.user_playlist_add_tracks(user_info["id"], new_playlist_id, liste_des_tracks_a_ajouter)

    #LA SUITE SERVIRA PEUT-ÊTRE PLUS TARD
    #if b=='Playlist sur critères':
        #c=st.multiselect('Critères choisis: ',['Dansabilité','Energie','Speechiness','Tempo','Valence'])
        #if c!=[]:
            #st.write('Vous avez choisi: ')
            #for i in range(0,len(c)):
                #st.write(c[i])
                #st.write('Description des valeurs que peut prendre '+c[i])
                #st.slider('Valeur de '+c[i],min_value=0.,max_value=1.,step=0.33)
            #data={'Track':['Track 1','Track 2','...'],
            #'Artist':['Artist 1','Artist 2','...'],
            #'Album':['Album 1','Album 2','...'],
            #'TrackId':['TrackId 1','TrackId 2','...'],}
            #pd_data=pd.DataFrame(data)
            #st.dataframe(pd_data)
            #st.button('Télécharger ma playlist')
    #elif b=='Playlist souffle':
        #st.write('Description de ce qu\'est la playlist souffle')
        #data={'Track':['Track 1','Track 2','...'],
        #'Artist':['Artist 1','Artist 2','...'],
        #'Album':['Album 1','Album 2','...'],
        #'TrackId':['TrackId 1','TrackId 2','...'],}
        #pd_data=pd.DataFrame(data)
        #st.dataframe(pd_data)
        #st.button('Télécharger ma playlist')
    return None

def glossaire():
    st.title('SpotData')
    st.header('Glossaire')
    st.write('Vous trouverez sur cette page une définition des différents audiofeatures, donnée par la documentation de Spotify. La plupart de ces indices sont mesurés entre 0 et 1.')
    gloss={'Audio-features (Traduction? Caractéristique/Paramètre':['Danceability','Speachiness','...'],
            'Description':['Description compréhensible de Danceability','Description compréhensible de Speechiness','...'],
            'Intervalle':['[0,1] : De Podcast à Musique Club','[0,1]: De Techno à Gospel','...'],}
    pd_gloss=pd.DataFrame(gloss)

    st.markdown("___Acousticness___")
    st.write("L'acoustiness mesure l'acoustic du morceau. Plus il est proche de 1, plus il y a de chance que le morceau soit acoustique (avec des instruments non synthétiques).")
    st.markdown("___Danceability___")
    st.write("La dansabilité mesure si un morceau est adapté à la danse à partir d'élements musicaux comme le tempo, la stabilité du rythme, la force de la rythmique. A 0, un morceau est très peu adapté à la danse alors qu'à 1 est un morceau très dansable.")
    st.markdown("___Energy___")
    st.write("L'énergie mesure la perception de l'intensité et de l'activité. Typiquement, les morceaux énergiques semblent rapides, forts et bruyant. Par exemple, le death metal est à haute énergie alors qu'un prélude de Bach est bas dans cette échelle. Les caractéristiques qui servent a créer cette donnée sont la sonorité perçue, le timbre, la vitesse d'apparition et l'entropie générale.")
    st.markdown("___Instrumentalness___")
    st.write("Cet indice mesure si un morceau contient des voix. Plus l'indice est proche de 1, plus il est certain qu'il n'y a aucune voix. Une valeur au dessus de 0.5 tend à être un morceau instrumental mais la probabilité augmente quand on s'approche de 1.")
    st.markdown("___Liveness___")
    st.write("La liveness permet de détecter la présence d'une audience dans l'enregistrement. Plus l'indice est proche de 1, plus il est probable que le morceau est live. Au dessus de 0.8, il est quasiment certain que l'enregistrement a été fait en live.")
    st.markdown("___Loudness___")
    st.write("Le bruit est le seul paramètre qui n'est pas mesuré entre 0 et 1 mais sur une échelle de -60 dB à 0dB. Cette mesure est moyennée sur l'ensemble.")
    st.markdown("___Speechness___")
    st.write("Cet indice détecte la présence de parties parlées. Les enregistrements parlés (type poèmes, talk show, podcast) seront proche de 1. Au dessus de 0.66, l'enregistrement est probablement entièrement consitué de paroles. Entre 0.33 et 0.66, il y aura des paroles et de la musique, soit en alternance ou dans les cas comme le rap. En dessous de 0.33, il est probable que l'enregistrement soit de la musique, sans parties parlées.")
    st.markdown("___Valence___")
    st.write("Plus la valence est haute, plus le morceau est joyeux. A l'inverse, plus la valence est faible, plus le morceau est triste.")

    st.subheader("Pour avoir plus d'information,")
    st.write("[Visitez ce site](https://rpubs.com/PeterDola/SpotifyTracks)")
    # st.table(pd_gloss)
    return None

def apropos():
    st.title('SpotData')
    st.header('A propos')
    st.write('SpotData est une WebApp développée par 4 élèves de l\'école Mines Paristech (nos noms) dans le cadre d\'un projet d\'informatique.')
    st.write("Le but est d\'analyser des playlists Spotify et de proposer des recommandations grâce au module python Spotipy. Cette application est développée à l'aide de Streamlit")
    st.write('[Lien du dépot Github du projet](https://github.com/EliseLune/Analyse_Spotify)')
    st.write('[Lien du site des Mines](https://www.minesparis.psl.eu/)')
    return None
app = MultiApp()
app.add_app("Se déconnecter", accueil)
app.add_app("Accueil", apres_auth)
app.add_app("Analyse", analyse)
app.add_app("Recommandations", recommandation)
app.add_app("Glossaire",glossaire)
app.add_app("A propos",apropos)
app.run()
