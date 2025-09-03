# 代码生成时间: 2025-09-03 09:11:07
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import math
import numpy as np

# 定义一个数学计算工具集应用
class MathCalculator:
    def __init__(self, app):
        self.app = app
        self.init_layout()
        self.init_callbacks()

    # 初始化布局
    def init_layout(self):
        self.app.layout = dbc.Container([
            dbc.Row(
                dbc.Col(html.H1("数学计算工具集"), width=12)
            ),
            dbc.Row(
                dbc.Col(dcc.Input(id='number1', type='number'), width=4),
                dbc.Col(dcc.Input(id='number2', type='number'), width=4),
                dbc.Col(dcc.Button('计算', id='calculate-button', n_clicks=0)),
                dbc.Col(dcc. Output(id='result'), width=4)
            ),
            dbc.Row(
                dbc.Col(html.P("支持的运算包括: 加法、减法、乘法、除法"), width=12)
            )
        ])

    # 初始化回调函数
    def init_callbacks(self):
        @self.app.callback(
            Output('result', 'children'),
            [Input('calculate-button', 'n_clicks')],
            prevent_initial_call=True,
            state=[State('number1', 'value'), State('number2', 'value')]
        )
        def calculate(n_clicks, number1, number2):
            if n_clicks is None or number1 is None or number2 is None:
                return '请选择两个数字并点击计算'
            try:
                if number1 == '' or number2 == '':
                    return '请输入两个数字'
                num1 = float(number1)
                num2 = float(number2)
                if n_clicks % 4 == 1:
                    return f'{num1} + {num2} = {num1 + num2}'
                elif n_clicks % 4 == 2:
                    return f'{num1} - {num2} = {num1 - num2}'
                elif n_clicks % 4 == 3:
                    return f'{num1} * {num2} = {num1 * num2}'
                elif n_clicks % 4 == 0:
                    if num2 == 0:
                        return '除数不能为0'
                    return f'{num1} / {num2} = {num1 / num2}'
            except ValueError:
                return '请输入有效的数字'

# 主函数
def main():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    MathCalculator(app)
    app.run_server(debug=True)

if __name__ == '__main__':
    main()