import base64
import io
import numpy as np
from PIL import Image
import os
import pandas as pd
from dash import html
import dash_bootstrap_components as dbc
from pathlib import Path
from tensorflow.keras.models import load_model


def decode_image(contents):
    """Decode base64 image into a PIL image."""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    return Image.open(io.BytesIO(decoded))


# ---------------------------------------------------------------------------- #


def encode_image(pil_img):
    """Encode a PIL image back to base64 for Dash."""
    buff = io.BytesIO()
    pil_img.save(buff, format="PNG")
    encoded = base64.b64encode(buff.getvalue()).decode("utf-8")
    return "data:image/png;base64," + encoded


# ---------------------------------------------------------------------------- #


def manual_img_preprocessing(pil_img):
    IMAGE_SIZE = (128, 128)
    pil_img = pil_img.resize(IMAGE_SIZE)
    img_array = np.array(pil_img) / 255.
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array


# ---------------------------------------------------------------------------- #

def get_model_prediction(img):
    model = fetch_model()
    prediction_result = model.predict(img)
    final_result = int(round(prediction_result[0][0]))

    return final_result
# ---------------------------------------------------------------------------- #


def parse_uploaded_img(content, file_name):
    pil_img = decode_image(content)
    img = manual_img_preprocessing(pil_img)

    true_count = fetch_true_count(file_name)

    predicted_count = get_model_prediction(img)
    

    return predicted_count, true_count


# ---------------------------------------------------------------------------- #


def output_counts(content, file_name) -> list:
    model_count, true_count = parse_uploaded_img(content, file_name)
    
    return dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3(file_name),
                        html.Img(
                            src=content, style={"maxWidth": "75%", "marginTop": "20px"}
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.H4(f"True count = {true_count}", style={'color':'navy', 'fontWeight': 'bold'}),
                        html.H4(f"Model count = {model_count}", style={'color':'red', 'fontWeight': 'bold'}),
                    ],
                    width=3,
                    style={'backgroundColor':'#f5f5f5',
                           "border": "1px solid",
                            "padding": "20px",
                            "borderRadius": "10px"
                            }
                ),
            ],
            justify='center',
            align='center'
        )
    #]


# ---------------------------------------------------------------------------- #


def get_img_filename(image_id: int) -> str:
    image_id = str(image_id).rjust(6, "0")
    img_name = f"seq_{image_id}.jpg"
    return img_name


# ---------------------------------------------------------------------------- #


def get_labels_df(labels_csv_path: str = None):
    if labels_csv_path is None:
        current_file_path = Path(__file__).resolve()
        current_file_directory = current_file_path.parent
        file_name = 'labels.csv'
        labels_csv_path = current_file_directory / file_name
    assert os.path.exists(
        labels_csv_path
    ), f"unable to locate the labels.csv file at {labels_csv_path}"

    df = pd.read_csv(labels_csv_path)
    df["img_file_name"] = df.id.apply(lambda x: get_img_filename(x))

    return df


# ---------------------------------------------------------------------------- #


def fetch_true_count(file_name: str):
    df = get_labels_df()
    df = df[df.img_file_name == file_name.lower()].copy()

    if df.empty:
        return "Unable to find true count"

    return df['count'].iloc[0]


# ---------------------------------------------------------------------------- #

def fetch_model():
    current_file_path = Path(__file__).resolve()
    current_file_directory = current_file_path.parent

    model_path = current_file_directory / '..' / '..' / 'models' / 'cnn-counting-model-25Nov2025-0004.keras'
    assert os.path.exists(
        model_path
    ), f"unable to locate the model file at {model_path}"

    model = load_model(model_path)

    return model
