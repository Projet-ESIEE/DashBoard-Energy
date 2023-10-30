import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO

# select the Bootstrap stylesheets and figure templates for the theme toggle here:
# url_theme1 = dbc.themes.FLATLY
# url_theme2 = dbc.themes.DARKLY
# theme_toggle = ThemeSwitchAIO(
#     aio_id="theme",
#     themes=[url_theme2, url_theme1],
#     icons={"left": "fa fa-sun", "right": "fa fa-moon"},
# )
external_stylesheets1 = dbc.themes.CYBORG
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
            if page.get("analitic")
        ],
        nav=True,
        label="Analitics",
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
    [navbar, dash.page_container],
    fluid=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)

