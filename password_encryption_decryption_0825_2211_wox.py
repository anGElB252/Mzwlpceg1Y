# 代码生成时间: 2025-08-25 22:11:26
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from cryptography.fernet import Fernet

# 初始化密钥
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# 定义Dash应用
app = dash.Dash(__name__)

# 定义应用布局
app.layout = html.Div([
    html.H1("Password Encryption Decryption Tool"),
    html.Div([
        html.Label("Enter Password:"),
        dcc.Input(id="password-input", type="password", value=""),
    ]),
    html.Button("Encrypt", id="encrypt-button"),
    html.Button("Decrypt", id="decrypt-button"),
    html.Div(id="output-container"),
])

# 回调函数：加密密码
@app.callback(
    Output("output-container", "children"),
    [Input("encrypt-button", "n_clicks")],
    [State("password-input", "value")],
)
def encrypt(n_clicks, password):
    if n_clicks is None or password == "":
        return ""
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    return html.Div([
        html.H3("Encrypted Password:"),
        html.Pre(encrypted_password)
    ])

# 回调函数：解密密码
@app.callback(
    Output("output-container", "children"),
    [Input("decrypt-button", "n_clicks")],
    [State("password-input", "value")],
)
def decrypt(n_clicks, encrypted_password):
    if n_clicks is None or encrypted_password == "":
        return ""
    try:
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
    except Exception as e:
        return html.Div([
            html.H3("Decryption Error:"),
            html.Pre(str(e))
        ])
    return html.Div([
        html.H3("Decrypted Password:"),
        html.Pre(decrypted_password)
    ])

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)