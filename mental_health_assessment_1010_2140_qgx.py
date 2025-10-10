# 代码生成时间: 2025-10-10 21:40:55
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
import pandas as pd

# 初始化Dash应用
app = dash.Dash(__name__)
server = app.server

# 应用布局
app.layout = html.Div(children=[
    html.H1(children='Mental Health Assessment'),
    html.Div(children='''Please answer the following questions to assess your mental health.'''),
    dcc.Dropdown(
        id='question1',
        options=[{'label': 'Always', 'value': 'always'},
                 {'label': 'Often', 'value': 'often'},
                 {'label': 'Sometimes', 'value': 'sometimes'},
                 {'label': 'Rarely', 'value': 'rarely'},
                 {'label': 'Never', 'value': 'never'}],
        value=['sometimes'],
        multi=True
    ),
    dcc.Dropdown(
        id='question2',
        options=[{'label': 'Always', 'value': 'always'},
                 {'label': 'Often', 'value': 'often'},
                 {'label': 'Sometimes', 'value': 'sometimes'},
                 {'label': 'Rarely', 'value': 'rarely'},
                 {'label': 'Never', 'value': 'never'}],
        value=['sometimes'],
        multi=True
    ),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output-container')
])

# 计算器回调函数
@app.callback(
    Output('output-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('question1', 'value'), State('question2', 'value')]
)
def update_output(n_clicks, question1, question2):
    # 错误处理
    if n_clicks == 0:
        raise PreventUpdate()
    
    # 计算总分
    total_score = len(question1) + len(question2)
    
    # 返回结果
    if total_score < 10:
        return html.Div(children='''You are doing well and are managing your mental health effectively.''')
    else:
        return html.Div(children='''You may be experiencing difficulties with your mental health and should consider seeking professional help.''')

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)