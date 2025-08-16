# 代码生成时间: 2025-08-16 09:23:31
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from collections import Counter
import base64
import io

# 定义一个函数，用于从文本文件中读取内容并生成报告
def generate_report(df):
    # 计算词频统计
    word_counts = Counter(df['text'])
    # 绘制高频词图
    top_words = word_counts.most_common(20)
    fig = px.bar(x=[word for word, _ in top_words], y=[count for _, count in top_words], 
                 labels={'x': 'Words', 'y': 'Counts'}, title='Top 20 Words')
    return fig

# 创建Dash应用
app = dash.Dash(__name__)

# 定义应用的布局
app.layout = html.Div(
    [
        dcc.Upload(
            id='upload-data',
            children=html.Button('Upload Text File'),
            style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 
                   'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 
                   'textAlign': 'center', 'margin': '10px'},
            # 允许上传的文件类型
            accept='.txt, .csv'
        ),
        html.Div(id='file-upload-output'),
        dcc.Graph(id='high-frequency-words-graph')
    ]
)

# 定义回调函数，处理文件上传和内容分析
@app.callback(
    Output('high-frequency-words-graph', 'figure'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
)
def update_output(contents, filename, last_modified):
    if contents is None:
        raise PreventUpdate

    # 读取文本文件内容
    try:
        _, content_string = contents.split(',')
        content = base64.b64decode(content_string).decode('utf-8')
    except Exception as e:
        print(e)
        return {}

    # 将文本内容分割成单词列表
    words = content.split()
    df = pd.DataFrame(words, columns=['text'])

    # 生成报告
    fig = generate_report(df)
    return fig

# 定义回调函数，显示上传的文件信息
@app.callback(
    Output('file-upload-output', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')]
)
def display_output(contents, filename, last_modified):
    if contents is None:
        raise PreventUpdate

    return f'File {filename} uploaded successfully!'

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)
