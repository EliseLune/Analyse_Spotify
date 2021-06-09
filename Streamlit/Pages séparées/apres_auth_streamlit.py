import streamlit as st

st.set_page_config(page_title='Accueil après authentification',initial_sidebar_state="expanded")

def main():
    ac_body()
    return None

def ac_body():
    st.title('SpotData')
    st.header('Bienvenue, [Nom de l\'utilisateur]!')
    st.subheader('Que souhaitez-vous obtenir?')
    st.write('Mes analyses de playlists')
    st.write('Obtenir des playlists personnalisées et recommandations')
    st.write('A propos')
    return None
    
if __name__=='__main__':
    main()