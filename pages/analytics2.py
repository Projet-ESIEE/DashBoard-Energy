import dash
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    name="Analitics2",
    analitic=True,
)

path_energy = os.path.join("dataset", "energy-cleaned-dataset.csv")
df_energy = pd.read_csv(path_energy)
THEME = "plotly"

area_options = {
    'Continent': df_energy['Continent'].unique(),
    'Region': df_energy['Region'].unique(),
    'Entity': df_energy['Country'].unique()
}


layout = html.Div(
    className="content",
    children=[
        html.H1('This is our Analytics2 page'),
    ]
)
