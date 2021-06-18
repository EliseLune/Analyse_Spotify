import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st

def create_work():
    """Create a dataframe containing all audio-features, plus popularity"""
    feat = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'valence', 'popularity']
    name = ['Acoustique', 'Dansabilité', 'Energie', 'Insturmentalité', 'Tonalité', 'Live', 'Puissance acoustique', 'Mode', 'Parler', 'Tempo', 'Jovialité', 'Popularité']
    desc = ["Décrit dans quelle proportion la piste est produite par des instruments acoustiques. 0 = électro | 1 = Vivaldi", "Décrit à quel point il est possible de danser sur la piste. 0 = émission radio | 1 = musique de boîte", "Décrit dans quelle mesure la piste est intense, active. 0 = prélude de Bach | 1 = death metal", "Décrit dans quelle proportion on entend des voix (paroles de chant, parlées) dans la piste. 0 = rap pur | 1 = pièce pour piano", "Donne la tonalité principale de la piste. 0 = Do, 1 = Do#, 2 = Ré, etc.", "Décrit si un public est présent. 0 = piste enregistré en studio | 1 = public qui chante avec l'artiste en concert", "Décrit à quel point la piste rend un son fort. -60 dB = ASMR | 0 dB = hard metal", "Donne le mode (majeur/mineur) de la piste. 0 = mineur ; 1 = majeur", "Décrit dans quelle mesure la piste contient des paroles parlées. 0 = musique pure | 1 = podcast", "Donne le tempo de la piste en battements par minute (BPM).", "Décrit la positivité communiquée par la piste. 0 = Sound of Silence | 1 = Happy", "Décrit l'étendue du public que la piste, et comment elle y est appréciée"]
    inte = [[0, 0.25, 0.5, 0.75, 1], [0, 0.33, 0.66, 1], [0, 0.33, 0.66, 1], [0, 0.5, 0.75, 1], None, [0, 0.5, 0.8, 1], None, None, [0, 0.33, 0.66, 1], None, [0, 0.25, 0.5, 0.75, 1], [0, 33, 66, 100]]
    tags = [['Synthétique', 'Plutôt synthétique', 'Plutôt acoustique', 'Acoustique'], ['Calme', 'De quoi battre le rythme', 'Très dansant'], ['Doux', 'Moyen', 'Energique'], ['Majorité de paroles', 'Majorité instrumentale', 'Instrumental pur'], None, ['Enregistrement studio', "Présence d'un petit public", 'Live'], None, None, ['Musical', 'Mélange discours et musique', 'Discours pur'], None, ['Très sombre', 'Plutôt sombre', 'Plutôt léger', 'Joyeux'], ['Peu connu', 'Relativement connu', 'Populaire']]
    anly = [True, True, True, True, False, True, False, False, True, False, True, True]
    dict  = {'audio-features':feat, 'name':name, 'description':desc, 'intervals':inte, 'tags':tags, 'to analyse':anly}
    audio_feat = pd.DataFrame(dict).set_index('audio-features')
    return audio_feat

def tag(audio_feat, carac, moy):
    """Returns the corresponding tag to the audio-features 'carac' based on their average
    audio_feat : pd.Dataframe
    carac : string
    moy : float"""
    if not audio_feat.loc[carac, "to analyse"] : return None
    for i, seuil in enumerate(audio_feat.loc[carac, "intervals"]):
        if moy < seuil :
            return audio_feat.loc[carac, "tags"][i-1]

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

#Test de laffichage dun graphique avec un playlist:
def gen_hists(dataPL,liste_feat, tabAF):
    tabTags = gen_tags(tabAF, dataPL)
    for aud_feat in liste_feat:
        #On peut faire une boucle for pour afficher les graphs de tous les audiofeatures sélectionnés
        #Et faire des if pour afficher un type de graph différent selon l'audiofeature?
        if aud_feat=='release_year':
            fig = px.histogram(dataPL, x='release_date')
            fig.update_layout(
                title="Année de sortie",
            )
            st.plotly_chart(fig)
        else:
            # if aud_feat=='popularity':
            #     binsize, eten = 10, [0,100]
            # else :
            #     binsize, eten = 0.75, [0,1.]
            # fig = ff.create_distplot([dataPL[aud_feat]], [aud_feat], bin_size=binsize, show_rug=False)
            # fig.update_xaxes(range=eten)
            fig = px.histogram(dataPL, x=[aud_feat],
                barmode='overlay',
                opacity=0.5)
            fig.update_layout(
                title = tabTags.loc[aud_feat, 'name'] + " : " + tabTags.loc[aud_feat, 'tag']
            )
            st.plotly_chart(fig)
    return tabTags