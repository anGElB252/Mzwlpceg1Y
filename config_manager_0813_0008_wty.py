# 代码生成时间: 2025-08-13 00:08:39
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
from dash.dependencies import Input, Output
import json
from dotenv import load_dotenv
import logging

# 配置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 环境变量文件
ENV_FILE = '.env'

class ConfigManager:
    def __init__(self):
        # 加载环境变量文件
        load_dotenv(dotenv_path=ENV_FILE)
        # 初始化Dash应用
        self.app = dash.Dash(__name__)
        self.app.layout = self.create_layout()
        self.app.config.suppress_callback_exceptions = True
        
    def create_layout(self):
        # 创建Dash应用布局
        return html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
                        'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                        'textAlign': 'center', 'margin': '10px'}
            ),
            html.Button('Save Configuration', id='save-config', n_clicks=0),
            html.Div(id='output-container')
        ])
    
    def update_config_file(self, uploaded_filename, file_content):
        # 更新配置文件内容
        try:
            with open(uploaded_filename, 'w') as file:
                json.dump(file_content, file, indent=4)
            return True
        except Exception as e:
            logger.error(f'Failed to update config file: {e}')
            return False
    
    @staticmethod
    def parse_config_file(uploaded_filename):
        # 解析配置文件内容
        try:
            with open(uploaded_filename, 'r') as file:
                return json.load(file)
        except Exception as e:
            logger.error(f'Failed to parse config file: {e}')
            return {}
    
    @staticmethod
    def download_config_file(filename, content):
        # 生成配置文件下载链接
        return dcc.Download(
            dcc.SendData(content, f'{filename}.json'),
            f'Download {filename}'
        )

    def register_callbacks(self):
        # 注册Dash回调函数
        @self.app.callback(
            Output('output-container', 'children'),
            [Input('upload-data', 'contents'), Input('upload-data', 'filename')],
            [State('save-config', 'n_clicks')])
        def parse_contents(contents, filename, n_clicks):
            if contents is not None and filename is not None:
                content_type, content_string = contents.split(',')
                if content_type == 'application/json':
                    try:
                        content = json.loads(content_string)
                        return self.download_config_file(filename, json.dumps(content, indent=4))
                    except Exception as e:
                        logger.error(f'Failed to parse JSON: {e}')
                        return 'Failed to parse JSON'
                else:
                    return 'Only JSON files are supported'
            elif n_clicks > 0:
                # 保存配置文件
                return html.Div([
                    html.Button('Upload File', id='upload-button', n_clicks=0),
                    html.Div(id='output-data-upload')
                ])
            return ''
    
    def run_server(self):
        # 运行Dash服务器
        self.register_callbacks()
        self.app.run_server(debug=True)

if __name__ == '__main__':
    # 创建配置管理器实例并运行服务器
    config_manager = ConfigManager()
    config_manager.run_server()