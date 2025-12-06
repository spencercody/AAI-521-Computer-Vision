from dash import dcc, html
import dash_bootstrap_components as dbc
import ids


def render():
    return dbc.Col(
        [
            html.H3("Drop an image from mall dataset below", style={"textAlign": "center"}),
            dcc.Upload(
                id=ids.UPLOAD_IMAGE,
                children=html.Div(["Drag and Drop or ", html.A("Select .jpg file")]),
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                    'backgroundColor':'#e8e8e8'
                },
                # Allow multiple files to be uploaded
                multiple=False,
            ),
        ]
    )
