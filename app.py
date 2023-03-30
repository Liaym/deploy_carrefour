import pandas as pd
import json
import dash
from dash import dcc,html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, use_pages = True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

navbar = dbc.NavbarSimple(
    children= [dbc.NavItem(dbc.NavLink(page["name"],href=page["path"])) for page in dash.page_registry.values()],
    brand= "Indice des prix à la consommation",
    brand_href="/",
    color= "#00005c",
    dark=True
)


app.layout = dbc.Container([
    navbar,
    dash.page_container
], fluid= True)


if __name__ == "__main__":
    app.run_server(port = 4050)