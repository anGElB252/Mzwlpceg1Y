# 代码生成时间: 2025-09-06 00:39:18
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from urllib.parse import quote
import time

# 定义全局变量
URL = 'http://example.com/'
REPETITIONS = 10
SLEEP_BETWEEN_REQUESTS = 2

# 创建Dash应用
app = dash.Dash(__name__)

# 创建应用布局
app.layout = html.Div(children=[
    html.H1("Performance Test Dashboard"),
    dcc.Input(id='url-input', type='text', placeholder='Enter URL', value=URL),
    html.Button("Start Test", id='start-test-button', n_clicks=0),
    dcc.Loading(id='test-loading', type='default'),
    html.Div(id='test-output')
])

# 定义性能测试函数
def performance_test(url):
    """
    对给定URL执行性能测试
    :param url: 要测试的URL
    :return: 包含测试结果的Pandas DataFrame
    """
    # 初始化结果列表
    results = []
    
    # 进行REPETITIONS次请求
    for _ in range(REPETITIONS):
        try:
            # 记录请求开始时间
            start_time = time.time()
            
            # 发起请求
            response = requests.get(url)
            
            # 记录请求结束时间
            end_time = time.time()
            
            # 计算请求耗时
            latency = end_time - start_time
            
            # 将结果添加到列表
            results.append({'url': url, 'status_code': response.status_code, 'latency': latency})
            
            # 等待SLEEP_BETWEEN_REQUESTS秒
            time.sleep(SLEEP_BETWEEN_REQUESTS)
        except Exception as e:
            # 如果请求失败，记录错误信息
            results.append({'url': url, 'status_code': None, 'latency': None, 'error': str(e)})
    
    # 将结果转换为DataFrame
    return pd.DataFrame(results)

# 定义回调函数
@app.callback(
    Output('test-output', 'children'),
    Output('test-loading', 'children'),
    Input('start-test-button', 'n_clicks'),
    State('url-input', 'value')
)
def run_test(n_clicks, url):
    if n_clicks > 0:
        # 开始性能测试
        df = performance_test(url)
        
        # 创建图表
        chart = px.line(df, x='url', y='latency', title='Request Latency Over Time')
        
        # 更新UI
        return [dcc.Graph(figure=chart), None]
    else:
        # 如果没有点击按钮，显示空内容
        return [html.Div(), dcc.Loading(id='test-loading', type='default')]

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)