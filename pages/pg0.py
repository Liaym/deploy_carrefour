import pandas as pd
import json
import dash
from dash import dcc,html, callback
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np
import pathlib

dash.register_page(__name__, path = '/', name="Accueil")

## Données 
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("donnees").resolve()

with open(DATA_PATH.joinpath("base_finale_lat_long.txt"),'r') as file:
    dico_produits = json.load(file)

Base_produits = pd.DataFrame.from_dict(dico_produits)


fig = px.scatter_mapbox(
    Base_produits, 
    lat="Latitude", 
    lon="Longitude",
    zoom=4,
    hover_name="Adresse",
    hover_data=["CP","Ville"],
    color="Typologie",
    labels={'Typologie':'Magasins','CP':'Code postal'})

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig.show()

nb_villes = len(pd.unique(Base_produits["Ville"]))
nb_produits = len(pd.unique(Base_produits["Nom_produit"]))
nb_magasins = len(pd.unique(Base_produits["Adresse"]))


# page 0

alerte1 = dbc.Alert([
    html.H3(str(nb_magasins), style={"color":"#ffffff"}),
    html.H5("Magasins enregistrés", style={"color":"#ffffff"})
],color="#1560bd")

alerte2 = dbc.Alert([
    html.H3(str(nb_villes), style={"color":"#ffffff"}),
    html.H5("Communes", style={"color":"#ffffff"})
],color="#00cccb")

alerte3 = dbc.Alert([
    html.H3(str(nb_produits), style={"color":"#ffffff"}),
    html.H5("Produits analysés", style={"color":"#ffffff"})
],color="#17657d")


layout = html.Div([
    dbc.Row([
        html.H6(
            "Cette application a pour objectif de suivre et de partager, à partir de la base de données que nous avons construite, les prix de différents biens alimentaires ou ménagers de base, ainsi que d'en fournir quelques statistiques aux consommateurs. Nous nous sommes concentrés dans un premier temps sur la chaine de magasins Carrefour, mais notre objectif est de l'étendre à plusieurs chaines de magasins.",
            style={"color":"#00005c"}
        )
    ], style = {"padding":"1rem 1rem"}),
    dbc.Row([
        dbc.Col([alerte1],style={"textAlign":"center"}),
        dbc.Col([alerte2],style={"textAlign":"center"}),
        dbc.Col([alerte3],style={"textAlign":"center"})
    ], style = {"padding":"0rem 1rem"}),
    dbc.Row([
        html.H4("Carte des magasins Carrefour en France",style={'color':"#00005c",'textAlign':"center"})
    ]),
    dbc.Row([
        dcc.Graph(
            id = "graphe_carrefours_france",
            figure = fig,
            style={"width":"58rem","margin-left":"1rem"}
        )
    ])
])

@callback(
    Output("graphe2","figure"),
    Input("produit2","children")
)

def afficher_p2(produit2):
    return None