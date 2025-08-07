# 代码生成时间: 2025-08-07 10:34:25
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import requests
import json

# API响应格式化工具
class ApiResponseFormatter:
    def __init__(self, app):
        # 初始化Dash应用
        self.app = app
        self.app.layout = html.Div([
            html.H1("API响应格式化工具"),
            dbc.Input(id="api-url", placeholder="请输入API URL"),
            dbc.Button("发送请求", id="send-request", n_clicks=0),
            html.Div(id="response-container")
        ])

        # 定义回调函数
        @self.app.callback(
            Output("response-container", "children\),
            [Input("send-request", "n_clicks\)],
            [State("api-url", "value\)]
        )
        def send_request(n_clicks, api_url):
            if n_clicks is None or api_url is None:
                return ""
            try:
                response = requests.get(api_url)
                response.raise_for_status()
                formatted_response = self.format_response(response.json())
                return html.Pre(formatted_response)
            except requests.RequestException as e:
                return f"请求错误：{e}"
            except json.JSONDecodeError as e:
                return f"解析错误：{e}"

    def format_response(self, response):
        """格式化API响应"""
        formatted_response = json.dumps(response, indent=4, ensure_ascii=False)
        return formatted_response

# 创建Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 实例化ApiResponseFormatter
api_response_formatter = ApiResponseFormatter(app)

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)