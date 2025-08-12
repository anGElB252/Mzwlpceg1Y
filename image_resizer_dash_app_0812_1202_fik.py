# 代码生成时间: 2025-08-12 12:02:28
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
from PIL import Image
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory

# Define the application layout
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Image Resizer Dashboard"),
    dcc.Upload(
        id='image_upload',
        children=html.Div([html.Button('Upload', id='upload-button'), html.I('Drag and Drop or Click to Upload Image')]),
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
               'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
               'textAlign': 'center', 'margin': '10px'},
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='image-upload-container'),
    html.Div(id='output-container')
])

# Ensure the uploaded file is secure
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Resize image function
def resize_image(image_path, width, height):
    try:
        with Image.open(image_path) as img:
            resized_img = img.resize((width, height), Image.ANTIALIAS)
            return resized_img
    except IOError:
        print('Error opening image file.')
        return None

# Update the layout with uploaded image after resizing
@app.callback(
    Output('image-upload-container', 'children'),
    Input('image_upload', 'contents'),
    State('image_upload', 'filename'),
    prevent_initial_call=True
)
def update_output(uploaded_files, filename):
    if uploaded_files is not None:
        children = []
        for file, file_name in zip(uploaded_files, filename):
            if allowed_file(file_name):
                # Save the uploaded file to disk
                save_path = os.path.join('temp', secure_filename(file_name))
                with open(save_path, 'wb') as f:
                    f.write(file)

                # Resize the image and create the output container
                resized_img = resize_image(save_path, 300, 300)
                if resized_img is not None:
                    resized_img.save(save_path)
                    children.append(html.Img(src=save_path, id='resized-image', style={'width': '100%', 'height': 'auto'}))
                else:
                    children.append(html.Div('Image could not be resized.'))
            else:
                children.append(html.Div(f'{file_name} is not a supported file extension.'))
    return children

# Serve the uploaded images
@app.server.route("/temp/<filename>")
def serve_temp_file(filename):
    return send_from_directory('temp', filename)

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
