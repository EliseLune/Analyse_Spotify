import streamlit as st

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        app = st.sidebar.radio(
        '',
        self.apps,
        format_func=lambda app: app['title'])

        app['function']()
        
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