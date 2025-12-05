from dash import html, dcc
import dash_bootstrap_components as dbc
from components import drop_image, output_drop_img

def serve_layout():
    return html.Div(
        [
            dbc.Row(
                [
                    html.H1("CNN Crowd Counting", style={"textAlign": "center"}),
                ]
            ),
            html.Br(),
            html.Hr(),
            dbc.Row(
                [dbc.Col(drop_image.render(),
                         width=8
                         )
                 ],
                 align='center',
                 justify='center'
            ),
            output_drop_img.render()
        ]
    )
