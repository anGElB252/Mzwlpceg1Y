# 代码生成时间: 2025-08-31 18:08:29
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import base64
import io
from PIL import Image
import os

# Function to resize an image
def resize_image(image_path, output_path, size):
    """
    Resizes an image to the specified size and saves it to the output path.
    
    Parameters:
    image_path (str): Path to the image file.
    output_path (str): Path to save the resized image.
    size (tuple): A tuple of (width, height) for the new size.
    """
    try:
        with Image.open(image_path) as img:
            img = img.resize(size)
            img.save(output_path)
    except IOError:
        print(f"Error opening or processing image file: {image_path}")

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Image Dimension Batch Resizer"),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ',
                         html.A('Select Files')]),
        # Contents of file are accessed through filename keyword in callback function
        multiple=True
    ),
    dcc.Output(id='output-data-upload'),
    html.Div(id='output-container')
])

# Callback to update the output when files are uploaded
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'))
def update_output(contents):
    if contents is not None:
        # Create a directory for resized images if it does not exist
        resized_path = "resized_images"
        if not os.path.exists(resized_path):
            os.makedirs(resized_path)
        
        # List to store the output for the UI
        output = []
        
        # Loop through each file uploaded
        for i, content in enumerate(contents):
            # Create a file path for the new resized image
            filename = os.path.join(resized_path, os.path.basename(content.filename))
            
            # Convert the file content to a buffer
            buffer = io.BytesIO(content.encode('utf-8'))
            
            # Resize the image to a new size (e.g., (300, 300))
            new_size = (300, 300)
            resize_image(buffer, filename, new_size)
            
            # Append a message to the output list
            output.append(f'Resized {content.filename} to {new_size[0]}x{new_size[1]}')
        
        # Show the messages in the app
        return output
    else:
        return html.Div(id='output-container', children=[html.P('No file currently uploaded')])

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)