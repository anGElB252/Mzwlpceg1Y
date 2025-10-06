# 代码生成时间: 2025-10-07 02:56:26
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd
from urllib.parse import quote_plus

### Metadata Management System using DASH framework
class MetadataManagementSystem:
    def __init__(self):
        # Initialize the DASH app
        self.app = dash.Dash(__name__)
        # Define the layout of the app
        self.layout()

    def layout(self):
        # Define the layout of the DASH app
        self.app.layout = html.Div([
            html.H1("Metadata Management System"),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                multiple=True,
                accept=".csv/*"
            ),
            html.Div(id='output-data-upload'),
            dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
            ),
            dash_table.DataTable(
                id='metadata-table',
                columns=[],
                data=[],
                page_size=10,
                editable=True
            )
        ])

    def callback_upload_data(self, contents, filename):
        # Parse contents of the uploaded file
        try:
            df = pd.read_csv(
                contents,
                encoding='utf-8'
            )
        except Exception as e:
            return {"type": "custom", "style": {"color": "red"}, "content": f'Error loading file {filename}. {str(e)}'}

        # Return the dataframe as a DASH DataTable
        return dash_table.DataTable(
            id='metadata-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records")
        )

    def update_table(self, n):
        # Update the table based on the uploaded data
        if 'upload-data' not in self.app.callback_map:
            return dash_table.DataTable(
                id='metadata-table',
                columns=[],
                data=[],
                page_size=10,
                editable=True
            )

        # Get the uploaded contents and filename
        upload_contents = self.app.callback_map['upload-data'].triggered[0]['prop_id'].split('.')[1]
        upload_filename = self.app.callback_map['upload-data'].triggered[0]['value']

        # Return the table based on the uploaded file
        return self.callback_upload_data(upload_contents, upload_filename)

    # Define the callbacks for the DASH app
    self.app.callback(Output('metadata-table', 'data'),
                    Input('upload-data', 'contents'),
                    Input('upload-data', 'filename'))(self.callback_upload_data)

    self.app.callback(Output('metadata-table', 'columns'),
                    Input('upload-data', 'contents'),
                    Input('upload-data', 'filename'))(self.callback_upload_data)

    self.app.callback(Output('output-data-upload', 'children'),
                    Input('interval-component', 'n'))(self.update_table)

# Run the DASH server if this script is executed
if __name__ == '__main__':
    MetadataManagementSystem().app.run_server(debug=True)