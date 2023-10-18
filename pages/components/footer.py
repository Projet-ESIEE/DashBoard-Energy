from dash import html


def footer():
    return html.Footer(
        className="footer",
        children=[
            html.Div(
                className="div_categories",
                children=[
                    html.Div(
                        className="col1",
                        children=html.P("text")
                    ),
                    html.Div(
                        className="col2",
                        children=html.P("text")
                    ),
                    html.Div(
                        className="col3",
                        children=html.P("text")
                    ),
                ]
            )
        ]
    )
