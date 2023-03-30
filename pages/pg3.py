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

dash.register_page(__name__, name = "Statistiques par produit")

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("donnees").resolve()
with open(DATA_PATH.joinpath("base_finale_lat_long.txt"),'r') as file:
    dico_produits = json.load(file)

BASE_PRODUITS = pd.DataFrame.from_dict(dico_produits)
BASE_PRODUITS = BASE_PRODUITS[BASE_PRODUITS["Prix_kg"] != "N.A."]

liste_index = BASE_PRODUITS[BASE_PRODUITS["CP"] == "Rue"].index
BASE_PRODUITS = BASE_PRODUITS.drop(liste_index)

BASE_PRODUITS["Prix_kg"] = BASE_PRODUITS["Prix_kg"].astype(np.float64)

BASE_PRODUITS["Typologie"] = BASE_PRODUITS["Typologie"].astype(str)


layout = html.Div([
    dbc.Row([
        html.H3("Statistiques par article", style={'color':"#00005c","margin-top":"1rem","margin-bottom":"1rem"}),
        html.H6("Sur cette page, nous présentons des statistiques de prix pour chaque article.", style={"color":"#00005c","margin-bottom":"1rem"})
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id = "categorie_prod", 
                options = BASE_PRODUITS["Recherche"].unique(),
                placeholder = "Catégorie",
                value=BASE_PRODUITS.loc[1,"Recherche"])
        ],width=2),
        dbc.Col([
            dcc.Dropdown(id = "nom_prod", 
            placeholder = "Nom de l'article",
            value=BASE_PRODUITS.loc[1,"Nom_produit"])
        ]),
        dbc.Col([
            dcc.Dropdown(
                id = "meta_prod", 
                placeholder = "Informations complémentaires",
                value=BASE_PRODUITS.loc[1,"Meta"]),
        ],width=3)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id = "graphe_1produit",
                style={"width":"58rem","margin-left":"1rem","height":"35rem"})
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H5("Répartition des prix du produit",style={"color":"#00005c","textAlign":"center"}),
            dcc.Graph(
                id = "boite_moustache1"
            )
        ]),
        dbc.Col([
            html.H5("Répartition des prix du produit par type de magasin",style={"color":"#00005c","textAlign":"center"}),
            dcc.Graph(
                id = "boite_moustache2"
            )
        ])
    ]),
    dbc.Row([
        html.H5("Histogramme des prix du produit",style={"color":"#00005c","textAlign":"center"}),
        dcc.Graph(
            id = "histo1"
        )
    ])
])


@callback(
    Output("nom_prod", "options"),
    [Input("categorie_prod", "value")]
)

def serveur1(categorie_prod):
    ## Dynamic dropdowns
    df1 = BASE_PRODUITS[BASE_PRODUITS["Recherche"] == categorie_prod]
    options_nom = [{'label':opt, 'value':opt} for opt in df1["Nom_produit"].unique()]
    return(options_nom)

@callback(
    Output("meta_prod", "options"),
    [Input("categorie_prod","value"),
    Input("nom_prod","value")]
)

def serveur2(categorie_prod, nom_prod):
    df1 = BASE_PRODUITS[BASE_PRODUITS["Recherche"] == categorie_prod]
    df2 = df1[df1["Nom_produit"] == nom_prod]
    options_meta = [{'label':opt, 'value':opt} for opt in df2["Meta"].unique()]
    return(options_meta)

@callback(
    Output("graphe_1produit","figure"),
    [Input("categorie_prod", "value"),
    Input("nom_prod","value"),
    Input("meta_prod","value")]
)

def ajour_carte(categorie_prod,nom_prod,meta_prod):
    df_sub = BASE_PRODUITS[BASE_PRODUITS['Recherche']==categorie_prod]
    df_sub = BASE_PRODUITS[BASE_PRODUITS['Nom_produit']==nom_prod]
    df_sub = BASE_PRODUITS[BASE_PRODUITS['Meta']==meta_prod]
    figu = px.scatter_mapbox(
        df_sub, lat="Latitude", 
        lon="Longitude", 
        color="Prix_kg",
        color_continuous_scale="Bluered", 
        mapbox_style = "open-street-map",
        zoom=5,
        hover_name="Adresse",
        hover_data=["Ville","CP"],
        labels={'Prix_kg':'Prix au kilo (en €)','CP':'Code postal'})
    return(figu)

@callback(
    Output("boite_moustache1","figure"),
    Output('boite_moustache2',"figure"),
    [Input("categorie_prod", "value"),
    Input("nom_prod","value"),
    Input("meta_prod","value")]
)

def ajour_boite1(categorie_prod,nom_prod,meta_prod):
    df1 = BASE_PRODUITS[BASE_PRODUITS['Recherche'] == categorie_prod]
    df1 = BASE_PRODUITS[BASE_PRODUITS['Nom_produit'] == nom_prod]
    df1 = BASE_PRODUITS[BASE_PRODUITS['Meta'] == meta_prod]
    figu1 = px.box(df1, y = "Prix_kg", labels={'Prix_kg':'Prix au kilo (en €)'})
    figu2 = px.box(
        df1,
        x = "Typologie", 
        y = "Prix_kg", 
        labels={'Typologie':'Type de magasin','Prix_kg':'Prix au kilo (en €)'},
        color="Typologie")
    figu2.layout.update(showlegend = False)
    return figu1, figu2

@callback(
    Output("histo1","figure"),
    [Input("categorie_prod", "value"),
    Input("nom_prod","value"),
    Input("meta_prod","value")]
)

def ajour_histo1(categorie_prod,nom_prod,meta_prod):
    df1 = BASE_PRODUITS[BASE_PRODUITS['Recherche'] == categorie_prod]
    df1 = BASE_PRODUITS[BASE_PRODUITS['Nom_produit'] == nom_prod]
    df1 = BASE_PRODUITS[BASE_PRODUITS['Meta'] == meta_prod]
    figu = px.histogram(
        df1,
        x = "Prix_kg",
        labels={'Prix_kg':'Prix au kilo (en €)'},
    )
    return figu