import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st

@st.cache
def create_work():
    """Create a dataframe containing all audio-features, plus popularity"""
    feat = ['acousticness','danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'valence', 'popularity']
    name = ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Key', 'Liveness', 'Loudness', 'Mode', 'Speechiness', 'Tempo', 'Valence', 'Popularité']
    desc = ["L'acousticness mesure l'acoustique du morceau. Plus il est proche de 1, plus il y a de chance que le morceau soit acoustique (avec des instruments non synthétiques).",
        "La dansabilité mesure si un morceau est adapté à la danse à partir d'élements musicaux comme le tempo, la stabilité du rythme, la force de la rythmique. A 0, un morceau est très peu adapté à la danse alors qu'à 1 est un morceau très dansable.",
        "L'énergie mesure la perception de l'intensité et de l'activité. Typiquement, les morceaux énergiques semblent rapides, forts et bruyants. Par exemple, le death metal est à haute énergie alors qu'un prélude de Bach est bas dans cette échelle.",
        "Cet indice mesure si un morceau contient des voix. Plus l'indice est proche de 1, plus il est certain qu'il n'y a aucune voix. Une valeur au dessus de 0.5 tend à être un morceau instrumental mais la probabilité augmente quand on s'approche de 1.",
        "Tonalité principale de la piste. 0 = Do, 1 = Do#, 2 = Ré, etc.",
        "La liveness permet de détecter la présence d'un public dans l'enregistrement. Plus l'indice est proche de 1, plus il est probable que le morceau est un live. Au dessus de 0.8, il est quasiment certain que l'enregistrement a été fait en live.",
        "Ce paramètre décrit à quel point la piste rend un son fort, sur une échelle allant de -60 dB (= ASMR) à 0 dB (= hard metal)",
        "Mode (majeur/mineur) de la piste. 0 = mineur ; 1 = majeur",
        "Cet indice détecte la présence de parties parlées. Les enregistrements parlés (type poèmes, talk show, podcast) seront proches de 1. Au dessus de 0.66, l'enregistrement est probablement entièrement consitué de paroles. Entre 0.33 et 0.66, il y aura des paroles et de la musique, soit en alternance, soit en même temps comme le rap. En dessous de 0.33, il est probable que l'enregistrement soit de la musique, sans parties parlées.",
        "Tempo de la piste en battements par minute (BPM)",
        "Plus la valence est haute, plus le morceau est joyeux. A l'inverse, plus la valence est faible, plus le morceau est triste.",
        "Cet indice mesure sur une échelle de 0 à 100 la notoriété de la piste."]
    inte = [[0, 0.25, 0.5, 0.75, 1], [0, 0.33, 0.66, 1], [0, 0.33, 0.66, 1], [0, 0.5, 0.75, 1], None, [0, 0.5, 0.8, 1], None, None, [0, 0.33, 0.66, 1], None, [0, 0.25, 0.5, 0.75, 1], [0, 33, 66, 100]]
    tags = [['Synthétique', 'Plutôt synthétique', 'Plutôt acoustique', 'Acoustique'],
        ['Calme', 'De quoi battre le rythme', 'Très dansant'],
        ['Doux', 'Moyen', 'Energique'],
        ['Majorité de paroles', 'Majorité instrumentale', 'Instrumental pur'],
        None,
        ['Enregistrement studio', "Présence d'un petit public", 'Live'],
        None,
        None,
        ['Musical', 'Mélange discours et musique', 'Discours pur'],
        None,
        ['Triste', 'Morose', 'Léger', 'Joyeux'],
        ['Peu connu', 'Relativement connu', 'Populaire']]
    anly = [True, True, True, True, False, True, False, False, True, False, True, False]
    dict  = {'audio-features':feat, 'name':name, 'description':desc, 'intervals':inte, 'tags':tags, 'to analyse':anly}
    audio_feat = pd.DataFrame(dict).set_index('audio-features')
    return audio_feat

def tag(audio_feat, carac, moy):
    """Returns the corresponding tag to the audio-features 'carac' based on their average
    audio_feat : pd.Dataframe
    carac : string
    moy : float"""
    if audio_feat.loc[carac, "intervals"]==None : return None
    for i, seuil in enumerate(audio_feat.loc[carac, "intervals"]):
        if moy < seuil :
            return audio_feat.loc[carac, "tags"][i-1]

@st.cache
def gen_tags(audio_feat, playlist):
    """Generate a dataframe specific to a playlist with tags and other statiscal information"""
    playlist2 = audio_feat.loc[:, 'name':'description'].copy()
    for aud in playlist2.index:
        playlist2.loc[aud, 'average'] = playlist[aud].mean()
        playlist2.loc[aud, 'tag'] = tag(audio_feat, aud, playlist2.loc[aud, 'average'])
        playlist2.loc[aud, 'min'] = playlist[aud].min()
        playlist2.loc[aud, 'max'] = playlist[aud].max()
        playlist2.loc[aud, 'median'] = playlist[aud].median()
        playlist2.loc[aud, 'st dev'] = playlist[aud].std()
    return playlist2

# def gen_wind_rose(dtaPL):
#     fig = px.bar_polar(dataPL, )


def gen_hists(dataPL,liste_feat, tabTags):
    for item in liste_feat:
        #On peut faire une boucle for pour afficher les graphs de tous les audiofeatures sélectionnés
        #Et faire des if pour afficher un type de graph différent selon l'audiofeature?
        if item=='Années de sortie':
            fig = px.histogram(dataPL, x='release_date')
            fig.update_layout(
                title="Années de sortie",
                xaxis_title = "Années de sortie",
                yaxis_title = "Nombre de piste /période de temps",
                bargap = 0.1
            )
            st.plotly_chart(fig)
        else:
            # if aud_feat=='popularity':
            #     binsize, eten = 10, [0,100]
            # else :
            #     binsize, eten = 0.75, [0,1.]
            # fig = ff.create_distplot([dataPL[aud_feat]], [aud_feat], bin_size=binsize, show_rug=False)
            # fig.update_xaxes(range=eten)
            aud_feat = item.lower()
            fig = px.histogram(dataPL, x=[aud_feat],
                barmode='overlay',
                opacity=0.5)
            fig.update_layout(
                title = tabTags.loc[aud_feat, 'name'] + " : " + tabTags.loc[aud_feat, 'tag'],
                xaxis_title = tabTags.loc[aud_feat, 'name'],
                yaxis_title = 'Nombre de pistes',
                bargap = 0.1
            )
            st.plotly_chart(fig)