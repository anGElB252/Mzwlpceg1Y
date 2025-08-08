# 代码生成时间: 2025-08-09 01:02:32
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# 定义全局变量
SEARCH_DATA = pd.DataFrame({'Name': ['Eve', 'John', 'Jim', 'Jane'], 'Age': [25, 35, 45, 55], 'Country': ['USA', 'France', 'UK', 'Canada']})

# 创建Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div(children=[
    html.H1(children='Search Optimization Example'),
    dcc.Input(id='search-input', type='text', placeholder='Search...', style={'margin': '20px', 'width': '80%'}),
    html.Div(id='search-results'),
])

# 回调函数：搜索结果
@app.callback(
    Output('search-results', 'children'),
    [Input('search-input', 'value')]
)
def search_results(query):
    # 搜索结果的空列表
    results = []
    # 检查查询字符串
    if query:
        # 将查询字符串转换为小写
        query = query.lower()
        # 过滤数据集
        filtered_df = SEARCH_DATA[SEARCH_DATA.apply(lambda row: query in row.astype(str).str.lower(), axis=1)]
        # 将搜索结果转换为列表并返回
        results = filtered_df.to_dict(orient='records')
    # 返回搜索结果的数量和结果列表
    return html.Div([html.H3(f'{len(results)} results found'), html.Ul([html.Li([f'Name: {item[