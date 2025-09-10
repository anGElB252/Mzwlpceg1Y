# 代码生成时间: 2025-09-10 15:57:54
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
# NOTE: 重要实现细节
import pandas as pd
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import base64
import io
import re
# 增强安全性
import os

"""
Text File Analyzer using Dash framework.
This application allows users to upload a text file and visualize the content analysis results.
"""

# Define the app layout
def app_layout():
    app = dash.Dash(__name__)
    app.layout = html.Div(children=[
        html.H1(children='Text File Analyzer'),
        html.Div(children=''Upload a text file: ''),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
# 添加错误处理
                html.A('Select a file')
            ]),
            style={'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'},
            # Allow multiple files to be uploaded
            multiple=False
        ),
        html.Div(id='output-data-upload'),
        html.Div(
            children=''Word Cloud: '',
            style={'margin-top': '20px', 'margin-bottom': '10px'}
        ),
        dcc.Graph(id='word-cloud-graph'),
# 扩展功能模块
        html.Div(
# 添加错误处理
            children=''Word Frequency: '',
            style={'margin-top': '20px', 'margin-bottom': '10px'}
# 添加错误处理
        ),
        dcc.Graph(id='word-freq-graph'),
    ])
# NOTE: 重要实现细节
    return app

# Define the callback function to update output when a file is uploaded
@app.callback(
    Output('output-data-upload', 'children'),
# 添加错误处理
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(contents, filename):
# 改进用户体验
    if contents is not None:
        # Read the contents of the file
# FIXME: 处理边界情况
        children = []
# 改进用户体验
        decoded = base64.b64decode(contents.split(',')[1]).decode('utf-8')
# NOTE: 重要实现细节
        children.append(html.H5(filename))
        children.append(html.P(datetime.datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%Y-%m-%d %H:%M:%S')))
        return children
    else:
        return html.Div()

# Define the callback function to generate word cloud and word frequency graph
@app.callback(
    Output('word-cloud-graph', 'figure'),
    Output('word-freq-graph', 'figure'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def generate_graphs(contents, filename):
    if contents is not None:
# TODO: 优化性能
        # Read the contents of the file
        decoded = base64.b64decode(contents.split(',')[1]).decode('utf-8')
        text = decoded.split('
')
        # Clean and split the text into words
# 改进用户体验
        words = ' '.join(text).lower().split()
        # Remove punctuation and numbers
# FIXME: 处理边界情况
        words = [re.sub(r'[^a-z]', '', word) for word in words]
        # Count the frequency of each word
        word_freq = pd.Series(words).value_counts()
        # Generate word cloud
        wordcloud = WordCloud(width=800, height=600, background_color='white').generate(' '.join(words))
        fig_wordcloud = px.imshow(wordcloud, aspect='auto')
        fig_wordcloud.update_layout(title='Word Cloud', xaxis_title='', yaxis_title='')
# 扩展功能模块
        # Generate word frequency bar chart
        fig_wordfreq = px.bar(word_freq, x=word_freq.index, y=word_freq.values)
        fig_wordfreq.update_layout(title='Word Frequency', xaxis_title='Words', yaxis_title='Frequency')
        return fig_wordcloud, fig_wordfreq
    else:
        return go.Figure(), go.Figure()
# 增强安全性

# Run the app
if __name__ == '__main__':
    app = app_layout()
    app.run_server(debug=True)