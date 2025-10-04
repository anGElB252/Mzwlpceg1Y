# 代码生成时间: 2025-10-04 22:00:37
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os
import glob
import shutil
from werkzeug.utils import secure_filename

# Define the path for the upload directory
UPLOAD_DIRECTORY = 'uploads/'

# Create the upload directory if it doesn't exist
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1('File Batch Operations Dashboard'),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload Files'),
        multiple=True,
        max_size=10000000  # 10MB limit
    ),
    html.Div(id='output-data-upload'),
    dcc.Button('Move Selected Files', id='move-button', n_clicks=0),
    html.Div(id='output-data-move')
])

# Define a callback for displaying the uploaded files
@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    State('upload-data', 'size'),
    State('upload-data', 'type'))
def update_output(list_of_contents, list_of_names, list_of_dates, list_of_sizes, list_of_types):
    if list_of_contents is not None:
        # Append the file names to the output div
        children = []
        for i in range(len(list_of_contents)):
            children.append(html.H6(list_of_names[i]))
        return children
    return 'No files uploaded yet'

# Define a callback for moving the selected files to a new directory
@app.callback(
    Output('output-data-move', 'children'),
    Input('move-button', 'n_clicks'),
    State('output-data-upload', 'children'))
def move_files(n_clicks, children):
    if n_clicks > 0 and children is not None:
        try:
            # Get the list of selected file names
            file_names = [child.text for child in children if isinstance(child, html.H6)]
            # Move each file to the new directory
            for file_name in file_names:
                src = os.path.join(UPLOAD_DIRECTORY, secure_filename(file_name))
                dst = os.path.join(UPLOAD_DIRECTORY, 'moved', secure_filename(file_name))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.move(src, dst)
            return 'Files moved successfully'
        except Exception as e:
            return f'An error occurred: {e}'
    return 'No files moved yet'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
