import dash, numpy as np
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
THEME = "plotly_dark"
path_energy = os.path.join("dataset", "energy-cleaned-dataset.csv")
df_energy = pd.read_csv(path_energy)
df_energy.insert(4, "Total electricity", np.sum([df_energy["Electricity from Fossil Fuels (TWh)"],
                                                 df_energy["Electricity from Nuclear (TWh)"],
                                                 df_energy["Electricity from Renewables (TWh)"]], axis=0))

df_histo = pd.DataFrame(df_energy, columns=["Country", "Continent", "Year",
                                            "Electricity from Fossil Fuels (TWh)",
                                            "Electricity from Nuclear (TWh)",
                                            "Electricity from Renewables (TWh)"])

df_histo = pd.melt(df_histo, id_vars=["Country", "Continent", "Year"], value_vars=["Electricity from Fossil Fuels (TWh)",
                                                                                   "Electricity from Nuclear (TWh)",
                                                                                   "Electricity from Renewables (TWh)"],
                   var_name="Electricity mode", value_name="Electricity (TWh)")

# Renommer les catégories "Electricity from fossil fuels (TWh)", "Electricity from nuclear (TWh)", "Electricity from
# renewable (TWh)" en "Fossil Fuels", "Nuclear", "Renewable" (ou les catégories de votre choix)
df_histo["Electricity mode"] = df_histo["Electricity mode"].str.replace("Electricity from ", "")
df_histo["Electricity mode"] = df_histo["Electricity mode"].str.replace(" (TWh)", "")

def make_map(color="Total electricity", scope="world", year = "2020"):
    df_map = df_energy.query("Year == "+year)
    fig = px.choropleth(
        df_energy,
        locations="Country",
        # color=np.log(df_energy[color]),
        color=color,
        hover_name="Country",
        hover_data=[color],
        locationmode="country names",
        # range_color=[0, np.log(max(df_energy[color]))],
        range_color=[min(df_energy[color]), max(df_energy[color])],
        template=THEME,
        scope=scope,
        color_continuous_scale=px.colors.sequential.thermal_r,
    )
    fig.update_layout(margin=dict(l=40, r=0, b=40, t=10, pad=0), paper_bgcolor="black",
                      hovermode='closest',
                      coloraxis_colorbar=dict(title=color, len=0.8, orientation="h", y=0))
    return fig


layout = html.Div([
    html.Div([
        dcc.Dropdown(
            df_energy.keys(),
            "Total electricity",
            id='columns dropdown',
        ),
    ], style={'width': '40%', 'display': 'inline-block', 'padding': '0 100 200 300'}),
    html.Div([
        dcc.Graph(
            id='map',
            figure=make_map(),
            hoverData={'points': [{'location': 'Japan'}]}
        )
    ], style={'width': '65%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='pie'),
    ], style={'display': 'inline-block', 'width': '25%'}),
])





@callback(
    Output("pie", "figure"),
    [Input("map", "hoverData")]
)
def pie(hoverData):
    pays = hoverData['points'][0]["location"]
    df_pie = df_histo.query("Country=='" + pays + "'")
    fig = px.pie(
        df_pie,
        names="Electricity mode",
        values="Electricity (TWh)",
        template=THEME
    )
    fig.update_layout(
        margin={'l': 20, 'b': 30, 'r': 10, 't': 10}
    )
    return fig
