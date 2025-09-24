# 代码生成时间: 2025-09-24 16:22:28
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import no_update
import plotly.express as px

# 定义Excel表格自动生成器应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div([
    html.H1("Excel表格自动生成器"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([html.Button('选择文件', id='upload-button'), html.H6(id='file-name')]),
        accept='.xlsx',
    ),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='表格预览', value='tab-1'),
        dcc.Tab(label='图表', value='tab-2'),
    ]),
    html.Div(id='table-preview'),
    html.Div(id='chart'),
])

# 回调函数：处理文件上传和表格预览
@app.callback(
    Output('file-name', 'children'),
    Output('table-preview', 'children'),
    Input('upload-data', 'contents'),
    Input('tabs', 'value'),
    State('upload-data', 'filename'),
)
def process_uploaded_file(contents, tab, filename):
    if contents is None or filename is None:
        raise PreventUpdate
    # 读取Excel文件
    df = pd.read_excel(contents)
    if 'tab-1' in tab:
        # 返回表格预览组件
        return html.H6(filename), px.dataframe_table(df)
    else:
        # 返回空组件
        return no_update, no_update

# 回调函数：处理图表显示
@app.callback(
    Output('chart', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
)
def display_chart(contents, filename):
    if contents is None or filename is None:
        raise PreventUpdate
    # 读取Excel文件
    df = pd.read_excel(contents)
    # 选择一个默认图表（例如：折线图）
    chart = px.line(df, y=df.columns[0])
    return dcc.Graph(figure=chart)

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
