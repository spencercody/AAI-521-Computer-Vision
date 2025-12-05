from dash import Dash
from layout import serve_layout
import dash_bootstrap_components as dbc
#from callbacks import register_callbacks
from components import callbacks

def create_app():
    app = Dash(__name__, 
               suppress_callback_exceptions=True, 
               external_stylesheets=[dbc.themes.ZEPHYR],
               title='CNN Crowd Counter'
               )
    # Set layout as a function (Dash will call it each page load)
    app.layout = serve_layout

    # Register callbacks
    #register_callbacks(app)

    return app

# Run server
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)