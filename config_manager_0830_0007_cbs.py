# 代码生成时间: 2025-08-30 00:07:50
import dash
from dash import html, dcc, Input, Output
from dash.exceptions import PreventUpdate
import json
import os

# Define the layout of the Dash application
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Configuration Manager'),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload Configuration'),
        max_size=None,  # No size limit
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center'},
    ),
    html.Div(id='config-output'),
    html.Button('Save Configuration', id='save-config', n_clicks=0),
    dcc.Input(id='config-name', type='text', placeholder='Enter configuration name'),
    html.Div(id='saved-configs'),
])

# State to store the current configuration
app.config = {'current_config': None}

# Callback to display the uploaded configuration
@app.callback(
    Output('config-output', 'children'),
    [Input('upload-data', 'contents')],
)
def update_output(contents):
    if contents is None:
        raise PreventUpdate
    try:
        # Convert the contents of the file to a string
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string).decode('utf-8')
        # Parse the JSON content
        config_data = json.loads(decoded)
        return json.dumps(config_data, indent=2)
    except Exception as e:
        return str(e)

# Callback to save the current configuration to a file
@app.callback(
    Output('saved-configs', 'children'),
    [Input('save-config', 'n_clicks')],
    [State('config-name', 'value'),
     State('config-output', 'children')],
)
def save_config(n_clicks, config_name, config_data):
    if n_clicks == 0:
        raise PreventUpdate
    if config_name is None or config_data is None:
        return 'Please enter a configuration name and upload a configuration file.'
    try:
        # Ensure the configuration directory exists
        config_directory = 'configs'
        os.makedirs(config_directory, exist_ok=True)
        # Write the configuration data to a file
        with open(os.path.join(config_directory, f'{config_name}.json'), 'w') as file:
            json.dump(json.loads(config_data), file, indent=4)
        return html.P(f'Configuration saved as {config_name}.json')
    except Exception as e:
        return str(e)

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)