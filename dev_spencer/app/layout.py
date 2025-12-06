from dash import html
import dash_bootstrap_components as dbc
from components import drop_image, output_drop_img, dataset_link


def serve_layout():
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H1(
                                "CNN Crowd Counting",
                                style={"textAlign": "center", "padding": "10px"},
                            ),
                        ],
                        width=8,
                    ),
                ],
                align="center",
                justify="center",
                style={"backgroundColor": "#e8e8ff"},
            ),
            dbc.Row(
                [dbc.Col([dataset_link.render()], width=2)],
                align="start",
                justify="end",
                #style={"backgroundColor": "#e8e8ff"},
            ),
            html.Hr(),
            dbc.Row(
                [dbc.Col(drop_image.render(), width=8)],
                align="center",
                justify="center",
            ),
            output_drop_img.render(),
            html.Hr(),
            html.Br(),
            html.Hr(),
            html.Br()
        ]
    )
