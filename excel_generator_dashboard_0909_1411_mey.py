# 代码生成时间: 2025-09-09 14:11:44
import dash
import dash_table
import pandas as pd
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import ALLSELECTIONS, ALLMULTISELECTION
import base64
import io
from datetime import datetime
from dash_extensions.javascript import Namespace, arrow

# Define the Dash application
app = dash.Dash(__name__)
app.title = 'Excel Table Generator'

# Load sample data for demonstration
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Define the layout of the app
app.layout = html.Div([
    html.H1('Excel Table Generator'),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload Excel File'),
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'},
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        column_selectable='single',
        row_selectable='multi',
        selected_rows=[],
        page_action='native',
        page_current=0,
        page_size=10,
    ),
    dcc.Download(id='download-button'),
])

# Callback to update output when a new file is uploaded
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
)
def update_output(contents, filename, last_modified):
    if contents is None:
        raise PreventUpdate
    # Parse the contents of the Excel file
    try:
        df = pd.read_excel(io.BytesIO(contents[0]))
    except Exception as e:
        return f'An error occurred while parsing the file: {e}'
    # Update the table with the new data
    return dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        column_selectable='single',
        row_selectable='multi',
        selected_rows=[],
        page_action='native',
        page_current=0,
        page_size=10,
    )

# Callback to download the current table as an Excel file
@app.callback(
    Output('download-button', 'data'),
    [Input('table', 'data')],
    [State('table', 'filename'), State('table', 'last_modified')]
)
def download_table(data, filename, last_modified):
    if data is None:
        raise PreventUpdate
    # Convert the table data to an Excel file
    try:
        out = io.BytesIO()
        df = pd.DataFrame(data)
        df.to_excel(out, index=False)
        out.seek(0)
        return send_data_frame(df, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', df.columns.tolist(), 'table.xlsx')
    except Exception as e:
        return f'An error occurred while generating the Excel file: {e}'

# Helper function to send a DataFrame as a file
def send_data_frame(df, as_attachment, filename, sheet_name):
    output = io.BytesIO()
    df.to_excel(output, sheet_name=sheet_name, index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, attachment_filename=filename)

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)
