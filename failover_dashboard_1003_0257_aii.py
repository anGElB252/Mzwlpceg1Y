# 代码生成时间: 2025-10-03 02:57:26
# failover_dashboard.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import requests
from urllib.parse import urljoin
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)

# 定义失败重试的装饰器
def retry_on_error(exception_classes=(Exception,), max_retries=3, delay=1):
    def decorator(f):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return f(*args, **kwargs)
                except exception_classes as e:
                    attempts += 1
                    logging.error(f"Attempt {attempts} failed with error: {str(e)}")
                    if attempts == max_retries:
                        return f"Max retries reached. Last error: {str(e)}"
                    logging.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
            return f
        return wrapper
    return decorator

# 创建Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 应用布局
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Failover Dashboard"), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Input(id='primary-url', type='text', placeholder='Enter Primary URL'), width=6),
        dbc.Col(dcc.Input(id='secondary-url', type='text', placeholder='Enter Secondary URL'), width=6)
    ]),
    dbc.Row([
        dbc.Col(html.Button("Test Failover", id='test-button', color='primary'), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='output'), width=12)
    ])
])

# 定义回调函数，测试故障转移机制
@app.callback(
    Output('output', 'children'),
    [Input('test-button', 'n_clicks')],
    [State('primary-url', 'value'), State('secondary-url', 'value')]
)
@retry_on_error(exception_classes=(requests.exceptions.RequestException,), max_retries=3, delay=2)
def test_failover(n_clicks, primary_url, secondary_url):
    """
    测试故障转移机制。
    
    如果主URL失败，尝试次URL。
    """
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate("Button has not been clicked.")
    try:
        # 尝试访问主URL
        response = requests.get(primary_url, timeout=5)
        response.raise_for_status()
        return f"Primary URL responded with {response.status_code}."
    except requests.exceptions.RequestException as e:
        # 捕获主URL请求异常，尝试次URL
        logging.error(f"Primary URL failed: {str(e)}")
        try:
            response = requests.get(secondary_url, timeout=5)
            response.raise_for_status()
            return f"Secondary URL responded with {response.status_code}."
        except requests.exceptions.RequestException as e:
            logging.error(f"Secondary URL failed: {str(e)}")
            return f"Both primary and secondary URLs failed. Last error: {str(e)}"

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)