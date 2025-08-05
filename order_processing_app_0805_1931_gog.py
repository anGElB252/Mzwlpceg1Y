# 代码生成时间: 2025-08-05 19:31:24
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from flask import Flask
import uuid

# 设置 Flask 服务器
server = Flask(__name__)

# 订单处理应用
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True

# 应用布局
app.layout = html.Div([
    html.H1("订单处理流程"),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
               'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
               'textAlign': 'center', 'margin': '10px'},
        # 允许上传csv文件
        accept=".csv"),
    html.Div(id='output-data-upload')
])

# 用于存储上传文件的UUID
uploaded_file_id = None

# 读取上传的CSV文件并更新表格
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(entered_text, filename):
    if entered_text is None or filename is None:
        # 如果没有文件上传，则不更新任何内容
        raise PreventUpdate()
    else:
        global uploaded_file_id
        # 生成文件的唯一ID
        uploaded_file_id = str(uuid.uuid4())
        
        # 读取上传的CSV文件内容
        df = pd.read_csv(
            io.StringIO(entered_text.decode('utf-8'))
        )
        # 将DataFrame转换为HTML表格
        return html.Table([
            html.Thead([
                html.Tr([html.Th(col) for col in df.columns])
            ]),
            html.Tbody([
                html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
                for i in range(len(df))
            ])
        ])

# 添加错误处理和文档
if __name__ == '__main__':
    app.run_server(debug=True)
