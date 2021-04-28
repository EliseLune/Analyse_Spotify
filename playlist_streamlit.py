import streamlit as st
import pandas as pd

st.set_page_config(page_title='Accueil après authentification',initial_sidebar_state="expanded")

def main():
    ac_sidebar()
    ac_body()
    return None

def ac_sidebar():
    st.sidebar.write('Analyse')
    st.sidebar.write('Recommandations')
    st.sidebar.write('A propos')
    return None

def ac_body():
    st.title('SpotData')
    st.subheader('Quel type de playlist souhaitez-vous obtenir?')
    b=st.selectbox('Types de playlists: ',['Choisissez une playlist','Playlist souffle','Playlist sur critères'])
    if b=='Playlist sur critères':
        c=st.multiselect('Critères choisis: ',['Dansabilité','Energie','Speechiness','Tempo','Valence'])
        if c!=[]:
            st.write('Vous avez choisi: ')
            for i in range(0,len(c)):
                st.write(c[i])
                st.write('Description des valeurs que peut prendre '+c[i])
                st.slider('Valeur de '+c[i],min_value=0.,max_value=1.,step=0.33)
            data={'Track':['Track 1','Track 2','...'],
            'Artist':['Artist 1','Artist 2','...'],
            'Album':['Album 1','Album 2','...'],
            'TrackId':['TrackId 1','TrackId 2','...'],}
            pd_data=pd.DataFrame(data)
            st.dataframe(pd_data)
            st.button('Télécharger ma playlist')
    elif b=='Playlist souffle':
        st.write('Description de ce qu\'est la playlist souffle')
        data={'Track':['Track 1','Track 2','...'],
        'Artist':['Artist 1','Artist 2','...'],
        'Album':['Album 1','Album 2','...'],
        'TrackId':['TrackId 1','TrackId 2','...'],}
        pd_data=pd.DataFrame(data)
        st.dataframe(pd_data)
        st.button('Télécharger ma playlist')
    return None
    
if __name__=='__main__':
    main()