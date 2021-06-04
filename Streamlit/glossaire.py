###Glossaire###

import streamlit as st
import pandas as pd

st.set_page_config(page_title='Glossaire')

def main():
    ac_body()
    return None

def ac_body():
    st.title('SpotData')
    st.write('Vous trouverez sur cette page une définition des différents audiofeatures, donnée par la documentation de Spotify. Tous ces indices sont mesurés entre 0 et 1.')
    Intervalle = [[0,1], [0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]]
    descrip=["L'acoustiness mesure l'acoustic du morceau. Plus il est proche de 1, plus il y a de chance que le morceau soit acoustique (avec des instruments non synthétiques.",
    "La dansabilité mesure si un morceau est adapté à la danse à partir d'élements musicaux comme le tempo, la stabilité du rythme, la force de la rythmique. A 0, un morceau est très peu adapté à la danse alors qu'à 1 est un morceau trus dansable.",
    "L'énergie mesure la perception de l'intensité et de l'activité. Typiquement, les morceaux énergiques semblent rapides, forts et bruyant. Par exemple, le death metal est à haute énergie alors qu'un prélude de Bach est bas dans cette échelle. Les caractérisitques qui servent a créer cette donnée sont la sonorité perçue, le timbre, la vitesse d'apparition et l'entropie générale.",
    "Cet indice mesure si un morceau contient des voix. Plus l'indice est proche de 1, plus il est certain qu'il n'y a aucune voix. Une valeur au dessus de 0.5 tend à être un morceau instrumentaux mais la probabilité augmente quand on s'approche de 1.",
    "La liveness permet de détecter la présence d'une audience dans l'enregistrement. Plus l'indice est proche de 1, plus il est probable que le morceau est live. Au dessus de 0.8, il est quasiment certain que l'enregistrement a été fait en live.",
    "Le bruit est mesuré en décibel. Cette mesure est moyenné sur l'ensemble du morceau et ramené entre 0 et 1.",
    "Cet indice détecte la présence de parties parlées. Les enregistrements parlés (type poèmes, talk show, podcast) seront proche de 1. Au dessus de 0.66, l'enregistrement est probablement entièrement consitué de paroles. Entre 0.33 et 0.66, il y aura des paroles et de la musique, soit en alternance ou dans les cas comme le rap. En dessous de 0.33, il est probable que l'enregistrement soit de la musique, sans parties parlées.",
    "Plus la valence est haute, plus le morceau est joyeux. A l'inverse, plus la valence est faible, plus le morceau est triste."]
    inde = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechness', 'valence']
    df=pd.DataFrame({'Description' : descrip}, index = inde)
    st.dataframe(df, height= 12000)
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
    st.write("Le bruit est mesuré en décibel. Cette mesure est moyenné sur l'ensemble du morceau et ramené entre 0 et 1.")
    st.markdown("___Speechness___")
    st.write("Cet indice détecte la présence de parties parlées. Les enregistrements parlés (type poèmes, talk show, podcast) seront proche de 1. Au dessus de 0.66, l'enregistrement est probablement entièrement consitué de paroles. Entre 0.33 et 0.66, il y aura des paroles et de la musique, soit en alternance ou dans les cas comme le rap. En dessous de 0.33, il est probable que l'enregistrement soit de la musique, sans parties parlées.")
    st.markdown("___Valence___")
    st.write("Plus la valence est haute, plus le morceau est joyeux. A l'inverse, plus la valence est faible, plus le morceau est triste.")
    return None

if __name__=='__main__':
    main()