from dash import Input, Output, State, callback, html
import ids
from components.utils_components import output_counts

@callback(
    Output(ids.OUTPUT_UPLOAD, 'children'),
    Input(ids.UPLOAD_IMAGE, 'contents'),
    Input(ids.UPLOAD_IMAGE, 'filename'),
    prevent_initial_call=True
    )

def update_output(content, filename):
    if content is None:
        return html.Div('Upload an image to begin')
    
    #acceptable_types = ['jpeg', 'jpg', 'png']
    children = output_counts(content, filename)

    return children

    # return html.Div([
    #             html.H5(filename),
    #             html.Img(src=content, style={"maxWidth": "100%", "marginTop": "20px"})
    #         ])

