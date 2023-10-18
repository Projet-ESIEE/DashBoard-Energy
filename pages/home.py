import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div(
    className="content",
    children=[
        html.H2('This is our Home page'),
        html.Div('This is our Home page content. With our git hub, the dataset origine, one map and so on'),
        html.P('just a test')
])