import dash
import pandas, numpy as np
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    name="Missing values",
    analytics=True,
    order=2
)

##################################
#   <-- variable call and init -->
path_energy = os.path.join("dataset", "energy-cleaned-dataset.csv")
df_energy = pd.read_csv(path_energy)
THEME = "plotly_dark"

area_options = {
    'Continent': df_energy['Continent'].unique(),
    'Region': df_energy['Region'].unique(),
    'Entity': df_energy['Country'].unique()
}


# @callback(Output(component_id="df_filter", component_property="data"),
#          Input(component_id="area_type-drop", component_property="value"),
#          Input(component_id="area_name-drop", component_property="value"))
def df_energy_query(area_type: str, area_name: str) -> pd.DataFrame:
    """
    The function df_energy_query return a filtered dataframe of df_energy.
    It useful because the computation is done only one time.
    :param area_type:
    :param area_name:
    :return: a pandas dataframe which is subpart of the df_energy
    """
    return df_energy.query(f"{area_type} == '{area_name}'")


def get_na_info(area_type: str, area_name: str):
    # compute the values for the indicator
    NB_OF_NAN = df_energy_query(area_type, area_name).isna().sum().sum()
    NB_OF_NAN_GLOBAL = df_energy.isna().sum().sum()
    NB_MEAN_NAN = (NB_OF_NAN_GLOBAL / len(df_energy[area_type].unique()))
    # compare the nb of nan for the given area_name to the mean of nan of other area_type

    return NB_OF_NAN, NB_OF_NAN_GLOBAL, NB_MEAN_NAN

fig_null_data = go.Figure(go.Bar(
        x=serie_na.index,
        y=serie_na,
        text=serie_na,
        textposition='auto'
    ))

##################################
layout = html.Div(
    className="content",
    children=[
        dcc.Dropdown(
            list(area_options.keys()),
            id='area_type-drop',
            multi=False,
            value="Continent",
            style={'width': '48%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='area_name-drop',
            style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id="indicator"),
        dcc.Graph(id="heatmap_missing_values"),
        dcc.Graph(id="lines_graph"),
        dcc.Graph(id="histo_hdi"),
    ]
)
#   <-- The dash app layout -->


@callback(
    Output('area_name-drop', 'options'),
    Input('area_type-drop', 'value'))
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in area_options[selected_country]]


@callback(
    Output('area_name-drop', 'value'),
    Input('area_name-drop', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']


##################################
#   <-- heatmap_missing_values -->
@callback(Output(component_id="indicator", component_property="figure"),
          # Input(component_id="df_filter", component_property="data"),
          Input(component_id="area_type-drop", component_property="value"),
          Input(component_id="area_name-drop", component_property="value"))
def indicator(area_type: str, area_name: str) -> go.Figure:
    """
    The indicator function give a subplot with main information
    :param area_type:
    :param area_name:
    :return:
    """
    NB_OF_NAN, NB_OF_NAN_GLOBAL, NB_MEAN_NAN = get_na_info(area_type, area_name)
    indicator = make_subplots(
        rows=1, cols=4,
        # column_widths=[0.3, 0.3, 0.3],
        specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}, {"type": "domain"}]],
    )
    indicator.add_trace(go.Indicator(
        mode="number",
        value=df_energy.shape[1],
        title={"text": f"Number of feature<br>"
                       "<span style='font-size:0.8em;color:gray'>"
                       f"in the dataset</span>"
               }
    ),
        row=1, col=1
    )

    indicator.add_trace(go.Indicator(
        mode="number",
        value=len(df_energy.Country.unique()),
        title={"text": f"Number of Country<br>"
                       "<span style='font-size:0.8em;color:gray'>"
                       f"in the dataset</span>"
               }
    ),
        row=1, col=2
    )

    indicator.add_trace(go.Indicator(
        mode="number",
        value=NB_OF_NAN_GLOBAL,
        title={"text": f"Number of nan for {area_name}<br>"
                       "<span style='font-size:0.8em;color:gray'>"
                       f"compare to the mean of {type}</span>"
               }
    ),
        row=1, col=3
    )

    indicator.add_trace(go.Indicator(
        mode="number+delta",  # 'delta' mean the % btw the value and a ref
        value=NB_OF_NAN,  # nb of nan for the current country looked
        delta={'reference': int(NB_MEAN_NAN), 'relative': True, 'valueformat': '.2f', "suffix": "%"},
        title={"text": f"NN of nan for {area_name}<br>"
                       "<span style='font-size:0.8em;color:gray'>"
                       f"compare to the mean of {type}</span>"
               }
    ),
        row=1, col=4
    )
    indicator.update_layout(
        height=230,
    )

    return indicator


