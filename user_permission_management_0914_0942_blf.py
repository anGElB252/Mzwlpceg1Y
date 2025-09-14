# 代码生成时间: 2025-09-14 09:42:30
import dash
from dash import dcc, html, Input, Output
from dash.dependencies import MATCH, ALL
from flask import session
from flask_simplelogin import SimpleLogin
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate

# 定义用户数据类
class UserData:
    def __init__(self):
        self.user_data = pd.DataFrame(columns=['username', 'email', 'password', 'role'])
        self.user_data = self.user_data.append({'username': 'admin', 'email': 'admin@example.com', 'password': 'admin', 'role': 'admin'}, ignore_index=True)
        self.user_data = self.user_data.append({'username': 'user', 'email': 'user@example.com', 'password': 'user', 'role': 'user'}, ignore_index=True)

    def login(self, username, password):
        return (username, password) in self.user_data.set_index('username')[['password', 'role']].itertuples(index=False)

    def logout(self):
        session.pop('user', None)

# 初始化Dash应用和SimpleLogin
app = dash.Dash(__name__)
server = app.server
SimpleLogin(app, login_url='/login')
app.title = 'User Permission Management'

# 设置登录页面
app.layout = html.Div([
    html.H1('Login'),
    dcc.Input(id='email-login', type='email', placeholder='Enter your email'),
    dcc.Input(id='password-login', type='password', placeholder='Enter your password'),
    html.Button('Login', id='login-button', n_clicks=0),
    html.Div(id='login-output')
])

# 设置用户权限页面
app.layout = html.Div([
    html.H1('User Permission Management'),
    dcc.Dropdown(
        id='user-dropdown',
        options=[{'label': user, 'value': user} for user in UserData().user_data['username']],
        value='admin',
        multi=False
    ),
    html.Button('Grant Admin', id='grant-admin-button', n_clicks=0),
    html.Button('Revoke Admin', id='revoke-admin-button', n_clicks=0),
    html.Div(id='user-output')
], id='user-permission-output')

# 回调函数：处理登录
@app.callback(
    Output('login-output', 'children'),
    Input('login-button', 'n_clicks'),
    Input('email-login', 'value'),
    Input('password-login', 'value'),
    prevent_initial_call=True
)
def login(n_clicks, email, password):
    if n_clicks > 0:
        user_data = UserData()
        valid_user = user_data.login(email, password)
        if valid_user:
            session['user'] = {'email': email, 'role': valid_user[1]}
            return 'Logged in successfully!'
        else:
            return 'Invalid credentials!'
    raise PreventUpdate()

# 回调函数：处理登出
@app.callback(
    Output('user-permission-output', 'style'),
    Input('logout-button', 'n_clicks'),
    prevent_initial_call=True
)
def logout(n_clicks):
    if n_clicks > 0:
        UserData().logout()
        return {'display': 'none'}
    raise PreventUpdate()

# 回调函数：处理权限授予
@app.callback(
    Output('user-output', 'children'),
    Input('grant-admin-button', 'n_clicks'),
    State('user-dropdown', 'value'),
    prevent_initial_call=True
)
def grant_admin(n_clicks, user):
    if n_clicks > 0:
        if session.get('user', {}).get('role') == 'admin':
            user_data = UserData()
            user_data.user_data.loc[user_data.user_data['username'] == user, 'role'] = 'admin'
            return f'Admin privileges granted to {user}!'
        else:
            return 'You do not have permission to grant admin privileges!'
    raise PreventUpdate()

# 回调函数：处理权限撤销
@app.callback(
    Output('user-output', 'children'),
    Input('revoke-admin-button', 'n_clicks'),
    State('user-dropdown', 'value'),
    prevent_initial_call=True
)
def revoke_admin(n_clicks, user):
    if n_clicks > 0:
        if session.get('user', {}).get('role') == 'admin':
            user_data = UserData()
            user_data.user_data.loc[user_data.user_data['username'] == user, 'role'] = 'user'
            return f'Admin privileges revoked from {user}!'
        else:
            return 'You do not have permission to revoke admin privileges!'
    raise PreventUpdate()

if __name__ == '__main__':
    app.run_server(debug=True)