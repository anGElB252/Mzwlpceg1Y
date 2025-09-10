# 代码生成时间: 2025-09-10 20:54:26
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
from PIL import Image
from io import BytesIO
from dash.dependencies import Input, Output
import base64

# 定义图片尺寸批量调整器的类
class ImageResizer:
    def __init__(self, output_dir='resized_images'):
        # 初始化输出目录
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def resize_image(self, image_path, new_size):
        """
        调整单个图片尺寸
        :param image_path: 原始图片路径
        :param new_size: 目标尺寸 (宽度, 高度)
        :return: None
        """
        try:
            with Image.open(image_path) as img:
                img = img.resize(new_size)
                output_path = os.path.join(self.output_dir, os.path.basename(image_path))
                img.save(output_path)
        except IOError:
            print(f"Error resizing image {image_path}")

    def batch_resize_images(self, image_folder, new_size):
        """
        批量调整文件夹中所有图片的尺寸
        :param image_folder: 包含图片的文件夹路径
        :param new_size: 目标尺寸 (宽度, 高度)
        :return: None
        """
        for filename in os.listdir(image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                self.resize_image(os.path.join(image_folder, filename), new_size)

# 创建Dash应用程序
app = dash.Dash(__name__)

# 添加上传组件和输出组件
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # 允许多文件上传
        multiple=True
    ),
    html.Div(id='output-data-upload')
])

# 回调函数，处理文件上传和图片尺寸调整
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')])
def update_output(contents):
    if contents is not None:
        # 将上传的文件内容转换为列表
        contents = contents.split(',')
        resizer = ImageResizer()
        for content in contents:
            # 解析文件名和二进制数据
            _, b64 = content.split(',')
            data = base64.b64decode(b64)
            # 保存图片并调整尺寸
            image = Image.open(BytesIO(data))
            output_path = 'resized_image.png'
            image.save(output_path)
            resizer.resize_image(output_path, (100, 100))
            os.remove(output_path)
        return 'All images have been resized successfully'
    else:
        return 'No files uploaded'

if __name__ == '__main__':
    app.run_server(debug=True)