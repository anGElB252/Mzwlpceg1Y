# 代码生成时间: 2025-08-01 15:30:18
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64
import cryptography.fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding

# 生成密钥函数
def generate_key():
    key = base64.urlsafe_b64encode(cryptography.fernet.Fernet.generate_key())
    return key

# 加密函数
def encrypt_message(message, key):
    try:
        fernet = cryptography.fernet.Fernet(base64.urlsafe_b64decode(key))
        encrypted_message = fernet.encrypt(message.encode())
        return encrypted_message
    except Exception as e:
        return str(e)

# 解密函数
def decrypt_message(encrypted_message, key):
    try:
        fernet = cryptography.fernet.Fernet(base64.urlsafe_b64decode(key))
        decrypted_message = fernet.decrypt(encrypted_message).decode()
        return decrypted_message
    except Exception as e:
        return str(e)

# DASH 应用程序
app = dash.Dash(__name__)

# 布局
app.layout = html.Div(children=[
    html.H1(children='Password Encryption and Decryption Tool'),
    html.Div(children=[
        html.Label('Message'),
        dcc.Input(id='message-input', type='text', value=''),
    ]),
    html.Div(children=[
        html.Label('Key'),
        dcc.Input(id='key-input', type='text', value=''),
    ]),
    html.Button('Encrypt', id='encrypt-button', n_clicks=0),
    html.Button('Decrypt', id='decrypt-button', n_clicks=0),
    html.Div(id='output-container'),
])

# 回调函数：加密
@app.callback(
    Output('output-container', 'children'),
    [Input('encrypt-button', 'n_clicks'),
     Input('message-input', 'value'),
     Input('key-input', 'value')],
    prevent_initial_call=True)
def encrypt(n_clicks, message, key):
    if n_clicks == 0 or not message or not key:
        return ''
    return html.Div(id='encrypted-message', children=encrypt_message(message, key))

# 回调函数：解密
@app.callback(
    Output('output-container', 'children'),
    [Input('decrypt-button', 'n_clicks'),
     Input('message-input', 'value'),
     Input('key-input', 'value')],
    prevent_initial_call=True)
def decrypt(n_clicks, message, key):
    if n_clicks == 0 or not message or not key:
        return ''
    return html.Div(id='decrypted-message', children=decrypt_message(message, key))

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)