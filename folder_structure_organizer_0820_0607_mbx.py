# 代码生成时间: 2025-08-20 06:07:12
import os
import shutil
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

"""
Folder Structure Organizer using Dash Framework
This script creates a Dash application that organizes the folder structure
by moving all files and folders into a specified directory structure.
"""

# Define the application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    dbc.CardHeader("Folder Structure Organizer"),
    dbc.CardBody([
        dbc.FormGroup([
            dbc.Label("Source Directory"),
            dbc.Input(id="source_directory", placeholder="Enter source directory", type="text")
        ]),
        dbc.FormGroup([
            dbc.Label("Target Directory"),
            dbc.Input(id="target_directory", placeholder="Enter target directory", type="text")
        ]),
        dbc.Button("Organize", id="organize_button", color="primary"),
        dbc.Alert(id="alert", color="primary")
    ])
])

# Callback to handle the organize button click
@app.callback(
    Output("alert", "children"),
    [Input("organize_button", "n_clicks")],
    [State("source_directory", "value"), State("target_directory", "value\)]
)
def organize_folder_structure(n_clicks, source_dir, target_dir):
    # Check if the button was clicked
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate()
    
    # Validate the source and target directories
    if not os.path.isdir(source_dir):
        return f"Error: Source directory '{source_dir}' does not exist."
    if not os.path.isdir(target_dir):
        return f"Error: Target directory '{target_dir}' does not exist."
    
    # Organize the folder structure
    try:
        for item in os.listdir(source_dir):
            item_path = os.path.join(source_dir, item)
            if os.path.isfile(item_path):
                # Move files to the target directory
                shutil.move(item_path, target_dir)
            elif os.path.isdir(item_path):
                # Move folders to the target directory
                shutil.move(item_path, target_dir)
        return "Folder structure organized successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
