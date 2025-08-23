# 代码生成时间: 2025-08-23 10:58:45
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import zipfile
import os
import base64
import io
from werkzeug.utils import secure_filename

# 定义应用
app = dash.Dash(prevent_initial_callbacks=True)

# 应用布局
app.layout = html.Div(children=[
    html.H1(children='压缩文件解压工具'),
    dcc.Upload(id='upload-data', children=html.Button('上传文件'),
               multiple=True),
    html.Div(id='output-container')
])

# 回调函数处理上传文件
@app.callback(
    Output('output-container', 'children'),
    [Input('upload-data', 'contents')]
)
def upload_file(list_of_contents):  # 这里假设上传的是压缩文件列表
    if list_of_contents is not None:  # 检查是否上传了文件
        children = []
        for content in list_of_contents:  # 遍历文件列表
            filename = secure_filename(content.filename)  # 确保文件名是安全的
            # 读取文件内容
            if 'zip' in filename:  # 检查文件是否是zip格式
                try:  # 捕获解压过程中的错误
                    with zipfile.ZipFile(io.BytesIO(content), 'r') as f:  # 使用BytesIO打开文件
                        f.extractall('extracted/')  # 解压到extracted文件夹
                        children.append(html.Div(
                            f'文件 {filename} 解压成功，文件已保存至 extracted/ 文件夹。'))  # 添加解压成功的信息
                except Exception as e:  # 处理解压过程中的异常
                    children.append(html.Div(f'文件 {filename} 解压失败: {e}'))  # 添加解压失败的信息
            else:  # 处理非zip格式的文件
                children.append(html.Div(f'文件 {filename} 不是zip格式，跳过解压。'))  # 添加非zip格式文件跳过的信息
        return children
    else:  # 如果没有上传文件，返回空字符串
        return ''

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)