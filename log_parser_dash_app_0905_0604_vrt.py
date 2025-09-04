# 代码生成时间: 2025-09-05 06:04:48
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import re
import os
from datetime import datetime

# Define the layout of the Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Log File Parser Tool'),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ',
                        html.A('Select File')]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(id='parsed-log-graph'),
    dcc.Table(id='parsed-log-table')
])

# Function to parse the log file and store it as a Pandas DataFrame
def parse_log_file(log_file):
    try:
        # Assuming the log file has a timestamp in the format: YYYY-MM-DD HH:MM:SS
        # and a log level (INFO, DEBUG, ERROR, etc.)
        df = pd.read_csv(log_file, names=['timestamp', 'log_level', 'message'],
                         sep=' ', engine='python')
        # Convert the timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        # Handle exceptions and return an error message
        return f'Error parsing log file: {e}'

# Callback to display the contents of the uploaded log file
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(contents, filename):
    if contents is not None:
        # Save the uploaded file to a temporary directory
        filename = filename.split('.')[0] + '.log'
        with open(filename, 'wb') as f:
            f.write(contents)
        return f'File {filename} uploaded successfully.'
    return 'No file uploaded.'

# Callback to parse the uploaded log file and display a graph and table
@app.callback(
    [Output('parsed-log-graph', 'figure'),
     Output('parsed-log-table', 'data')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def parse_log(contents, filename):
    if contents is not None:
        # Parse the log file
        df = parse_log_file(filename)
        if isinstance(df, str):
            # If an error occurred during parsing, display the error message
            return {'data': [{'x': [1], 'y': [1], 'type': 'bar', 'name': df}],
                    'layout': {'title': 'Error'}}, None
        else:
            # Group the data by log level and count the occurrences
            grouped = df['log_level'].value_counts().reset_index()
            grouped.columns = ['log_level', 'count']
            # Create a graph
            figure = {"data": [
                {"x": grouped['log_level'], "y": grouped['count'], "type": "bar", "name": "Count"}],
                "layout": {"title": "Log Level Distribution"}}
            # Create a table
            table = df.to_dict('records')
            return figure, table
    return None, None

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)