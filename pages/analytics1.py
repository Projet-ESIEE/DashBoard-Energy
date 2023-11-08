import dash
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

THEME = "plotly_white"

area_options = {
    'Continent': df_energy['Continent'].unique(),
    'Region': df_energy['Region'].unique(),
    'Country': df_energy['Country'].unique(),
}


def df_energy_query(area_type: str, area_name: str) -> pd.DataFrame:
    """
    The function df_energy_query return a filtered dataframe of df_energy.
    It useful because the computation is done only one time.
    :param area_type: ["Entity", "Continent", "Region", "iso3"]
    :param area_name: ["France", "Europe", "Western Europe", "FRA", ...]
    :return: a pandas dataframe which is subpart of the df_energy
    """
    return df_energy.query(f"{area_type} == '{area_name}'")


def get_na_info(area_type: str, area_name: str) -> tuple:
    """
    Give information about the missing values of the dataframe
    :param area_type: ["Entity", "Continent", "Region", "iso3"]
    :param area_name: ["France", "Europe", "Western Europe", "FRA", ...]
    :return: NB_OF_NAN, NB_OF_NAN_GLOBAL, NB_MEAN_NAN
    """
    NB_OF_NAN = df_energy_query(area_type, area_name).isna().sum().sum()
    NB_OF_NAN_GLOBAL = df_energy.isna().sum().sum()
    NB_MEAN_NAN = (NB_OF_NAN_GLOBAL / len(df_energy[area_type].unique()))
    # compare the nb of nan for the given area_name to the mean of nan of other area_type

    return NB_OF_NAN, NB_OF_NAN_GLOBAL, NB_MEAN_NAN


##################################
#   <-- The layout of the page -->
layout = html.Div(
    className="content",
    children=[
        dcc.Dropdown(
            list(area_options.keys()),
            id='area_type-drop',
            multi=False,
            value="Continent",
            style={'width': '50%', 'display': 'inline-block'}
        ),
        dcc.Dropdown(
            id='area_name-drop',
            style={'width': '50%', 'display': 'inline-block'}
        ),
        dcc.Graph(id="indicator"),
        # html.Hr(),
        dcc.Graph(id="lines_values_percentage"),
        dcc.Graph(id="heatmap_missing_values"),
        dcc.Graph(id="histo_hdi"),
    ]
)


##################################
#   <-- The dropdown menu -->
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
# <-- Indicator_missing_values -->
@callback(Output(component_id="indicator", component_property="figure"),
          # Input(component_id="df_filter", component_property="data"),
          Input(component_id="area_type-drop", component_property="value"),
          Input(component_id="area_name-drop", component_property="value"))
