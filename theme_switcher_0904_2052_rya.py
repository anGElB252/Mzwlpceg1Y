# 代码生成时间: 2025-09-04 20:52:16
import dash
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

# 主题切换函数
def toggle_theme(switch_input, color_scheme):
    # 如果切换输入与当前颜色方案相同，则返回防止更新
    if switch_input == color_scheme:
        raise PreventUpdate
    # 返回新的颜色方案
    return switch_input

# 定义Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 应用布局
app.layout = dbc.Container(
    children=[
        # 主题切换开关
        dbc.Switch(
            id='theme-switch',
            on_value='dark',
            off_value='light',
            value='light',
            label='Dark Mode',
            labelPosition='bottom',
        ),

        # 响应式元素
        html.Div(id='theme-display', children=''),
    ],
)

# 回调函数，用于更新主题
@app.callback(
    Output('theme-display', 'children'),
    [Input('theme-switch', 'value'), State('theme-switch', 'value')],
)
def update_theme(switch_input, current_value):
    # 如果输入与当前值相同，则不进行任何操作
    if switch_input == current_value:
        raise PreventUpdate
    # 根据主题切换显示相应的文本
    if switch_input == 'dark':
        return 'Dark mode is enabled'
    else:
        return 'Light mode is enabled'

# 回调函数，用于实际切换主题
@app.callback(
    Output('theme-display', 'children'),
    [Input('theme-switch', 'value')],
    prevent_initial_call=True,
)
def apply_theme(switch_input):
    # 根据主题切换输出不同的CSS样式
    if switch_input == 'dark':
        return dbc.Alert(
            'Dark mode is enabled', color='primary', className='text-left'
        )
    else:
        return dbc.Alert(
            'Light mode is enabled', color='warning', className='text-left'
        )

if __name__ == '__main__':
    app.run_server(debug=True)