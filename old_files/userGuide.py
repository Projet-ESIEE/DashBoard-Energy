import dash
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    name="User guide",
    guide=True,
)

THEME = "plotly_dark"

layout = html.Div(
    className="content",
    children=[
        html.H1('This is our User guide page'),
    ]
)
