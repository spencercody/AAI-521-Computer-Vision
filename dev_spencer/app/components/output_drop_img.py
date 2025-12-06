from dash import html, dcc
import ids

def render():
    return dcc.Loading(html.Div(id= ids.OUTPUT_UPLOAD))