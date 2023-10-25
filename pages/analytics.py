import dash
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__, order=2)

path_energy = os.path.join("dataset", "energy-cleaned-dataset.csv")
df_energy = pd.read_csv(path_energy)
THEME = "plotly_dark"

area_options = {
    'Continent': df_energy['Continent'].unique(),
    'Region': df_energy['Region'].unique(),
    'Entity': df_energy['Country'].unique()
}


def line_plot_missing_values() -> go.Figure:
    """
    The line_plot_missing_values function plot the number of na by years
    :return:
    """
    missing_values_by_year = df_energy.groupby("Year").apply(lambda x: x.isna().sum().sum())

    # Create a line chart
    fig_na = px.line(
        x=missing_values_by_year.index,
        y=missing_values_by_year,
        template=THEME,  # Assuming THEME is defined elsewhere
        labels={"x": "Years", "y": "Missing values count"},
        range_y=[0, 400],
        markers=True,
        title="Evolution of missing values over time",
    )

    return fig_na


def bar_graph_missing_values() -> go.Figure:
    """

    :return:
    """
    serie_na = df_energy.isnull().sum().sort_values(ascending=False)
    serie_na.rename('Null Values', inplace=True)

    fig_null_data = go.Figure(go.Bar(
        x=serie_na.index,
        y=serie_na,
        text=serie_na,
        textposition='auto'
    ))

    fig_null_data.update_layout(
        title='Null Values Count',
        xaxis_tickfont_size=12,
        template=THEME,
    )

    return fig_null_data


layout = html.Div(
    className="content",
    children=[
        html.H1('This is our Analytics page'),
        dcc.Graph(figure=bar_graph_missing_values()),
        html.P("As we can see there is a lot of missing values..."),
        dcc.Graph(figure=line_plot_missing_values()),
        html.P("But this is not caused by the age"),
        html.Br(),
        html.P("Let's have a deeper look to missing data"),
        html.H3("Select an area"),

        html.Label('Multi-Select Dropdown Continent'),
        html.Br(),
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
        dcc.Graph(id="heatmap_missing_values"),
        html.Br(),
        dcc.Graph(id="histo_hdi")



    ]
)


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


################################
################################
################################

@callback(Output(component_id="heatmap_missing_values", component_property="figure"),
          Input(component_id="area_type-drop", component_property="value"),
          Input(component_id="area_name-drop", component_property="value"))
def heatmap_missing_values(area_type: str = "Continent", area_name: str = "Europe") -> go.Figure:
    """
    This function creat a complexe multi-figure within a heatmap of missing values for the given area_name for all features and an indicator trace.
    :param df_heatmap: The data frame to analyse
    :param area_type: ["Entity", "Continent", "Region", "iso3"]
    :param area_name: ["France", "Europe", "Western Europe", "FRA", ...]
    :return: a figure object of the plotly lib (heatmap + indicator)
    """

    ###############
    ## Computation
    ###############
    # The set of var to observe except the one used on other axis
    col = df_energy.columns.tolist()
    for x in ['Year', 'Country', 'Continent', 'Region', 'iso3']: col.remove(x)

    df_heat = df_energy.query(f"{area_type} == '{area_name}'")[col]  # make the df with for the given area_name
    df_heat_na = df_heat.isna()
    df_heat_na.replace({True: 1, False: 0},
                       inplace=True)  # We change the True to 1 because plotly can not interpret them

    # compute the values for the indicator
    NB_OF_NAN = df_heat_na.sum().sum()
    NB_OF_NAN_GLOBAL = df_energy.isna().sum().sum()
    NB_MEAN_NAN = (NB_OF_NAN_GLOBAL / len(df_energy[area_type].unique()))
    # compare the nb of nan for the given area_name to the mean of nan of other area_type

    df_heat_na['Year'] = df_energy['Year']  # add the year column to the df
    transposed_df = df_heat_na.groupby('Year').sum().T

    # testing after the upper calculation to be sure that the nb of missing val and shape is plausible
    assert transposed_df.sum().sum() == df_energy.query(
        f"{area_type} == '{area_name}'").isna().sum().sum(), "<-- The sum of nan is not the same -->"
    assert transposed_df.shape[0] == len(col), "<-- The number of columns is not the same -->"
    assert transposed_df.shape[1] == len(
        df_energy['Year'].unique().tolist()), "<-- The number of rows is not the same -->"

    ###############
    ## The subplot
    ###############
    heatmap = make_subplots(
        rows=1, cols=2,  # 2 col bcs 2 graph
        column_widths=[0.9, 0.2],
        specs=[[{"type": "xy"}, {"type": "domain"}]],
        subplot_titles=("Heatmap des valeurs manquantes par année et par variable", "")
    )

    ##### The heatmap
    heatmap.add_trace(
        go.Heatmap(
            z=transposed_df,
            x=df_energy['Year'].unique().tolist(),
            y=col,

            # Styling
            colorscale='Viridis',
            colorbar=dict(
                title="nombre",
                titleside="top"
            )
        ),
        # placement of the graph in 1st position
        row=1, col=1
    )

    ###### The indicator
    heatmap.add_trace(
        go.Indicator(
            mode="number+delta",  # 'delta' mean the % btw the value and a ref
            value=NB_OF_NAN,  # nb of nan for the current country looked
            delta={'reference': int(NB_MEAN_NAN), 'relative': True, 'valueformat': '.2f', "suffix": "%"},
            # styling
            title={"text": f"NN of nan for {area_name}<br>"
                           "<span style='font-size:0.8em;color:gray'>"
                           f"compare to the mean of {area_type}</span>"
                   }
        ),
        # placement of the graph in 2nd position
        row=1, col=2
    )

    ##### styling
    heatmap.update_layout(
        template=THEME,  # just a default theme
        title_text="Observation of missing values for : {}".format(area_name),
        title_font_size=24,  # Increase title font size
        title_x=0.5,  # Center the title
        height=800,  # Set the height of the figure in pixels
        # width=1000,  # Set the width of the figure in pixels
        font=dict(family='Arial', size=12),  # Customize font family and size for the whole figure
        # margin=dict(t=80, l=50, r=50, b=50),  # Add margin for better layout spacing
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
    df_histo = pd.DataFrame(data=df_energy, columns=['Year', 'Country', 'Continent', 'Region', 'Human Development Index'])

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
                         template=THEME,
                         text_auto=True,
                         animation_frame="Year",
                         )

    return histo
