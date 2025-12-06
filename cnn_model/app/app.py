from dash import Dash
from layout import serve_layout
import dash_bootstrap_components as dbc
#import callbacks here to register them
from components import callbacks

def create_app():
    app = Dash(__name__, 
               suppress_callback_exceptions=True, 
               external_stylesheets=[dbc.themes.ZEPHYR],
               title='CNN Crowd Counter'
               )
    
    app.layout = serve_layout

    return app

# Run server
if __name__ == "__main__":
    app = create_app()
    app.run(debug=False)