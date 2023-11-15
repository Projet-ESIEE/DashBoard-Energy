import dash
import numpy as np
import pandas as pd
import os
import plotly.express as px
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    name="Map & Histogram",
    analytics=True,
)
THEME = "plotly_white"
test = "test1"

color_map = {
    "Fossil Fuels": "rgb(2223,95,73)",
    "Nuclear": "rgb(74,147,255)",
    "Renewables": "rgb(0,205,94)"
}

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
df_histo["Electricity mode"] = df_histo["Electricity mode"].str.slice(stop=-6)

layout = html.Div([
    html.Div([
        html.H1(children="Titre",
                className="header_title",
                id="titre"
                )
    ],
        className="header",
    ),

    html.Div([
        html.Div([
            dcc.Slider(
                df_histo['Year'].min(),
                df_histo['Year'].max(),
                step=1,
                id="slider",
                value=df_histo['Year'].max(),
                marks={str(year): str(year) for year in df_histo['Year'].unique() if year % 5 == 0},
                className="div_filter_slider"
            ),
            html.H2(
                children="test",
                id="pourcentage",
                className="div_filter_pourcentage"
            )
        ], className="div_filter_bg")
    ], className="div_filter"),

    html.Div([
        html.Div([
            dcc.Graph(
                id='map',
                hoverData={'points': [{'location': 'Japan'}]},
                config={'responsive': True}
            )],
            className="div_map_bg")
    ],
        className="div_map",
    ),

    html.Div([
        html.Div([
            dcc.Graph(id='pie')
        ], className="div_pie1_bg")
    ], className="div_pie1"),

    html.Div([
        html.Div([
            dcc.Graph(id='histogram')
        ], className="div_hist_bg")
    ], className="div_hist"),
], className="html",
)


@callback(
    Output("titre", "children"),
    [Input("map", "hoverData"),
     Input("slider", "value")]
)
def titre(hoverData, year_value):
    pays = hoverData['points'][0]["location"]
    titre = "Electricity production in " + pays + " in " + str(year_value) + " (TWh)"
    return titre


@callback(
    Output("pourcentage", "children"),
    [Input("slider", "value"),
     Input("map", "hoverData")]
)
def pourcentage(year_value, hoverData):
    pays = hoverData['points'][0]["location"]
    pays_elec = df_histo.query("Country=='" + pays + "' and Year==" + str(year_value))["Electricity (TWh)"].sum()
    tot_elec = df_histo.query("Year == "+str(year_value))["Electricity (TWh)"].sum()
    percentage = (pays_elec / tot_elec) * 100
    formatted_percentage = round(percentage, 2)
    output_text = f"Total : {int(pays_elec)} TWh \n\n {formatted_percentage} % of world production"
    return dcc.Markdown(output_text)


@callback(
    Output("map", "figure"),
    [Input("slider", "value")]
)
# def make_map(color="Total electricity", scope="world", year="2020"):
def make_map(year_value):
    color = "Total electricity"
    scope = "world"
    fig = px.choropleth(
        df_energy[df_energy["Year"] == year_value],
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
        center={"lat": 30, "lon": 0},  # Coordonnées latitudinales et longitudinales du centre
        projection_scale=1.3
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode='closest',
        autosize=False,
        margin=dict(l=50, r=20, t=20, b=130),
        width=900,

        coloraxis_colorbar=dict(title="", len=1, orientation="v"),
        # plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor="rgba(239.0625, 239.0625, 239.0625, 1)")
    )
    return fig


@callback(
    Output("pie", "figure"),
    [Input("map", "hoverData"),
     Input("slider", "value")]
)
def pie(hoverData, year_value):
    pays = hoverData['points'][0]["location"]
    df_pie = df_histo.query("Country=='" + pays + "' and Year==" + str(year_value))
    fig = px.pie(
        df_pie,
        names="Electricity mode",
        values="Electricity (TWh)",
        opacity=0.9,
    )

    fig.update_traces(marker=dict(colors=[color_map[mode] for mode in df_pie["Electricity mode"]]))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig


@callback(
    Output("histogram", "figure"),
    [Input("map", "hoverData"),
     Input("slider", "value")]
)
def histogram(hoverData, year_value):
    pays = hoverData['points'][0]["location"]
    df_histogram = df_histo.query("Country=='" + pays + "' and Year<=" + str(year_value)).copy()
    df_histogram["Year"] = df_histogram["Year"].astype(str)
    fig = px.histogram(df_histogram,
                       x="Year",
                       y="Electricity (TWh)",
                       color="Electricity mode",
                       color_discrete_map=color_map,
                       opacity=0.8)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        geo=dict(bgcolor="rgba(239.0625, 239.0625, 239.0625, 1)"),
        height=300,
        margin=dict(l=50, r=20, t=20, b=100),
    )
    fig.update_yaxes(title_text="")
    return fig