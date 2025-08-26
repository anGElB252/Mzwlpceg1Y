# 代码生成时间: 2025-08-27 01:11:48
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from io import StringIO

# 全局变量，用于存储上传的文件
uploaded_file = ''

# 定义文档转换器应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div(children=[
    html.H1('文档格式转换器'),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['点击上传文件或拖拽文件到此处']),
        multiple=False,  # 禁止同时上传多个文件
    ),
    html.Div(id='output-data-upload'),
])

# 回调函数，上传文件后触发
@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
)
def update_output(contents, filename):
    global uploaded_file
    try:
        # 保存上传的文件内容
        uploaded_file = contents
        if uploaded_file is not None:
            # 显示文件上传成功并显示文件名
            return f'文件上传成功：{filename}'
        else:
            return '未上传文件'
    except Exception as e:
        # 错误处理
        return f'文件上传失败：{e}'

# 回调函数，用于转换文件格式
@app.callback(
    Output('output-data-upload', 'children'),
    Input('output-data-upload', 'n_clicks'),
    State('upload-data', 'contents'),
)
def convert_file(n_clicks, contents):
    if n_clicks is None or contents is None:
        return '尚未上传文件或点击转换按钮'
    try:
        # 读取文件内容
        file_content = StringIO(contents.split(',')[1])
        # 假设文件为CSV格式，转换为Excel格式
        df = pd.read_csv(file_content)
        # 将DataFrame保存为Excel文件
        xlsx_file = 'converted_file.xlsx'
        df.to_excel(xlsx_file, index=False)
        # 显示转换成功的消息
        return f'文件已转换为Excel格式：{xlsx_file}'
    except Exception as e:
        # 错误处理
        return f'文件转换失败：{e}'

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)