import dash
# import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

from pages.components import footer

app = Dash(__name__, use_pages=True)    # external_stylesheets=[dbc.themes.CYBORG],)

app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container,
    footer.footer(),
    ]
)


if __name__ == '__main__':
    app.run(debug=True)
