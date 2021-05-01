###PAGE OU ON RENTRE LES IDENTIFIANTS###

import streamlit as st

st.set_page_config(page_title='Authentification',initial_sidebar_state="expanded")

def main():
    ac_body()
    return None

def ac_body():
    st.title('SpotData')
    st.header('Connectez-vous avec vos identifiants Spotify')
    st.text_input('Identifiant / Adresse mail')
    st.text_input('Mot de passe')
    st.button('Se connecter')
    return None
    
if __name__=='__main__':
    main()
    