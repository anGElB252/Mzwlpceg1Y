# 代码生成时间: 2025-08-06 14:27:22
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash.themes import FLATLY
from dash.themes import UNITED
import dash_bootstrap_components as dbc

# 初始化Dash应用程序
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Theme Switcher App'

# 定义应用布局
app.layout = dbc.Container(
    children=[
        html.H1('Theme Switcher', className='mb-5'),
        html.Div(
            dcc.Dropdown(
                id='theme-selector',
                options=[
                    {'label': 'Flatly', 'value': FLATLY},
                    {'label': 'United', 'value': UNITED},
                ],
                value=FLATLY,  # 默认主题
            ),
            className='mb-5',
        ),
        html.Div(
            dcc.Graph(
                id='example-graph',
                figure={'data': [{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar'}]},
            ),
        ),
    ],
    fluid=True,
)

# 回调函数，用于切换主题
@app.callback(
    Output('theme-selector', 'options'),
    Input(app.layout, 'style'),
)
def update_dropdown(style):
    # 如果布局样式发生了变化，则更新主题选择器的选项列表
    if style:
        theme = style['externalStylesheets'][0]
        return [{'label': 'Switch Theme', 'value': theme}]
    raise PreventUpdate()

# 回调函数，用于根据选择的主题更新应用程序布局的样式
@app.callback(
    Output(app.layout, 'style'),
    Input('theme-selector', 'value'),
)
def change_theme(value):
    # 根据选择的主题值，更新应用程序的样式
    if value:
        return [{'external_stylesheets': [value]}]
    raise PreventUpdate()

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)