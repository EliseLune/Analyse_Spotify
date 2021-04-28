###PAGE D'ACCUEIL DE LA WEBAPP###

import streamlit as st

st.set_page_config(page_title='Page d\'accueil webapp')

def main():
    ac_body()
    return None

def ac_body():
    st.title('SpotData')
    st.write('Par P.Vehrlé, J.Delaplace, C.Nothhelfer, E.Lei')
    st.write('Cette application web a pour but de montrer différentes analyses sur vos playlists spotify.')
    st.button('SE CONNECTER')
    return None

if __name__=='__main__':
    main()