##################################
#   <-- heatmap_missing_values -->
@callback(Output(component_id="heatmap_missing_values", component_property="figure"),
          # Input(component_id="df_filter", component_property="data"),
          Input(component_id="area_type-drop", component_property="value"),
          Input(component_id="area_name-drop", component_property="value"))
def heatmap_missing_values(area_type: str, area_name: str) -> go.Figure:
    """
    This function creat a complexe multi-figure within a heatmap of missing values for the given area_name for all features and an indicator trace.
    # :param df_filtered:
    :param area_type: ["Entity", "Continent", "Region", "iso3"]
    :param area_name: ["France", "Europe", "Western Europe", "FRA", ...]
    :return: a figure object of the plotly lib (heatmap + indicator)
    """
    # The set of var to observe except the one used on other axis
    col = df_energy.columns.tolist()
    for x in ['Year', 'Country', 'Continent', 'Region', 'iso3']: col.remove(x)

    df_heat = df_energy_query(area_type, area_name)[col]  # make the df with for the given area_name
    df_heat_na = df_heat.isna()
    df_heat_na.replace({True: 1, False: 0},
                       inplace=True)  # We change the True to 1 because plotly can not interpret them

    df_heat_na['Year'] = df_energy['Year']  # add the year column to the df
    transposed_df = df_heat_na.groupby('Year').sum().T

    # testing after the upper calculation to be sure that the nb of missing val and shape is plausible
    assert transposed_df.sum().sum() == df_energy.query(
        f"{area_type} == '{area_name}'").isna().sum().sum(), "<-- The sum of nan is  not the same -->"
    assert transposed_df.shape[0] == len(col), "<-- The number of columns is not the same -->"
    assert transposed_df.shape[1] == len(
        df_energy['Year'].unique().tolist()), "<-- The number of rows is not the same -->"

    heatmap = go.Figure()
    heatmap.add_trace(go.Heatmap(
        z=transposed_df,
        x=df_energy['Year'].unique().tolist(),
        y=col,

        # Styling
        colorscale='aggrnyl',
        colorbar=dict(
            title="nombre",
            titleside="top"
        ),
    )
    )
    heatmap.update_layout(
        height=430,
    )

    return heatmap


@callback(Output(component_id="histo_hdi", component_property="figure"),
          Input(component_id="area_type-drop", component_property="value"),
          Input(component_id="area_name-drop", component_property="value"), )
def histo_hdi(area_type: str, area_name: str, reference_year: int = 2020) -> go.Figure:
    """
    histo_HDI make a histogram with the frequency of HDI for a given area type. The slider change the year of observation. The area name is the current country observed.
    :param reference_year:
    :param area_type:
    :param area_name:
    :return:
    """
    # Selection feature needed
    df_histo = pd.DataFrame(data=df_energy,
                            columns=['Year', 'Country', 'Continent', 'Region', 'Human Development Index'])

    # Filtering by the area_name and the year + the reference year for this same are_name
    df_histo_filtered = df_histo.query(f"{area_type} == '{area_name}'")

    # Creation of the feature 'reference' that is a boolean.
    df_histo_filtered['reference'] = df_histo_filtered['Year'] == reference_year

    histo = px.histogram(df_histo_filtered,
                         x="Human Development Index",
                         marginal="box",  # ["rug", "box", "violin"]
                         color="reference",
                         title='Histogram Human Development Index per year with 2020 as reference',
                         pattern_shape="reference",
                         opacity=1,
                         # template=THEME,
                         text_auto=True,
                         animation_frame="Year",
                         )

    return histo
