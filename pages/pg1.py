import pandas as pd
import json
import dash
from dash import dcc,html, callback, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np
import pathlib

dash.register_page(__name__, name = "Data")

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

# page 1

layout = html.Div([
    dbc.Row([
        html.H5("Consultez notre base de données des magasins Carrefour",style={'color':"#00005c",'textAlign':"center","padding":"1rem 0rem"})
    ]),
    dbc.Row([
        html.H6("Choisissez le produit et le magasin",style={'color':"#00005c"})
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id = "categorie_prod1",
                options = BASE_PRODUITS["Recherche"].unique(),
                placeholder = "Catégorie",
                value=BASE_PRODUITS.loc[1,"Recherche"]
            )
        ],width=2),
        dbc.Col([
            dcc.Dropdown(
                id = "nom_prod1",
                placeholder = "Nom de l'article",
                value=BASE_PRODUITS.loc[1,"Nom_produit"]
            )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id = "ville1",
                options = sorted(BASE_PRODUITS["Ville"].unique()),
                placeholder="Ville du magasin",
                value=BASE_PRODUITS.loc[1,"Ville"],
                searchable=True
            )
        ],width=3),
        dbc.Col([
            dcc.Dropdown(
                id = "adresse1",
                placeholder="Adresse du magasin",
                value=BASE_PRODUITS.loc[1,"Adresse"]
            )
        ])
    ], style={"padding":"1rem 0rem"}),
    dbc.Row([
        html.H6("Choisissez les informations souhaitées",style={'color':"#00005c"})
    ]),
    dbc.Row([
        dbc.Checklist(
            id='selection_colonnes',
            options = [{"label":s, "value":s} for s in ["Prix_unitaire","Prix_kg","Meta","Typologie","CP","Lien","Latitude","Longitude"]],
            value = ["Prix_unitaire"],
            inline=True
        )
    ]),
    dbc.Row([
        dash_table.DataTable(id="afficher_base")
    ], style={"padding":"1rem 0rem"})
])

@callback(
    Output("nom_prod1","options"),
    Output("adresse1","options"),
    Input("categorie_prod1","value"),
    Input("ville1","value")
)

def ajour_dropdowns(categorie_prod,ville):
    df1 = BASE_PRODUITS[BASE_PRODUITS["Recherche"] == categorie_prod]
    options_nom = [{'label':opt, 'value':opt} for opt in df1["Nom_produit"].unique()]
    df2 = BASE_PRODUITS[BASE_PRODUITS["Ville"] == ville]
    options_adresse = [{'label':opt, 'value':opt} for opt in df2["Adresse"].unique()]
    return(options_nom, options_adresse)

@callback(
    Output("afficher_base","data"),
    Input("categorie_prod1","value"),
    Input("nom_prod1","value"),
    Input("ville1","value"),
    Input("adresse1","value"),
    Input("selection_colonnes","value")
)

def ajour_base(categorie_prod,nom_prod,ville,adresse,selection_colonnes):
    df1 = BASE_PRODUITS[["Adresse","Ville","Recherche","Nom_produit"]+[selection for selection in selection_colonnes]]
    df1 = df1[df1["Recherche"]==categorie_prod]
    df1 = df1[df1["Ville"]==ville]
    df1 = df1[df1["Adresse"]==adresse]
    df1 = df1[df1["Nom_produit"]==nom_prod]
    return df1.to_dict(orient='records')
