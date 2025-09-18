# 代码生成时间: 2025-09-18 10:41:38
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

# 定义Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div([
    html.H1("交互式图表生成器"),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': '数据集1', 'value': 'dataset1'},
            {'label': '数据集2', 'value': 'dataset2'}
        ],
        value='dataset1'  # 默认值
    ),
    dcc.Graph(id='graph')
])

# 回调函数，当下拉框选项改变时更新图表
@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value')]
)
def update_graph(selected_dataset):
    # 根据选择的数据集加载数据
    if selected_dataset == 'dataset1':
        df = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [10, 20, 25, 30]})
    elif selected_dataset == 'dataset2':
        df = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [40, 30, 20, 10]})
    else:
        # 如果选择的数据集无效，则返回空图表
        raise ValueError('无效的数据集')

    # 创建图表
    fig = px.line(df, x='x', y='y', title=f'{selected_dataset}的图表')
    return fig

# 运行应用
def run_app():
    app.run_server(debug=True)

# 如果直接运行该脚本，则启动应用
if __name__ == '__main__':
    run_app()