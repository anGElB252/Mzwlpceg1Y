# 代码生成时间: 2025-08-02 06:39:18
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from urllib.parse import quote
import base64
import io

# 定义Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div([
    html.H1('Excel表格自动生成器'),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['将Excel文件拖拽到这里或点击上传']),
        style={'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'},
        # 允许上传多个文件
        multiple=False
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(id='excel-plot'),
])

# 回调函数处理文件上传
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(contents, filename):
    if contents is None:
        raise PreventUpdate
    
    # 读取Excel文件内容
    try:
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(contents)
            # 显示表格预览
            return html.Div([
                html.H4(f'文件 {filename} 已上传'),
                html.Table([
                    html.Tr([html.Th(col) for col in df.columns]) for col in df.columns] +
                    [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(min(len(df), 10))]
                )
            ])
        else:
            return '请上传Excel文件 (.xlsx 或 .xls)'
    except Exception as e:
        return f'文件读取错误: {str(e)}'

# 回调函数生成图表
@app.callback(
    Output('excel-plot', 'figure'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_graph(contents, filename):
    if contents is None:
        raise PreventUpdate
    
    try:
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(contents)
            # 选择第一个sheet作为示例
            fig = px.line(df)
            return fig
        else:
            return {}
    except Exception as e:
        return {}

# 启动应用
if __name__ == '__main__':
    app.run_server(debug=True)