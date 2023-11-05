import dash, numpy as np
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    name="Map & Histogram",
    analytics=True,
)
THEME = "plotly_white"
path_energy = os.path.join("dataset", "energy-cleaned-dataset.csv")
df_energy = pd.read_csv(path_energy)
df_energy.insert(4, "Total electricity", np.sum([df_energy["Electricity from Fossil Fuels (TWh)"],
                                                 df_energy["Electricity from Nuclear (TWh)"],
                                                 df_energy["Electricity from Renewables (TWh)"]], axis=0))

df_histo = pd.DataFrame(df_energy, columns=["Country", "Continent", "Year",
                                            "Electricity from Fossil Fuels (TWh)",
                                            "Electricity from Nuclear (TWh)",
                                            "Electricity from Renewables (TWh)"])

df_histo = pd.melt(df_histo, id_vars=["Country", "Continent", "Year"],
                   value_vars=["Electricity from Fossil Fuels (TWh)",
                               "Electricity from Nuclear (TWh)",
                               "Electricity from Renewables (TWh)"],
                   var_name="Electricity mode", value_name="Electricity (TWh)")

# Renommer les catégories "Electricity from fossil fuels (TWh)", "Electricity from nuclear (TWh)", "Electricity from
# renewable (TWh)" en "Fossil Fuels", "Nuclear", "Renewable" (ou les catégories de votre choix)
df_histo["Electricity mode"] = df_histo["Electricity mode"].str.replace("Electricity from ", "")
df_histo["Electricity mode"] = df_histo["Electricity mode"].str.replace(" (TWh)", "")

def make_map(color="Total electricity", scope="world", year="2020"):
    fig = px.choropleth(
        df_energy,
        locations="Country",
        color=color,
        hover_name="Country",
        hover_data=[color],
        locationmode="country names",
        range_color=[min(df_energy[color]), max(df_energy[color])],
        scope=scope,
        color_continuous_scale=px.colors.sequential.thermal_r,
    )
    fig.update_geos(
        visible=False,
        showcoastlines=True,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode='closest',
        autosize=False,
        margin=dict(l=50, r=20, t=20, b=130),
        width=900,
        # height=500,
        coloraxis_colorbar=dict(title=color, len=1, orientation="v"),
        # plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor="rgba(239.0625, 239.0625, 239.0625, 1)")
    )
    return fig


def init_pie():
    df_pie = df_histo.query("Country=='France'")
    fig = px.pie(
        df_pie,
        names="Electricity mode",
        values="Electricity (TWh)",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig


layout = html.Div([
    html.Div([
        html.H1("Energy Dashboard",
                className="header_title",
                )
    ],
        className="header",
    ),

    html.Div([
        html.Div([
            dcc.Graph(id='pie3', figure=init_pie())
        ], className="div_filter_bg")
    ], className="div_filter"),

    html.Div([
        html.Div([
            dcc.Graph(
                id='map',
                figure=make_map(),
                hoverData={'points': [{'location': 'Japan'}]},
                config={'responsive': True}
            )],
            className="div_map_bg")
    ],
        className="div_map",
    ),

    html.Div([
        html.Div([
            dcc.Graph(id='pie', figure=init_pie())
        ], className="div_pie1_bg")
    ], className="div_pie1"),
    # html.Div([
    #     html.Div([
    #         dcc.Graph(id='pie2', figure=init_pie())
    #     ], className="div_pie2_bg")
    # ], className="div_pie2"),

    html.Div([
        html.Div([
            dcc.Graph(id='pie4', figure=init_pie())
        ], className="div_hist_bg")
    ], className="div_hist"),
], className="html",
)


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
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig
