# 代码生成时间: 2025-08-19 08:27:25
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import requests
import logging
from flask import Flask, session
from flask_caching import Cache
from dash.exceptions import PreventUpdate

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Message Notification System'

# 初始化缓存
cache = Cache(app.server, config={"CACHE_TYPE": "simple"})

# 首页布局
def home_layout():
    return html.Div([
        html.H1("Message Notification System"),
        html.P("Welcome to the message notification system."),
        dcc.Input(id="message-input", type="text", placeholder="Enter message"),
        html.Button("Send Message", id="send-button", n_clicks=0),
        dcc.Dropdown(
            id="user-dropdown",
            options=[{"label": user, "value": user} for user in session.get("users", [])],
            value=session.get("selected_user", ""),
            multi=False,
        ),
        dcc.Interval(id="interval-component", interval=1000, disabled=False),
        html.Div(id="output-container"),
    ])

# 回调：发送消息
@app.callback(
    Output("output-container", "children"),
    [Input("send-button", "n_clicks"), Input("interval-component", "n_intervals")],
    [State("message-input", "value"), State("user-dropdown", "value")],
)
def send_message(n_clicks, n_intervals, message, selected_user):
    # 检查输入
    if not message or not selected_user:
        raise PreventUpdate
    
    # 发送消息到指定用户
    try:
        response = requests.post("http://localhost:5000/api/send_message", json={"message": message, "user": selected_user})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message: {e}")
        return dbc.Alert("Failed to send message.", color="danger")
    
    # 返回成功消息
    return dbc.Alert("Message sent successfully!", color="success")

# 启动服务器
def run_server():
    app.layout = home_layout()
    app.run_server(debug=True)

# 主函数
def main():
    run_server()

if __name__ == "__main__":
    main()