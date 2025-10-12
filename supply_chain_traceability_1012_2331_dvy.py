# 代码生成时间: 2025-10-12 23:31:47
# 供应链溯源系统

# 导入必要的库
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# 数据加载和预处理
df = pd.read_csv('supply_chain_data.csv')

# 创建Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 应用布局
app.layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("供应链溯源"),
                        dbc.CardBody(
                            dbc.Row(
                                [
                                    dbc.Col(html.Div(id='traceability-output'))
                                ]
                            )
                        )
                    ]
                ),
                body=True
            )
        )
    ]
)

# 回调函数：供应链溯源
@app.callback(
    Output('traceability-output', 'children'),
    [Input('column-selector', 'value')],  # 假设有一个下拉菜单选择列
    prevent_initial_call=True
)
def traceability(column_value):
    try:
        # 根据选择的列进行数据筛选和可视化
        if column_value:
            fig = px.line(df, x='date', y=column_value, title=f'{column_value}溯源')
            return dcc.Graph(figure=fig)
        else:
            return html.Div('请选择一个列进行溯源')
    except Exception as e:
        return html.Div(f'发生错误：{str(e)}')

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
