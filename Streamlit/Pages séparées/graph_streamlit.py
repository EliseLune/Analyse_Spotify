###PAGE OU L'UTILISATEUR PEUT VOIR L'ANALYSE DE SES DONNEES###

import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title='Mes graphiques',layout="wide",initial_sidebar_state="expanded")

def main():
    ac_sidebar()
    ac_body()
    return None
def ac_sidebar():
    st.sidebar.write('Deconnexion')
    st.sidebar.write('Recommandations')
    st.sidebar.write('A propos')
    return None
def ac_body():
    st.title('SpotData')
    st.header('Analyse de vos playlists')
    st.selectbox('Choix de la playlist à analyser:',['Playlist1','Playlist2','etc'])
    a=st.multiselect('Audio-Features',['Dansabilité','Energie','Speechiness','Tempo','Valence'])
    if a!=[]:
        st.subheader('Vous avez choisi: **{}**'.format(a))
        for k in a:
            st.write (description(k))
        st.write ('Moyenne:...')
        st.write ('Appréciation:...')
        st.write ('Répartition:')
        st.write('Histogrammes')
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

    st.subheader('Envie de créer une playlist personnalisée?')
    st.button('Cliquez ici')
    return None

def description(a):
    if a=='Dansabilité':
        return('Ceci est une description de la dansabilité')
    elif a=='Energie':
        return('Ceci est une description de l\'énergie')
    elif a=='Speechiness':
        return('Ceci est une description de "Speechiness"')
    elif a=='Tempo':
        return('Ceci est une description du tempo')
    elif a=='Valence':
        return('Ceci est une description de la valence')

if __name__=='__main__':
    main()