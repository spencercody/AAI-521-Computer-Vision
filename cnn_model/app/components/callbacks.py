from dash import Input, Output, callback, html
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
        return html.Div('Upload an image to begin (.jpg or .png only)',
                        style={"textAlign": "center"}
                        )
    
    file_ext = filename.split('.')[-1]
    acceptable_types = ['jpeg', 'jpg', 'png']

    if file_ext.lower() not in acceptable_types:
        return html.Div(f'Invalid file type: {file_ext}. Only jpg or png images are accepted.',
                        style={"textAlign": "center"}
                        )
    
    children = output_counts(content, filename)

    return children


