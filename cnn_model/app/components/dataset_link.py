from dash import html


def render():
    link = 'https://www.kaggle.com/datasets/fmena14/crowd-counting'
    return html.A('Link to Dataset', href=link, target="_blank")