def graph_indicator(area_type: str, area_name: str) -> go.Figure:
    """
    The indicator function give a subplot with the more relevant information
    :param area_type: ["Entity", "Continent", "Region", "iso3"]
    :param area_name: ["France", "Europe", "Western Europe", "FRA", ...]
    :return: go.Figure.Indicator | 1 row / 4 col | nub of : features, Country, ..., nan for a given area_name
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
        title={"text": f"Number of nan<br>"
                       "<span style='font-size:0.8em;color:gray'>"
                       f"in the dataset</span>"
               }
    ),
        row=1, col=3
    )

    indicator.add_trace(go.Indicator(
        mode="number+delta",  # 'delta' mean the % btw the value and a ref
        value=NB_OF_NAN,  # nb of nan for the current country looked
        delta={'reference': int(NB_MEAN_NAN), 'relative': True, 'valueformat': '.2f', "suffix": "%"},
        title={"text": f"Number of nan for {area_name}<br>"
                       "<span style='font-size:0.8em;color:gray'>"
                       f"compare to the mean of {area_type}</span>"
               }
    ),
        row=1, col=4
    )
    indicator.update_layout(
        height=230,
        template=THEME,
    )

    return indicator


##################################
#   <-- heatmap_missing_values -->
@callback(Output(component_id="heatmap_missing_values", component_property="figure"),
          # Input(component_id="df_filter", component_property="data"),
          Input(component_id="area_type-drop", component_property="value"),
          Input(component_id="area_name-drop", component_property="value"))
def graph_heatmap_missing_values(area_type: str, area_name: str) -> go.Figure:
    """
    This function creat a complexe multi-figure within a heatmap of missing values for :
    - the given area_name
    - all features
    - an indicator trace.
    :param area_type: ["Entity", "Continent", "Region", "iso3"]
    :param area_name: ["France", "Europe", "Western Europe", "FRA", ...]
    :return: a figure object of the plotly lib (heatmap + indicator)
    """
    # The set of var to observe except the one used on other axis
    col = df_energy.columns.tolist()
    for x in ['Year', 'Country', 'Continent', 'Region', 'iso3']: col.remove(x)

    df_heat = df_energy_query(area_type, area_name)[col]  # make the df with for the given area_name
    df_heat_na = df_heat.isna()
    df_heat_na.replace({True: 1, False: 0}, inplace=True)  # We change the True to 1 because plotly can't interpret them

    df_heat_na['Year'] = df_energy['Year']  # add the year column to the df
    transposed_df = df_heat_na.groupby('Year').sum().T

    # testing after the upper calculation to be sure that the nb of missing val and shape is plausible
    assert transposed_df.sum().sum() == df_energy_query(area_type, area_name).isna().sum().sum(), \
        "<-- The sum of nan is  not the same -->"
    assert transposed_df.shape[0] == len(col), "<-- The number of columns is not the same -->"
    assert transposed_df.shape[1] == len(
        df_energy['Year'].unique().tolist()), "<-- The number of rows is not the same -->"

    heatmap = go.Figure()
    heatmap.add_trace(go.Heatmap(
        z=transposed_df, x=df_energy['Year'].unique().tolist(), y=col,
        # Styling
        colorscale='aggrnyl',
        colorbar=dict(
            title="",
            titleside="right"
        ),
    ))
    heatmap.update_layout(
        height=430,
        template=THEME,
        title=f"Number of missing values across years for countries of {area_name}"
    )

    return heatmap


@callback(Output(component_id="lines_values_percentage", component_property="figure"),
          Input(component_id="area_type-drop", component_property="value"),
          Input(component_id="area_name-drop", component_property="value"))
def graph_lines_percentage(area_type: str, area_name: str) -> go.Figure:
    """
    Draw a lines chart with years on x-axis and values in % on y-axis. It shows the evolution of serval variables for
    a given area_name. The evolution of pourcentage take year 2000 as reference.
    :param area_type: ["Entity", "Continent", "Region", "iso3"]
    :param area_name: ["France", "Europe", "Western Europe", "FRA", ...]
    :return: go.Figure.line object, with a centered legend
    """

    df_normalized = df_energy_query(area_type, area_name)
    df_normalized = df_normalized.replace(0, 1)

    cols_to_normalize = df_normalized.columns.difference(
        ['Country', 'Year', 'Continent', 'Region', 'iso3', 'Access to Electricity (%)', 'Low-Carbon Electricity (%)',
         'Renewables (% Equivalent Primary Energy)'])
    # Exclure les colonnes non numériques et celle qui sont deja en %

    assert df_normalized[cols_to_normalize].apply(
        lambda s: pd.to_numeric(s, errors='coerce').notnull().all()).sum() != 9, "<-- All values are not numeric -->"

    # Créez un masque pour exclure les années autres que 2000
    mask_2000 = (df_normalized['Year'] == 2000)
    df_normalized_2000 = df_normalized[mask_2000][cols_to_normalize].reindex(df_normalized.index, method='pad',
                                                                             fill_value=1)

    df_normalized[cols_to_normalize] = ((df_normalized[cols_to_normalize] - df_normalized_2000[
        cols_to_normalize]) / df_normalized_2000) * 100

    df_line = df_normalized.groupby("Year").sum()

    lines = px.line(df_line, x=df_line.index, y=cols_to_normalize,
                    markers=True, log_y=False,
                    title="Evolution in % with 2000 as reference",
                    # template=THEME,
                    )

    # Change the name of the variable in the légend. The goal is to have a better render and have shortened name
    legend_new = {
        'CO2 Emissions (kt by country)': 'CO2 Emissions',
        'Electricity from Fossil Fuels (TWh)': 'Electricity Fossil',
        'Electricity from Nuclear (TWh)': 'Electricity Nuclear',
        'Electricity from Renewables (TWh)': 'Electricity Renewables',
        'GDP Growth': 'GDP Growth',
        'GDP per Capita': 'GDP per Capita',
        'Human Development Index': 'HDI',
        'Primary Energy Consumption per Capita (kWh/person)': 'Primary Energy',
        'Renewable Electricity Capacity per Capita': 'Renewable Electricity'
    }

    lines.for_each_trace(lambda t: t.update(name=legend_new[t.name]))
    # legendgroup = legend_new[t.name],
    # hovertemplate = t.hovertemplate.replace(t.name, legend_new[t.name])

    lines.update_layout(

        legend=dict(
            orientation="h",
            entrywidth=70,
            yanchor="bottom",
            y=-0.5,
            xanchor="right",
            x=1
        ),
    )
    return lines


@callback(Output(component_id="histo_hdi", component_property="figure"),
          Input(component_id="area_type-drop", component_property="value"),
          Input(component_id="area_name-drop", component_property="value"), )
def graph_histo_hdi(area_type: str, area_name: str, reference_year: int = 2020) -> go.Figure:
    """
    The functino graph_histo_HDI make a histogram with the frequency of HDI for a given area type.
    The slider change the year of observation and a marginal distribution as a box plot.
    The area name is the current country observed.
    :param reference_year: an int in [2000, 2020]
    :param area_type: ["Entity", "Continent", "Region", "iso3"]
    :param area_name: ["France", "Europe", "Western Europe", "FRA", ...]
    :return: go.Figure.histogram
    """
    df_histo = df_energy_query(area_type, area_name)
    df_histo_filtered = df_histo[['Year', 'Country', 'Continent', 'Region', 'Human Development Index']]

    # Creation of the feature 'reference' that is a boolean.
    reference = pd.DataFrame({'reference': df_histo_filtered['Year'] == reference_year})  # chatGPT
    df_histo_filtered = pd.concat([df_histo_filtered, reference], axis=1)

    histo = px.histogram(df_histo_filtered,
                         x="Human Development Index",
                         marginal="box",  # ["rug", "box", "violin"]
                         color='reference',
                         title=f"Histogram Human Development Index per year for countries in {area_name}",
                         pattern_shape='reference',
                         opacity=1,
                         template=THEME,
                         text_auto=True,
                         animation_frame="Year",
                         )

    histo.update_layout(
        showlegend=False,
        transition={'duration': 10000},
        yaxis_title="Number of country",
    )

    return histo
