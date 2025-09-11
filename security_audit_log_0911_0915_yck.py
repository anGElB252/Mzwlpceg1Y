# 代码生成时间: 2025-09-11 09:15:52
import os
import logging
from flask import Flask, request, jsonify
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

# 设置日志配置
logging.basicConfig(
    filename="security_audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_request(req):
    """记录请求信息到安全审计日志"""
    logging.info(f"Request: {req.remote_addr} - {req.method} {req.full_path} {req.user_agent}")

def log_response(res):
    """记录响应信息到安全审计日志"""
    logging.info(f"Response: {res.status} {res.status_message}")

# 初始化 Flask 应用
app = Flask(__name__)

# 定义 Dash 应用
server = app.server
app = dash.Dash(__name__, server=server)

# 定义 Dash 布局
app.layout = html.Div([
    html.H1("Security Audit Log Dashboard"),
    dcc.Graph(id='audit-log-graph'),
    dcc.Table(id='audit-log-table')
])

# 定义回调函数，生成图表
@app.callback(
    Output('audit-log-graph', 'figure'),
    [Input('audit-log-table', 'data')]
)
def update_graph(data):
    if data:
        df = px.DataFrame(data, data_frame=True)
        return df.line(title='Security Audit Log Over Time')
    else:
        return {"data": [], "layout": {"title": "No data to display"}}

# 记录所有进入 Flask 应用的请求
@app.before_request
def before_request():
    try:
        log_request(request)
    except Exception as e:
        logging.error(f"Error logging request: {e}")

# 记录所有 Flask 应用的响应
@app.after_request
def after_request(response):
    try:
        log_response(response)
    except Exception as e:
        logging.error(f"Error logging response: {e}")
    return response

# 启动 Dash 应用
if __name__ == '__main__':
    app.run_server(debug=True)