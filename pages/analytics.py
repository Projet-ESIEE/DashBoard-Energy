import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__, order=2)

layout = html.Div([
    html.H1('This is our Analytics page'),
    html.Div('Here will be the main pages of our work'),

    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
                 ['Montréal', 'San Francisco'],
                 multi=True),
    html.P('https://dash.plotly.com/layout#core-components')
])