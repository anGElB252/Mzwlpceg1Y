# 代码生成时间: 2025-09-13 21:45:17
import os
import re
from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate

"""
Batch File Renamer Tool
====================

This script provides a Dash-based web application for batch renaming files.
It allows users to specify a directory and a pattern to rename files.
"""

# Define the directory path and regex pattern in the layout
DIRECTORY_PATH = "/path/to/your/directory"

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Batch File Renamer"),
    html.Div(["Enter directory path: ", dcc.Input(id='dir-path', type='text')],
    html.Button("Load Files", id="load-files-button"),
    html.Div(id="file-list-div"),
    html.Div(["Enter regex pattern: ", dcc.Input(id='regex-pattern', type='text')],
    html.Button("Rename Files", id="rename-files-button"),
    html.Div(id="rename-status")
])

# Callback to load files from the directory
@app.callback(
    Output("file-list-div", "children"),
    [Input("load-files-button", "n_clicks")],
    [State("dir-path", "value")]
)
def load_files(n_clicks, dir_path):
    if n_clicks is None:
        raise PreventUpdate()
    try:
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        return html.Ul([html.Li(f) for f in files])
    except Exception as e:
        return html.Div(f"Error loading files: {e}")

# Callback to rename files based on the regex pattern
@app.callback(
    Output("rename-status", "children"),
    [Input("rename-files-button", "n_clicks")],
    [State("dir-path", "value"), State("regex-pattern", "value"), State("file-list-div", "children")]
)
def rename_files(n_clicks, dir_path, regex_pattern, file_list_div):
    if n_clicks is None:
        raise PreventUpdate()
    try:
        pattern = re.compile(regex_pattern)
        files = file_list_div.children[0].children
        renamed_files = []
        for file in files:
            file_name, file_extension = os.path.splitext(file.children[0])
            new_file_name = pattern.sub("", file_name) + file_extension
            new_file_path = os.path.join(dir_path, new_file_name)
            old_file_path = os.path.join(dir_path, file.children[0])
            os.rename(old_file_path, new_file_path)
            renamed_files.append(html.Li(f"Renamed {file.children[0]} to {new_file_name}"))
        return html.Ul(renamed_files)
    except re.error as e:
        return html.Div(f"Invalid regex pattern: {e}")
    except Exception as e:
        return html.Div(f"Error renaming files: {e}")

if __name__ == "__main__":
    app.run_server(debug=True)
