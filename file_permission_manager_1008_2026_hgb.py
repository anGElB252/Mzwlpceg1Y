# 代码生成时间: 2025-10-08 20:26:47
import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import stat

# Define a function to change file permissions
def change_file_permission(file_path, new_permission):
    try:
        # Update file permissions
        os.chmod(file_path, new_permission)
        return f"Permissions for {file_path} changed to {oct(new_permission)}"
    except Exception as e:
        return f"Error changing permissions: {e}"

# Define a function to get current file permissions
def get_file_permissions(file_path):
    try:
        # Get the current permissions
        current_permission = stat.S_IMODE(os.stat(file_path).st_mode)
        return f"Current permissions for {file_path}: {oct(current_permission)}"
    except Exception as e:
        return f"Error getting permissions: {e}"

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the app
app.layout = dbc.Container(
    children=[
        dbc.Row(
            children=[
                dbc.Col(html.H1("File Permission Manager"), width=12)
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Input(id="file-path-input", type="text", placeholder="Enter file path"),
                    width=6
                ),
                dbc.Col(
                    dbc.Button("Change Permissions", id="change-permissions-button", color="primary"),
                    width=2
                ),
                dbc.Col(
                    dbc.Button("Get Permissions", id="get-permissions-button", color="success"),
                    width=2
                )
            ],
            className="mb-4"
        ),
        dbc.Row(
            children=[
                dbc.Col(dcc.Textarea(id="output"), width=12)
            ]
        )
    ],
    fluid=True
)

# Callback to handle changing file permissions
@app.callback(
    Output("output", "value"),
    [Input("change-permissions-button", "n_clicks"), Input("file-path-input", "value"), Input("output", "value")],
    prevent_initial_call=True
)
def change_permissions(n_clicks, file_path, output):
    if n_clicks and file_path:
        return change_file_permission(file_path, new_permission=stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)
    return output

# Callback to handle getting file permissions
@app.callback(
    Output("output", "value"),
    [Input("get-permissions-button", "n_clicks"), Input("file-path-input", "value"), Input("output", "value")],
    prevent_initial_call=True
)
def get_permissions(n_clicks, file_path, output):
    if n_clicks and file_path:
        return get_file_permissions(file_path)
    return output

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)