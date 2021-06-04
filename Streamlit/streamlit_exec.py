import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_une_page import MultiApp


def accueil():
    st.title('SpotData')
    st.write('Par P.Vehrlé, J.Delaplace, C.Nothhelfer, E.Lei')
    st.write('SpotData est une Webapp vous proposant de faire analyser vos playlists Spotify, et de découvrir encore plus de musiques qui vous correspondent.')
    st.button('SE CONNECTER')
    return None

def apres_auth():
    st.title('SpotData')
    st.header('Bienvenue, [Nom de l\'utilisateur]!')
    st.image('Desktop/spotify_profil_mockup.png')
    st.write('Infos utilisateur')
    st.write('E-mail')
    st.write('Pays')
    st.subheader('Pour commencer, une vision d\'ensemble de votre musique')
    st.write('Statistiques globales:')
    st.write('  - Nombre de playlists')
    st.write('  - Nombre de titres enregistrés')
    st.write('  - Nombre d\'artistes écoutés')
    st.write('Top 5 des artistes écoutés')
    st.write('Musique la plus écoutée:')
    st.write('Petit texte "Votre musique semble plutôt" [adjectif déterminé à partir de moyennes d\'audio-features]')
    return None


def graph():
    st.title('SpotData')
    st.header('Analyse de vos playlists')
    st.write('Nombre dans la playlist+durée d\'écoute totale')
    st.write('(Texte d\'analyse=>Playlist sport/tranquille etc.-pas prioritaire-)')
    st.selectbox('Choix de la playlist à analyser:',['Playlist1','Playlist2','etc'])
    a=st.multiselect('Audio-Features',['Dansabilité','Energie','Speechiness','Tempo','Valence'])
    if a!=[]:
        st.subheader('Vous avez choisi: **{}**'.format(a))
        l=len(a)
        if l==1:
            fig,ax=plt.subplots()
            ax.set_title('Histogramme de: '+a[0])   
        else:
            fig,ax=plt.subplots(1,l,figsize=(10,l//2))
            i=0
            for value in a:
                ax[2*i//l].set_title('Histogramme de: '+value)
                i+=1
                if i==l:
                    break
        st.pyplot(fig)
        if l>2:
            st.write('Nuage de points')
            fig,ax=plt.subplots(1,l,figsize=(10,l//2))
            for j in (0,l-1):
                ax[2*j//l].set_title('Nuage de points de: '+a[j]+', '+a[j+1])
                ax[2*j//l].set_xlabel(a[j])
                ax[2*j//l].set_ylabel(a[j+1])
            st.pyplot(fig)
        elif l==2:
            st.write('Nuage de points')
            fig,ax=plt.subplots(1,l-1,figsize=(10,l//2))
            ax.set_title('Nuage de points de: '+a[0]+', '+a[1])
            ax.set_xlabel(a[0])
            ax.set_ylabel(a[1])
            i+=1
            st.pyplot(fig)  
    return None

def playlist():
    st.title('SpotData')
    st.header('Recommandation de playlists')
    st.subheader('A partir de vos playlists, nous vous en proposons des nouvelles, de plusieurs manières différentes.')
    st.subheader('A partir de quelle playlist souhaitez-vous en obtenir une nouvelle?')
    b=st.selectbox('Vos playlists: ',['Choisissez une playlist','Tous vos titres','Playlist 1','Playlist 2','...'])
    st.write('Pour l\'instant, 1 seul type de recommandations')
    data={'Track':['Track 1','Track 2','...'],
            'Artist':['Artist 1','Artist 2','...'],
            'Album':['Album 1','Album 2','...'],
            'TrackId':['TrackId 1','TrackId 2','...'],}
    pd_data=pd.DataFrame(data)
    st.dataframe(pd_data)
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
    st.write("L'acoustiness mesure l'acoustic du morceau. Plus il est proche de 1, plus il y a de chance que le morceau soit acoustique (avec des instruments non synthétiques.")
    st.markdown("___Danceability___")
    st.write("La dansabilité mesure si un morceau est adapté à la danse à partir d'élements musicaux comme le tempo, la stabilité du rythme, la force de la rythmique. A 0, un morceau est très peu adapté à la danse alors qu'à 1 est un morceau trus dansable.")
    st.markdown("___Energy___")
    st.write("L'énergie mesure la perception de l'intensité et de l'activité. Typiquement, les morceaux énergiques semblent rapides, forts et bruyant. Par exemple, le death metal est à haute énergie alors qu'un prélude de Bach est bas dans cette échelle. Les caractérisitques qui servent a créer cette donnée sont la sonorité perçue, le timbre, la vitesse d'apparition et l'entropie générale.")
    st.markdown("___Instrumentalness___")
    st.write("Cet indice mesure si un morceau contient des voix. Plus l'indice est proche de 1, plus il est certain qu'il n'y a aucune voix. Une valeur au dessus de 0.5 tend à être un morceau instrumentaux mais la probabilité augmente quand on s'approche de 1.")
    st.markdown("___Liveness___")
    st.write("La liveness permet de détecter la présence d'une audience dans l'enregistrement. Plus l'indice est proche de 1, plus il est probable que le morceau est live. Au dessus de 0.8, il est quasiment certain que l'enregistrement a été fait en live.")
    st.markdown("___Loudness___")
    st.write("Le bruit est le seul paramètre qui n'est pas mesuré entre 0 et 1 mais sur une échelle de -60 dB à 0dB. Cette mesure est moyennée sur l'ensemble.")
    st.markdown("___Speechness___")
    st.write("Cet indice détecte la présence de parties parlées. Les enregistrements parlés (type poèmes, talk show, podcast) seront proche de 1. Au dessus de 0.66, l'enregistrement est probablement entièrement consitué de paroles. Entre 0.33 et 0.66, il y aura des paroles et de la musique, soit en alternance ou dans les cas comme le rap. En dessous de 0.33, il est probable que l'enregistrement soit de la musique, sans parties parlées.")
    st.markdown("___Valence___")
    st.write("Plus la valence est haute, plus le morceau est joyeux. A l'inverse, plus la valence est faible, plus le morceau est triste.")

    st.table(pd_gloss)
    return None

def apropos():
    st.title('SpotData')
    st.header('A propos')
    st.write('SpotData est une WebApp développée par 4 élèves de l\'école Mines Paristech (nos noms) dans le cadre d\'un projet d\'informatique.')
    st.write('Le but est d\'analyser des playlists Spotify et de proposer des recommandations grâce au module python Spotipy')
    st.write('Lien du dépot Github du projet:')
    st.write('Lien du site des Mines:')
    return None
app = MultiApp()
app.add_app("Se déconnecter", accueil)
app.add_app("Accueil", apres_auth)
app.add_app("Mes Graphiques", graph)
app.add_app("Recommandations", playlist)
app.add_app("Glossaire",glossaire)
app.add_app("A propos",apropos)
app.run()
