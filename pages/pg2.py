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

dash.register_page(__name__, name = "Panier de biens")

dico_panier = {
    'Nutella':[" Pâte à tartiner aux noisettes et au cacao NUTELLA "," le pot de 825g "],
    'Riz':[" Riz basmati 12mn Bio CARREFOUR BIO ", " le paquet de 500g "],
    'Pates':[" Pâtes Coquillettes Carrefour Classic' ", " le paquet d'1Kg "],
    "Beurre":[" Beurre Doux Gastronomique PRESIDENT ", " la plaquette de 250 g "],
    "Caprice des dieux":[" Fromage CAPRICE DES DIEUX ", " le fromage de 200 g "],
    "Papier toilette":[" Papier toilette humide pure LOTUS ", " le paquet de 42 feuilles "],
    "Pain de mie":[ " Pain de mie american sandwich nature grandes tranches  HARRYS ", " le paquet de 14 tranches - 550 g " ]
    }

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

Base_pan = pd.read_csv(DATA_PATH.joinpath("base_panier.csv"),sep = ";")
Base_pan = Base_pan.dropna()


# page 2

alerte4 = dbc.Alert([
    html.H3("Choisissez votre panier de biens représentatif", style={"textAlign":"center"}),
    html.Hr(),
    dbc.Checklist(
        id = "choix_panier",
        options = [{"label":dico_panier[s][0], "value":s} for s in dico_panier.keys()],
        value = [s for s in dico_panier.keys()],
        #inline=True
    ),
],color = "#dbeaff")

alerte5 = dbc.Alert([
    html.H4("Panier moyen", style={"color":"#ffffff"}),
    html.H6(id = "panier_moyen", style={"color":"#ffffff"})
], color = "#7f8fa6")

alerte6 = dbc.Alert([
    html.H4("Panier médian", style={"color":"#ffffff"}),
    html.H6(id = "panier_median", style={"color":"#ffffff"})
], color = "#7f8fa6")

alerte7 = dbc.Alert([
    html.H4("Panier minimum / maximum", style={"color":"#ffffff"}),
    html.H6(id = "panier_min_max", style={"color":"#ffffff"})
], color = "#7f8fa6")

alerte8 = dbc.Alert([
    html.H4("Variance", style={"color":"#ffffff"}),
    html.H6(id = "panier_var", style={"color":"#ffffff"})
], color = "#7f8fa6")

alerte_class1 = dbc.Alert([
    html.H5("#1"),
    html.H6(id = "moins_cher1")
],color="#98fb98")

alerte_class2 = dbc.Alert([
    html.H5("#2"),
    html.H6(id = "moins_cher2")
],color="#98fb98")

alerte_class3 = dbc.Alert([
    html.H5("#3"),
    html.H6(id = "moins_cher3")
],color="#98fb98")

alerte_class4 = dbc.Alert([
    html.H5("#1"),
    html.H6(id = "plus_cher1")
],color="#f08080")

alerte_class5 = dbc.Alert([
    html.H5("#2"),
    html.H6(id = "plus_cher2")
],color="#f08080")

alerte_class6 = dbc.Alert([
    html.H5("#3"),
    html.H6(id = "plus_cher3")
],color="#f08080")

layout = html.Div([
    dbc.Row([
        html.H6(
            "Sur cette page, nous proposons de construire un panier de biens représentatif d'un consommateur afin d'étudier les caractéristiques de sa composition et de sa répartition.",
            style = {'color':"#00005c"}
        )
    ],style={"padding":"1rem 0rem"}),
    dbc.Row([
        alerte4
    ], style={"textAlign":"center","margin-left":"1rem","margin-right":"1rem","margin-top":"1rem"}),
    dbc.Row([
        dbc.Col([
            alerte5,
            alerte7
        ], style = {"margin-left":"1rem","margin-right":"0rem"}),
        dbc.Col([
            alerte6,
            alerte8
        ], style = {"margin-left":"0rem","margin-right":"1rem"})
    ]),
    dcc.Graph(
        id = "carte_panier",
        style={"width":"58rem","margin-left":"1rem"}),
    dbc.Row([
        dbc.Col([
            html.H5("Les trois paniers les plus chers", style={"color":"#00005c","padding":"1rem 0rem"}),
            alerte_class1,
            alerte_class2,
            alerte_class3
        ], style = {"margin-left":"1rem","margin-right":"0rem"}),
        dbc.Col([
            html.H5("Les trois paniers les moins chers", style={"color":"#00005c","padding":"1rem 0rem"}),
            alerte_class4,
            alerte_class5,
            alerte_class6
        ], style = {"margin-left":"0rem","margin-right":"1rem"})
    ]),
    dbc.Row([
        html.H5("Répartition du prix du panier de biens moyen",style={'color':"#00005c",'textAlign':"center"})
    ]),
    dbc.Row([
        dcc.Graph(
            id = "compo_panier"
        )
    ]),
    dbc.Row([
        html.H5("Répartition des prix du panier de biens",style={'color':"#00005c",'textAlign':"center"})
    ]),
    dbc.Row([
        dcc.Graph(
            id = "repartition_paniers"
        )
    ]),
    dbc.Row([
        html.H5("Histogramme des prix des paniers de biens",style={'color':"#00005c",'textAlign':"center"})
    ]),
    dbc.Row([
        dcc.Graph(
            id = "histo_panier"
        )
    ])
])



