# 代码生成时间: 2025-08-02 13:02:52
# 用户登录验证系统
# 使用Python和Dash框架实现

# 导入必要的库
import dash
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

# 定义用户数据
users = {
    "admin": generate_password_hash("admin")
}

# 定义Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H1("用户登录"),
                        dbc.Form(
                            children=[
                                dbc.FormGroup(
                                    children=[
                                        dbc.Label("用户名"),
                                        dbc.Input(
                                            type="text", id="username", placeholder='请输入用户名'
                                        )
                                    ]
                                ),
                                dbc.FormGroup(
                                    children=[
                                        dbc.Label("密码"),
                                        dbc.Input(
                                            type="password", id="password", placeholder='请输入密码'
                                        )
                                    ]
                                ),
                                dbc.Button("登录", color="primary", id="login-button"),
                                html.Div(id="login-output")
                            ]
                        )
                    ],
                    width=6
                )
            ]
        )
    ]
)

# 登录逻辑
@app.callback(
    Output("login-output", "children"),
    [Input("login-button", "n_clicks")],
    prevent_initial_call=True
)
def login(n_clicks):
    if n_clicks is None:
        return None
    username = dash.callback_context.inputs.get("username")
    password = dash.callback_context.inputs.get("password")
    if username is None or password is None:
        return "请填写用户名和密码"
    user_hash = users.get(username)
    if user_hash is None:
        return "用户名不存在"
    if not check_password_hash(user_hash, password):
        return "密码错误"
    session["username"] = username
    return "登录成功"

# 运行应用
if __name__ == "__main__":
    app.run_server(debug=True)