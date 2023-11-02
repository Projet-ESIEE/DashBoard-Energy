import dash
import os
from dash import html

dash.register_page(__name__, order=4)

gif_path = os.path.join("assets", "404.gif")

layout = html.Div(
    className="content-centered",
    children=[
        html.H1('There is nothing here..'),
        html.Img(src=gif_path, alt="404"),
    ]
)