@callback(
    Output("panier_moyen","children"),
    Output("panier_median","children"),
    Output("panier_min_max","children"),
    Output("panier_var","children"),
    Input("choix_panier","value")
)

def val_panier(choix_panier):
    df1 = Base_pan.copy()
    df1 = df1[[produit for produit in choix_panier]]
    df1 = df1.dropna()
    df1["Total_panier"] = df1.sum(axis=1)
    return str(round(df1["Total_panier"].mean(),2))+"€", str(round(df1["Total_panier"].median(),2))+"€", str(round(df1["Total_panier"].min(),2))+"€"+ " / " + str(round(df1["Total_panier"].max(),2))+"€", str(round(df1["Total_panier"].var(),2))+"€"

@callback(
    Output("carte_panier","figure"),
    Input("choix_panier","value")
)

def carte_panier(choix_panier):
    df1 = Base_pan.copy()
    df1 = df1[["Adresse","CP","Latitude","Longitude"]+[produit for produit in choix_panier]]
    df1["CP"] = df1["CP"].astype(str)
    df1["Total_panier"] = df1[[produit for produit in choix_panier]].sum(axis=1)
    carte = px.scatter_mapbox(
        df1, 
        lat="Latitude", 
        lon="Longitude",
        zoom=4,
        color="Total_panier",
        hover_name="Adresse",
        hover_data=["CP"],
        labels={"Total_panier":"Prix du panier (€)","CP":"Code postal"})
    carte.update_layout(mapbox_style="open-street-map")
    carte.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return carte

@callback(
    Output("moins_cher1","children"),
    Output("moins_cher2","children"),
    Output("moins_cher3","children"),
    Input("choix_panier","value")
)

def moins_cher(choix_panier):
    df1 = Base_pan.copy()
    df1 = df1[["Ville","Adresse","CP"]+[produit for produit in choix_panier]]
    df1["CP"] = df1["CP"].astype(str)
    df1["Total_panier"] = df1.sum(axis=1)
    df1 = df1.sort_values(by="Total_panier",ascending = True)
    df1.index = [k for k in range(len(df1.index))]
    return df1.loc[0,"Adresse"] +" "+ df1.loc[0,"CP"]+ " " +df1.loc[0,"Ville"], df1.loc[1,"Adresse"]+" "+df1.loc[1,"CP"]+" "+df1.loc[1,"Ville"], df1.loc[2,"Adresse"]+" "+df1.loc[2,"CP"]+" "+df1.loc[2,"Ville"]


@callback(
    Output("plus_cher1","children"),
    Output("plus_cher2","children"),
    Output("plus_cher3","children"),
    Input("choix_panier","value")
)

def plus_cher(choix_panier):
    df1 = Base_pan.copy()
    df1 = df1[["Ville","Adresse","CP"]+[produit for produit in choix_panier]]
    df1["CP"] = df1["CP"].astype(str)
    df1["Total_panier"] = df1.sum(axis=1)
    df1 = df1.sort_values(by="Total_panier",ascending = False)
    df1.index = [k for k in range(len(df1.index))]
    return df1.loc[0,"Adresse"] +" "+ df1.loc[0,"CP"]+ " " +df1.loc[0,"Ville"], df1.loc[1,"Adresse"]+" "+df1.loc[1,"CP"]+" "+df1.loc[1,"Ville"], df1.loc[2,"Adresse"]+" "+df1.loc[2,"CP"]+" "+df1.loc[2,"Ville"]

@callback(
    Output("compo_panier","figure"),
    Input("choix_panier","value")
)

def ajour_compo_panier(choix_panier):
    df1 = Base_pan.copy()
    df1.index = df1["Adresse"]
    df1 = df1[[produit for produit in choix_panier]]
    df1 = df1.transpose()
    Prix = df1.mean(axis = 1)
    Article = df1.index
    figu = px.pie(
        values=Prix, 
        names=Article,
        hole=0.3,
        labels={'label':"Produit","value":"Prix"})
    return figu

@callback(
    Output("repartition_paniers","figure"),
    Input("choix_panier","value")
)

def ajour_repartion_paniers(choix_panier):
    df1 = Base_pan.copy()
    df1 = df1[[produit for produit in choix_panier]]
    df1 = df1.dropna()
    df1["Total_panier"] = df1.sum(axis=1)
    figu = px.box(
        df1,
        x = "Total_panier",
        labels={"Total_panier":"Prix du panier (en €)"}
    )
    return figu

@callback(
    Output("histo_panier","figure"),
    Input("choix_panier","value")
)

def ajour_histo_panier(choix_panier):
    df1 = Base_pan.copy()
    df1 = df1[[produit for produit in choix_panier]]
    df1 = df1.dropna()
    df1["Total_panier"] = df1.sum(axis=1)
    figu = px.histogram(
        df1,
        x = "Total_panier",
        labels={"Total_panier":"Prix du panier"}
    )
    return figu