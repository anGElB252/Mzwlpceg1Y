# 代码生成时间: 2025-08-19 19:21:43
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from io import StringIO
import re

# TextFileAnalyzer class to encapsulate the Dash application
class TextFileAnalyzer:
    def __init__(self):
        # Initialize the Dash application
        self.app = dash.Dash(__name__)

        # Define the layout of the Dash app
        self.app.layout = html.Div(children=[
            html.H1(children='Text File Content Analyzer'),
            dcc.Upload(
                id='upload-data',
                children=html.Button('Upload Text File'),
                style={'width': '100%', 'height': '60px', 'lineHeight': '60px'},
                multiple=False
            ),
            html.Div(id='output-data-upload'),
            dcc.Graph(id='word-cloud-graph'),
            html.Div(id='word-count-table')
        ])

        # Define callback functions
        self.app.callback(
            Output('output-data-upload', 'children'),
            [Input('upload-data', 'contents')]
        )(self.display_upload)

        self.app.callback(
            Output('word-cloud-graph', 'figure'),
            [Input('upload-data', 'contents')]
        )(self.update_graph)

        self.app.callback(
            Output('word-count-table', 'children'),
            [Input('upload-data', 'contents')]
        )(self.update_table)

    def display_upload(self, contents):
        # Handle file upload and display the content or error message
        if contents is None:
            return 'Please upload a text file.'
        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string).decode('utf-8')
            return dcc.Markdown('### Text File Content:')
        except Exception as e:
            return f'Error: {str(e)}'

    def update_graph(self, contents):
        # Generate a word cloud graph based on the uploaded text file
        if contents is None:
            return {}
        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string).decode('utf-8')
            df = pd.DataFrame({"word": decoded.split()}).fillna(0)
            df['count'] = df['word'].map(df['word'].value_counts())
            fig = px.bar(df, x='word', y='count', title='Word Cloud')
            return fig
        except Exception as e:
            print(f'Error: {str(e)}')
            return {}

    def update_table(self, contents):
        # Display a word count table based on the uploaded text file
        if contents is None:
            return ''
        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string).decode('utf-8')
            df = pd.DataFrame({"word": decoded.split()}).fillna(0)
            df['count'] = df['word'].map(df['word'].value_counts())
            table = html.Table([
                html.Tr([html.Th(col) for col in df.columns]),
                html.Tr([html.Td(df[col].iloc[0]) for col in df.columns])
            ])
            return table
        except Exception as e:
            print(f'Error: {str(e)}')
            return ''

    # Run the Dash application
    def run(self):
        self.app.run_server(debug=True)

if __name__ == '__main__':
    analyzer = TextFileAnalyzer()
    analyzer.run()