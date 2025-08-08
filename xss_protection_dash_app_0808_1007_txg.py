# 代码生成时间: 2025-08-08 10:07:30
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import request
from bs4 import BeautifulSoup
import re

# 定义XSS攻击防护函数
def xss_protection(input_string):
    # 将输入字符串转换为BeautifulSoup对象
    soup = BeautifulSoup(input_string, 'html.parser')
    # 移除所有脚本和iframe标签
    for script in soup(["script", "iframe"]):
        script.extract()  # rip it out
    # 移除所有属性，如onerror, onclick等
    for tag in soup.find_all(True):  # 遍历所有标签
        for attribute in tag.attrs:  # 遍历标签的所有属性
            if attribute.startswith('on'):  # 如果属性以'on'开头，移除
                del tag[attribute]
    return str(soup)

# 创建Dash应用
app = dash.Dash(__name__)

# 定义网页布局
app.layout = html.Div([
    html.H1("XSS Protection Dash App"),
    dcc.Input(id='input-string', type='text', placeholder='Enter your input here...'),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output'),
])

# 定义回调函数，用于处理表单提交
@app.callback(
    Output('output', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input-string', 'value')]
)
def submit(input_value):  # 处理输入值
    if input_value is None:  # 检查输入值是否为空
        raise dash.exceptions.PreventUpdate  # 阻止更新
    try:  # 尝试防护XSS攻击
        protected_string = xss_protection(input_value)
        return html.Div(protected_string)  # 返回防护后的字符串
    except Exception as e:  # 错误处理
        return f'Error: {str(e)}'  # 返回错误信息

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)
