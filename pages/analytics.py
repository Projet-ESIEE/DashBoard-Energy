import dash, pandas as pd, plotly.express as px
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__, order=2)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

layout = html.Div(
    className="content",
    children=[
        html.H1('This is our Analytics page'),
        html.Div('Here will be the main pages of our work'),
        dcc.Graph(id='graph-with-slider'),
        dcc.Slider(
            df['year'].min(),
            df['year'].max(),
            step=None,
            value=df['year'].min(),
            marks={str(year): str(year) for year in df['year'].unique()},
            id='year-slider'
        )
    ]
)


@callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig
