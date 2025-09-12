# 代码生成时间: 2025-09-12 15:10:05
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import json
from flask import escape

# 定义一个函数来格式化API响应
def format_api_response(response, status_code=200, headers=None):
    """
    格式化API响应并返回指定的状态码和头信息。
    
    参数:
    response (dict): API响应内容。
    status_code (int): HTTP状态码，默认为200。
    headers (dict): HTTP头信息，默认为空。
    
    返回:
    tuple: 格式化后的响应内容和状态码及头信息。
    """
    if not isinstance(response, dict):
        raise ValueError("响应内容必须是字典类型")
    if headers is None:
        headers = {}
    return (json.dumps(response), status_code, headers)

# 创建Dash应用
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("API响应格式化工具"),
    dcc.Textarea(
        id='api-response-input',
        placeholder='输入API响应内容',
        style={'width': '100%', 'height': '200px'}
    ),
    html.Button('格式化响应', id='format-button'),
    html.Div(id='formatted-response')
])

# 定义回调函数来处理格式化操作
@app.callback(
    Output('formatted-response', 'children'),
    [Input('format-button', 'n_clicks')],
    [State('api-response-input', 'value')]
)
def format_response(n_clicks, api_response):
    """
    处理格式化按钮点击事件。
    
    参数:
    n_clicks (int): 按钮点击次数。
    api_response (str): 输入的API响应内容。
    
    返回:
    str: 格式化后的响应内容。
    """
    if n_clicks is None or n_clicks < 1:  # 防止未点击按钮时触发回调
        return ''
    try:
        # 尝试解析输入的API响应内容
        response = json.loads(api_response)
        # 格式化响应内容
        formatted_response, _, _ = format_api_response(response)
        return escape(formatted_response)  # 使用Flask的escape函数转义HTML特殊字符
    except json.JSONDecodeError:  # 处理解析错误
        return '输入的API响应内容格式不正确'
    except Exception as e:  # 处理其他异常
        return f'发生错误：{str(e)}'

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)