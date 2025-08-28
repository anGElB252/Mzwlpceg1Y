# 代码生成时间: 2025-08-29 06:19:42
# error_log_collector.py
"""
Error Log Collector using Dash framework

This application is designed to collect and display error logs.
It provides a simple dashboard for viewing and managing error logs.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import os
from datetime import datetime
import logging

# Initialize logging
logging.basicConfig(filename='error_log_collector.log', level=logging.ERROR)
logger = logging.getLogger(__name__)

# Define the application layout
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Error Log Collector"),
    dcc.Textarea(
        id='error-log',
        placeholder='Error logs will be displayed here...',
        readOnly=True,
        rows=20
    ),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
               'borderWidth': '1px', 'borderStyle': 'dashed',
               'borderRadius': '5px', 'textAlign': 'center',
               'margin': '10px'}
    ),
    html.Button('Clear Logs', id='clear-logs', n_clicks=0)
])

# Callback to update the error log display
@app.callback(
    dash.dependencies.Output('error-log', 'value'),
    [dash.dependencies.Input('upload-data', 'contents')]
)
def update_log(contents):
    if contents is not None:
        content_type = contents[0]['content_type']
        if content_type == "text/plain":
            # Get the content of the file
            value = contents[0]['data'].decode('utf-8')
            return value
        else:
            return "Please upload a text file"
    else:
        return "No file uploaded"

# Callback to clear the logs
@app.callback(
    dash.dependencies.Output('error-log', 'value'),
    [dash.dependencies.Input('clear-logs', 'n_clicks')]
)
def clear_logs(n_clicks):
    if n_clicks > 0:
        # Clear the log file
        open('error_log_collector.log', 'w').close()
        logger.info(f'Logs cleared by user {os.getlogin()} at {datetime.now()}')
        return ""
    return dash.no_update

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
