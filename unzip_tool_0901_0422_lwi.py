# 代码生成时间: 2025-09-01 04:22:01
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import zipfile
import os
from werkzeug.utils import secure_filename
import base64
import io
import requests
from io import BytesIO
from flask import send_file

# 定义应用
app = dash.Dash(__name__)
server = app.server

# 创建应用布局
app.layout = html.Div([
    html.H1('Compress File Unzip Tool', style={'textAlign': 'center'}),
    html.Div(dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                'textAlign': 'center', 'margin': '10px'},
        multiple=True
    ), style={'width': '100%', 'height': '60px', 'textAlign': 'center', 'margin': '10px'}),
    html.Button('Unzip', id='unzip-button', n_clicks=0),
    dcc.Download(id='download-button'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    ),
    html.Div(id='output-container')
])

# 回调函数：处理上传的文件
@app.callback(Output('output-container', 'children'),
              [Input('upload-data', 'contents'),
               Input('interval-component', 'n_intervals')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(contents, n, filenames, last_modifieds):
    # 检查是否有文件上传
    if contents is not None:
        # 保存文件到临时目录
        uploaded_filename = secure_filename(filenames[0])
        uploaded_file = BytesIO(contents[0])
        with open(uploaded_filename, 'wb') as f:
            f.write(uploaded_file.read())

        # 解压文件
        try:
            zip_ref = zipfile.ZipFile(uploaded_filename, 'r')
            zip_ref.extractall('extracted_files')
            zip_ref.close()
            return html.Div([html.H5('Files have been successfully unzipped!')])
        except zipfile.BadZipFile:
            return html.Div([html.H5('Error: Invalid zip file.')])
        finally:
            # 删除临时文件
            os.remove(uploaded_filename)
    return html.Div([html.H5('No files uploaded.')])

# 回调函数：下载解压后的文件
@app.callback(Output('download-button', 'data'),
              [Input('unzip-button', 'n_clicks')],
              [State('output-container', 'children')])
def download_files(n_clicks, children):
    # 检查是否有文件解压
    if n_clicks > 0 and children:
        # 将解压后的文件打包为zip文件
        zip_filename = 'extracted_files.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, dirs, files in os.walk('extracted_files'):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join('extracted_files', '')))

        # 发送文件下载
        return send_file(zip_filename, as_attachment=True)
    return None

if __name__ == '__main__':
    app.run_server(debug=True)