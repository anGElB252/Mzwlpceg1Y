# 代码生成时间: 2025-08-15 11:01:01
import os
from PIL import Image
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# 定义一个函数来调整图片尺寸
def resize_image(image_path, output_size):
    try:
        # 打开图片
        with Image.open(image_path) as img:
            # 调整尺寸
            img_resized = img.resize(output_size)
            # 保存调整后的图片
            img_resized.save(image_path)
            return True
    except IOError:
        print(f"Error: Could not open image file {image_path}")
        return False

# 设置Dash应用程序
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义布局
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Batch Image Resizer"), width=12),
    ]),
    dbc.Row([
        dbc.Col(dcc.Upload(
            id='upload-data',
            children=html.Div([html.Button('Upload', id='upload-button', n_clicks=0)]),
            multiple=True,
        ), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Input(id='resize-size', type='number', placeholder='Enter size (e.g., 300)'), width=4),
        dbc.Col(dcc.Button('Resize', id='resize-button', n_clicks=0), width=2),
    ]),
    dbc.Row([
        dbc.Col(dcc.Download(id='download-link'), width=12),
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='output-container'), width=12),
    ]),
])

# 回调函数处理图片上传和尺寸调整
@app.callback(
    Output('output-container', 'children'),
    Input('upload-button', 'n_clicks'),
    Input('resize-button', 'n_clicks'),
    prevent_initial_call=True,
)
def upload_resize(n_clicks_upload, n_clicks_resize):
    # 检查按钮是否被点击
    if n_clicks_upload and n_clicks_resize:
        # 获取上传的文件
        uploaded_files = dash.callback_context.inputs['upload-data']
        if uploaded_files is not None:
            file_list = uploaded_files.split(', ')
            size = dash.callback_context.inputs['resize-size']
            # 调整所有上传图片的尺寸
            for file in file_list:
                image_path = os.path.join('temp', file.split('name=')[-1])
                if resize_image(image_path, (int(size), int(size))):
                    print(f"Resized {file} successfully")
                else:
                    print(f"Failed to resize {file}")
            return 'All images have been resized successfully'
        else:
            return 'No files uploaded'
    else:
        return ''

# 启动服务器
if __name__ == '__main__':
    app.run_server(debug=True)