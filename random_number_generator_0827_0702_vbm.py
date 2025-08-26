# 代码生成时间: 2025-08-27 07:02:17
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import random

# 定义 Dash 应用程序
app = dash.Dash(__name__)

# 设定应用程序布局
app.layout = html.Div(children=[
    # 添加标题
    html.H1(children='Random Number Generator'),
    # 添加输入框以设置随机数范围
    dcc.Input(id='input-number', type='number', placeholder='Enter number range (e.g. 1-100)'),
    # 添加按钮以触发随机数生成
    html.Button('Generate', id='generate-button', n_clicks=0),
    # 添加输出框以显示生成的随机数
    html.Div(id='output-container')
])

# 定义回调函数以处理按钮点击事件
@app.callback(
    Output('output-container', 'children'),
    [Input('generate-button', 'n_clicks')],
    [State('input-number', 'value')]
)
def generate_random_number(n_clicks, number_range):
    if n_clicks > 0:  # 确保按钮被点击过
        try:
            # 将输入值转换为整数并生成随机数
            lower, upper = map(int, number_range.split('-'))
            random_number = random.randint(lower, upper)
            # 返回生成的随机数
            return f'Random Number: {random_number}'
        except (ValueError, TypeError):  # 错误处理
            # 如果输入无效，则返回错误信息
            return 'Please enter a valid number range (e.g. 1-100)'
    return ''  # 如果按钮未被点击，则返回空字符串

# 运行应用程序
if __name__ == '__main__':
    app.run_server(debug=True)