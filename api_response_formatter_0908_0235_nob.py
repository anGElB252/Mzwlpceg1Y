# 代码生成时间: 2025-09-08 02:35:23
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import json

# 定义一个函数，用于格式化API响应
def format_api_response(response):
    # 检查响应是否为None
    if response is None:
        return {"error": "No response received"}
    # 检查响应是否为JSON字符串
    try:
        # 尝试将响应解析为JSON
        parsed_response = json.loads(response)
    except json.JSONDecodeError:
        # 如果解析失败，返回错误信息
        return {"error": "Invalid JSON response"}
    # 返回格式化后的响应
    return {"success": True, "data": parsed_response}

# 创建Dash应用
app = dash.Dash(__name__)

# 定义布局
app.layout = html.Div([
    # 响应输入框
    dcc.Textarea(
        id='api-response-input',
        placeholder='Paste your API response here...',
        style={'width': '100%', 'height': '200px'}
    ),
    # 格式化按钮
    html.Button('Format Response', id='format-button'),
    # 格式化后的结果输出框
    dcc.Textarea(
        id='formatted-response-output',
        placeholder='Formatted response will appear here...',
        style={'width': '100%', 'height': '200px'}
    )
])

# 定义回调函数，用于处理按钮点击事件
@app.callback(
    Output('formatted-response-output', 'value'),
    [Input('format-button', 'n_clicks')],
    [State('api-response-input', 'value')]
)
def format_response(n_clicks, response_value):
    # 如果按钮未被点击，阻止更新
    if n_clicks is None:
        raise PreventUpdate()
    # 格式化API响应
    formatted_response = format_api_response(response_value)
    # 返回格式化后的结果
    return json.dumps(formatted_response, indent=4)

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)