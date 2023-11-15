import dash
import dash_bootstrap_components as dbc

external_stylesheets1 = dbc.themes.COSMO
external_stylesheets2 = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[external_stylesheets1],
)


navbar = dbc.NavbarSimple([
    dbc.Nav(
        [
            dbc.NavLink(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page.get("top_nav")
        ],
    ),
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page.get("analytics")
        ],
        nav=True,
        label="Analytics",
    ),
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page.get("guide")
        ],
        nav=True,
        label="Guides",
    )],
    brand="Dash board - Energy",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(
    [dash.html.Link(rel='stylesheet', href='/assets/style.css'),
        navbar,
        dash.page_container],
    fluid=True,
)


if __name__ == "__main__":
    app.run_server(debug=False)

