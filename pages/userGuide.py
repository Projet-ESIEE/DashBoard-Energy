import dash
from dash import html, dcc

dash.register_page(
    __name__,
    name="User guide",
    guide=True,
)


layout = html.Div(
    className="content",
    children=[
        html.H1('This is our User guide page'),
    ]
)
