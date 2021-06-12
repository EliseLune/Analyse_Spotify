def get_artists_to_list(i):
    res = playlist_cible.iloc[i]['artists']
    res_list  = list(res[1:-1].split(","))
    final=[]
    for artist in res_list:
        if artist[0]=="'":
            final.append(artist[1:-1])
        if artist[0]==" ":
            final.append(artist[2:-1])
    return final

i=0
new_dataframe = playlist_cible[playlist_cible["artists"].str.contains(get_artists_to_list(i)[0])]