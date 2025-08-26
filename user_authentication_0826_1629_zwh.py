# 代码生成时间: 2025-08-26 16:29:19
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

# 假设用户数据存储在内存中，实际应用中应使用数据库
users = {
    "admin": generate_password_hash("admin123")
}

# Dash应用
app = dash.Dash(__name__)

# 身份验证页面
app.layout = html.Div(
    [
        html.H1("用户身份认证"),
        dcc.Input(id="username", type="text", placeholder="用户名"),
        dcc.Input(id="password", type="password", placeholder="密码"),
        html.Button("登录", id="login-button", n_clicks=0),
        html.Div(id="output")
    ]
)

# 登录函数
@app.callback(
    Output("output", "children"),
    [Input("login-button", "n_clicks")],
    [State("username", "value"), State("password", "value")]
)
def login(n_clicks, username, password):
    if n_clicks > 0:
        # 检查用户名和密码是否正确
        if username in users and check_password_hash(users[username], password):
            # 将用户信息存储在session中
            session["username"] = username
            return "登录成功！"
        else:
            return "用户名或密码错误！"
    return None

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)