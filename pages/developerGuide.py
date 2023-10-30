import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    name="Developer guide",
    guide=True,
)


THEME = "plotly_dark"

layout = html.Div(
    className="content",
    children=[
        html.H1('This is our developer guide page'),
    ]
)
