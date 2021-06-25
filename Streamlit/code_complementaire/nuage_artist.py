import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def artist_dataframe(all_tracks,sp):
    df = pd.DataFrame(columns=['artist_id','name','number of tracks','image'])
    for track in all_tracks:
        artists = sp.track(track)["artists"]
        for artist in artists:
            liste_index = df[df['artist_id'].str.contains(artist["id"])].index.tolist()
            n = len(liste_index)
            if n!=0:
                i = liste_index[0]
                df['number of tracks'][i] = df['number of tracks'][i] +1
            else :
                tutu = sp.artist(artist["id"])
                images = tutu["images"]
                if len(images) !=0:
                    df = df.append({'artist_id': artist["id"], 'name' : tutu["name"], 'number of tracks' : 1,'image' : images[0]["url"]}, ignore_index=True)
                else : 
                    df = df.append({'artist_id': artist["id"],'name' : tutu["name"], 'number of tracks' : 1,'image' : None}, ignore_index=True)
                
    return df


class C():
    def __init__(self,r,df):
        self.N = len(r)
        self.df = df
        self.x = np.ones((self.N,3))
        self.x[:,2] = r
        maxstep = 2*self.x[:,2].max()
        length = np.ceil(np.sqrt(self.N))
        grid = np.arange(0,length*maxstep,maxstep)
        gx,gy = np.meshgrid(grid,grid)
        self.x[:,0] = gx.flatten()[:self.N]
        self.x[:,1] = gy.flatten()[:self.N]
        self.x[:,:2] = self.x[:,:2] - np.mean(self.x[:,:2], axis=0)

        self.step = self.x[:,2].min()
        self.p = lambda x,y: np.sum((x**2+y**2)**2)
        self.E = self.energy()
        self.iter = 1.

    def minimize(self):
        while self.iter < 1000*self.N:
            for i in range(self.N):
                rand = np.random.randn(2)*self.step/self.iter
                self.x[i,:2] += rand
                e = self.energy()
                if (e < self.E and self.isvalid(i)):
                    self.E = e
                    self.iter = 1.
                else:
                    self.x[i,:2] -= rand
                    self.iter += 1.

    def energy(self):
        return self.p(self.x[:,0], self.x[:,1])

    def distance(self,x1,x2):
        return np.sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)-x1[2]-x2[2]

    def isvalid(self, i):
        for j in range(self.N):
            if i!=j: 
                if self.distance(self.x[i,:], self.x[j,:]) < 0:
                    return False
        return True

    def plot(self, ax):
        for i in range(self.N):
            # st.image(self.df['image'][i])
            # image = plt.imread(self.df['image'][i])
            circ = plt.Circle(self.x[i,:2],self.x[i,2] )
            ax.add_patch(circ)

def creat_chart(all_tracks,sp):
    # create 10 circles with different radii
    df = artist_dataframe(all_tracks,sp)
    # r = np.random.randint(5,15, size=10)
    r = df['number of tracks'].tolist()
    c = C(r,df)
    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    ax.axis("off")

    c.minimize()

    c.plot(ax)
    ax.relim()
    ax.autoscale_view()
    st.write(fig)
    plt.show()
    return df