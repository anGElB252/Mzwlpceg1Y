# 代码生成时间: 2025-08-16 14:53:11
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

# 设置数据库连接
DATABASE = 'login.db'

# 函数：创建数据库连接
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# 函数：创建用户表
def create_user_table():
    conn = get_db_connection()
    try:
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT NOT NULL UNIQUE,
                     password TEXT NOT NULL)'')
    finally:
        conn.close()

# 函数：注册新用户
def register_user(username, password):  # 密码存储为哈希值
    conn = get_db_connection()
    try:
        password_hash = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
    finally:
        conn.close()

# 函数：验证用户登录
def validate_login(username, password):  # 验证密码是否正确
    conn = get_db_connection()
    try:  # 找到用户名对应的哈希密码
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password'], password):  # 验证密码
            return True
        return False
    finally:
        conn.close()

# Dashboard 应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(
    [dbc.Row(
        dbc.Col(
            dbc.Card(
                [dbc.CardHeader("Login"),
                 dbc.CardBody(
                     [dbc.Form(
                         [dbc.FormGroup(
                             [dbc.Label("Username"),
                             dbc.Input(type="text", placeholder="Enter username"),
                             ],
                             className="mb-3"),
                         dbc.FormGroup(
                             [dbc.Label("Password"),
                             dbc.Input(type="password", placeholder="Enter password")
                             ],
                             className="mb-3"),
                         dbc.Button("Login", color="primary", className="mt-3", type="submit")
                     ],
                     className="p-3")
                ],
                className="mt-3"),
            ),
            width=6,
        ),
        className="mt-4"),
    ],
    fluid=True,
)

# 回调函数：处理登录
@app.callback(
    Output('login-card-body', 'children'),  # 输出到CardBody组件
    [Input('login-form', 'submit_n_click_timestamp')],  # 表单提交事件
    [State('username-input', 'value'), State('password-input', 'value')]  # 输入框的值
)
def handle_loginsubmit(timestamp, username, password):  # 登录提交事件的回调函数
    if validate_login(username, password):  # 密码验证
        session['logged_in'] = True  # 将用户名存储到session中
        return dbc.Alert("Login successful!", color="success")
    else:  # 登录失败
        return dbc.Alert("Invalid username or password!", color="danger")

if __name__ == '__main__':
    create_user_table()  # 创建用户表
    app.run_server(debug=True)