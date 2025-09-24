# 代码生成时间: 2025-09-24 11:02:59
import logging
from flask import Flask, request
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# 设置日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask 应用
server = Flask(__name__)

# Dash 应用
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义 Dash 应用界面
app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(html.H1("错误日志收集器"), width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Input(id="error-message", type="text", placeholder="输入错误信息"), width=8),
            dbc.Col(dbc.Button("提交错误", id="submit-error", className="mt-2"), width=4),
        ]),
        dbc.Row([dbc.Col(dcc.Textarea(id="error-log", placeholder="错误日志显示在这里"), width=12)]),
    ],
    fluid=True,
)

# 回调函数处理错误提交
@app.callback(
    Output("error-log", "value"),
    [Input("submit-error", "n_clicks")],
    [State("error-message", "value")],
)
def submit_error(n_clicks, error_message):
    if n_clicks is None:
        # 没有提交错误
        return ""
    else:
        # 处理错误消息并添加到日志
        logger.error(error_message)
        # 将错误消息添加到 textarea
        return error_message + "
"

# 运行 Dash 应用
if __name__ == "__main__":
    app.run_server(debug=True)
