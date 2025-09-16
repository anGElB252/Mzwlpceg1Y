# 代码生成时间: 2025-09-17 07:54:40
import dash
import dash_auth
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# 定义用户和密码，实际部署时需使用更安全的方式存储
AUTH_BASIC = {
    "admin": "admin",
    "user": "user"
}

# 设置认证回调函数
def load_auth_credentials():
    """
    加载认证凭据。
    """
    return AUTH_BASIC

# 创建Dash应用
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# 添加认证组件
auth = dash_auth.BasicAuth(
    app,
    load_auth_credentials,
    # 错误消息
    "Please enter username and password"
)

# 定义Dash应用布局
app.layout = html.Div([
    html.H1("Dash Access Control Example"),
    # 按钮用于重新加载页面并触发认证
    html.Button("Logout", id="logout-button"),
    # 条件渲染的内容
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# 定义回调函数
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
    prevent_initial_call=True
)
def display_page(pathname):
    """
    根据URL路径显示内容。
    """
    if pathname == "/":
        return html.Div([
            html.H2("Welcome to the Dash Access Control Example!"),
            html.P("Visit /admin to see the Admin Dashboard."),
            html.P("Visit /user to see the User Dashboard.")
        ])
    elif pathname == "/admin":
        if auth.get_user():
            return html.Div([
                html.H2("Admin Dashboard"),
                html.P("Welcome, you have admin access."),
                # 可以添加更多管理员面板组件
            ])
        else:
            raise PreventUpdate("Not authorized to view this section.")
    elif pathname == "/user":
        if auth.get_user():
            return html.Div([
                html.H2("User Dashboard"),
                html.P("Welcome, you have user access."),
                # 可以添加更多用户面板组件
            ])
        else:
            raise PreventUpdate("Not authorized to view this section.")
    else:
        return html.Div([
            html.H1("404: Not found"),
            html.P("The page you are looking for does not exist.")
        ])

# 定义回调函数处理登出按钮事件
@app.callback(
    Output("url", "pathname"),
    [Input("logout-button", "n_clicks")],
    [dash.State("url", "pathname")]
)
def logout(n_clicks, pathname):
    """
    处理登出按钮点击事件，重定向到登录页面。
    """
    if n_clicks:
        auth.clear_credentials()
        return ""
    return pathname

# 启动Dash应用程序
if __name__ == '__main__':
    app.run_server(debug=True)