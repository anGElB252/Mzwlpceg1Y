# 代码生成时间: 2025-08-04 08:47:41
import dash\
import dash_core_components as dcc\
import dash_html_components as html\
from dash.dependencies import Input, Output, State\
import plotly.express as px\
import pandas as pd\
\
# 引入Dash的CSS\
app = dash.Dash(__name__)\
app.title = "Theme Switcher"\
\
# 主页布局\
app.layout = html.Div([\
    dcc.Dropdown(\
        id='theme-selector',\
        options=[\
            {"label": "Dark", "value": "dark"},\
            {"label": "Light", "value": "light"}  # 添加更多主题时可以在这里添加\
        ],\
        value="light",  # 默认主题\
    ),\
    dcc.Graph(id='example-graph'),\
    html.P("Change the theme to see the effect."),\
])\
\
# 回调函数，用于更新图表主题\
@app.callback(\
    Output('example-graph', 'figure'),\
    [Input('theme-selector', 'value')],\
    [State('example-graph', 'figure')]\
)\
def update_graph_theme(theme, figure):
    # 根据主题改变颜色
    if theme == "dark":
        new_theme = "plotly_dark"
    elif theme == "light":
        new_theme = "plotly"
    else:
        # 如果没有匹配的主题，使用默认的plotly主题
        new_theme = "plotly"
        # 这里可以添加错误处理
        print("Warning: Unknown theme selected. Defaulting to Plotly theme.")
    # 应用主题并返回新的图表
    figure.update_layout(template=new_theme)
    return figure\
\
# 添加示例数据和图表\
df = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [10, 11, 12, 13]})\
app.clientside_callback(
    