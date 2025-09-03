# 代码生成时间: 2025-09-03 14:31:41
import hashlib
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# 定义Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div([
    html.H1('Hash Calculator Tool'),
    dcc.Textarea(id='input-text', placeholder='Enter text here...', style={'width': '100%', 'height': '100px'}),
    html.Button('Calculate Hash', id='calculate-button', n_clicks=0),
    html.Div(id='output-hash')
])

# 定义回调函数以计算哈希值
@app.callback(
    Output('output-hash', 'children'), 
    [Input('calculate-button', 'n_clicks')],
    [State('input-text', 'value')]
)
def calculate_hash(n_clicks, input_text):
    if n_clicks is None or input_text is None or input_text == '':
        raise PreventUpdate()
    
    # 将输入文本转换为字节
    text_bytes = input_text.encode('utf-8')
    
    # 计算MD5哈希值
    md5_hash = hashlib.md5(text_bytes).
        hexdigest()
    
    # 计算SHA256哈希值
    sha256_hash = hashlib.sha256(text_bytes).
        hexdigest()
    
    # 返回哈希值的HTML格式
    return html.Div([
        html.H3('MD5 Hash:'),
        html.P(md5_hash),
        html.H3('SHA256 Hash:'),
        html.P(sha256_hash)
    ])

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)