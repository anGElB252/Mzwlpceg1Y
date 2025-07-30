# 代码生成时间: 2025-07-30 17:08:57
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from pathlib import Path
import logging
import re

# 设置日志记录
logging.basicConfig(level=logging.INFO)


def parse_log_file(log_file_path, pattern):
    """解析日志文件并返回解析后的数据。"""
    try:
        # 读取日志文件
        with open(log_file_path, 'r') as file:
            log_data = file.readlines()
            # 使用正则表达式匹配日志行
            parsed_data = [re.match(pattern, line) for line in log_data if re.match(pattern, line)]
            # 将匹配结果转换为DataFrame
            df = pd.DataFrame([m.groupdict() for m in parsed_data], columns=['timestamp', 'level', 'message'])
            # 返回解析后的DataFrame
            return df
    except FileNotFoundError:
        logging.error(f'文件 {log_file_path} 未找到。')
        raise
    except Exception as e:
        logging.error(f'解析日志文件时发生错误：{e}')
        raise

# 创建Dash应用
app = dash.Dash(__name__)

# 定义应用布局
app.layout = html.Div([
    html.H1('日志文件解析工具'),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['点击上传日志文件']),
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
               'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
               'textAlign': 'center', 'margin': '10px'},
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(id='log-graph'),
])

# 回调函数：处理文件上传
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(contents, filename):
    if contents is not None:
        # 解析文件内容
        try:
            log_data = parse_log_file(contents.decode('utf-8'), r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),(\w+),(.*)$')
            # 显示文件名和文件大小
            return html.Div([
                html.H5(f'文件已上传：{filename}'),
                html.P(f'大小：{len(contents)} 字节')
            ])
        except Exception as e:
            return html.Div([
                html.H5('发生错误：'),
                html.P(str(e))
            ])

# 回调函数：绘制日志图表
@app.callback(
    Output('log-graph', 'figure'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_graph(contents, filename):
    if contents is not None:
        # 解析文件内容
        try:
            log_data = parse_log_file(contents.decode('utf-8'), r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),(\w+),(.*)$')
            # 绘制图表
            fig = px.line(log_data, x='timestamp', y='level')
            fig.update_layout(title='日志级别趋势图')
            return fig
        except Exception as e:
            return {'data': [], 'layout': {'annotations': [{'text': f'发生错误：{e}', 'x': 0.5, 'y': 0.5, 'xref': 'paper', 'yref': 'paper', 'showarrow': False}]}}

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)