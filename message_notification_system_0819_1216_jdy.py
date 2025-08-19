# 代码生成时间: 2025-08-19 12:16:06
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import requests
from flask import Response
from jinja2 import Template
import json
import logging

# 设置日志记录级别
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定义消息通知系统
class MessageNotificationSystem:
    def __init__(self, app):
        # 初始化Dash应用
        self.app = app
        self.app.layout = self.create_layout()
        self.register_callbacks()

    def create_layout(self):
        # 创建Dash应用的布局
        return dbc.Container(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                html.H1("消息通知系统"),
                                html.P("这是一个简单的消息通知系统"),
                                dcc.Input(id="message-input", type="text", placeholder="输入消息"),
                                dbc.Button("发送消息", id="send-button", n_clicks=0, className="me-2"),
                                html.Div(id="message-output"),
                            ],
                            width=12,
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                html.H2("历史消息"),
                                dcc.Graph(id="message-graph"),
                            ],
                            width=12,
                        ),
                    ],
                    className="mb-4",
                ),
            ],
            className="mt-4",
        )

    def register_callbacks(self):
        # 注册回调函数
        @self.app.callback(
            Output("message-output", "children"),
            [Input("send-button", "n_clicks"), Input("message-input", "value")],
            [State("message-input", "value"), State("send-button", "n_clicks")],
        )
        def send_message(n_clicks, message, message_state, n_clicks_state):
            # 发送消息的回调函数
            if n_clicks is None or n_clicks_state is None:
                return ""
            return html.Div(
                children=[
                    html.P("消息已发送: " + message),
                ],
            )

        @self.app.callback(
            Output("message-graph", "figure"),
            [Input("message-input", "value")],
            [State("message-input", "value")],
        )
        def update_graph(message):
            # 更新历史消息图表的回调函数
            if not message:
                return px.line(pd.DataFrame())

            # 模拟发送消息到后端
            try:
                response = requests.post("http://localhost:5000/message", json={"message": message})
                response.raise_for_status()
            except requests.RequestException as e:
                logger.error("发送消息失败: %s", e)
                return px.line(pd.DataFrame())

            # 获取历史消息
            try:
                response = requests.get("http://localhost:5000/messages")
                response.raise_for_status()
                messages = response.json()

                # 创建历史消息图表
                df = pd.DataFrame(messages, columns=["message", "timestamp"])
                return px.line(df, x="timestamp", y="message")
            except requests.RequestException as e:
                logger.error("获取历史消息失败: %s", e)
                return px.line(pd.DataFrame())

# 创建Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
MessageNotificationSystem(app)

if __name__ == "__main__":
    app.run_server(debug=True)