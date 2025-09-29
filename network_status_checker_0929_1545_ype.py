# 代码生成时间: 2025-09-29 15:45:12
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
from urllib.parse import urlparse
import pandas as pd

# 定义全局变量，用于存储网络检测结果
NETWORK_STATUS = {}

# 函数：检查URL是否可达
def is_url_accessible(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException as e:
        print(f"Error checking URL {url}: {e}")
        return False

# 函数：解析URL并检查其网络连接状态
def check_network_status(url):
    try:
        parsed_url = urlparse(url)
        if is_url_accessible(url):
            return {
                'status': 'Accessible',
                'hostname': parsed_url.hostname,
                'port': parsed_url.port
            }
        else:
            return {
                'status': 'Not Accessible',
                'hostname': parsed_url.hostname,
                'port': parsed_url.port
            }
    except ValueError:
        return {'status': 'Invalid URL', 'error': 'Invalid URL provided'}

# Dash应用布局
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Network Connection Status Checker'),
    dcc.Input(id='url-input', type='text', placeholder='Enter URL here...', debounce=True),
    html.Button('Check Status', id='check-button', n_clicks=0),
    dcc.Markdown(id='status-output'),
])

# 回调函数：检查网络状态并更新输出
@app.callback(
    Output('status-output', 'children'),
    [Input('check-button', 'n_clicks'),
     Input('url-input', 'value')
    ],
    prevent_initial_call=True
)
def update_output(n_clicks, url):
    if n_clicks > 0 and url:
        status_info = check_network_status(url)
        if status_info['status'] == 'Accessible':
            return f'The URL {url} is accessible.'
        elif status_info['status'] == 'Not Accessible':
            return f'The URL {url} is not accessible.'
        else:
            return status_info['error']
    return 'Provide a URL and click the button to check its status.'

if __name__ == '__main__':
    app.run_server(debug=True)