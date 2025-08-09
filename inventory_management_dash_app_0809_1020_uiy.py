# 代码生成时间: 2025-08-09 10:20:31
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from dash.exceptions import PreventUpdate

# 库存管理系统的URL
SERVER_URL = 'http://127.0.0.1:8050/'

# 定义库存数据
inventory_data = pd.DataFrame(columns=['ID', 'Product Name', 'Quantity', 'Price'])

# 初始化Dash应用
app = dash.Dash(__name__, server=app.server, url_base_pathname='/inventory/', external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# 应用布局
app.layout = html.Div(
    children=[
        html.H1('Inventory Management System'),
        html.Div('Enter Product ID'),
        dbc.Input(id='product-id-input', placeholder='Enter Product ID', type='text'),
        dbc.Button('Add Product', id='add-product-button', n_clicks=0, className='me-2'),
        dbc.Button('Remove Product', id='remove-product-button', n_clicks=0, className='me-2'),
        html.Div(id='product-list'),
        html.Div(id='table'),
    ],
    style={'textAlign': 'center'}
)

# 回调函数 - 添加产品
@app.callback(
    Output('product-list', 'children'),
    [Input('add-product-button', 'n_clicks')],
    [State('product-id-input', 'value')],
)
def add_product(n_clicks, product_id):
    if n_clicks is None or product_id is None:  # 避免初始加载时的更新
        raise PreventUpdate
    try:
        new_product = pd.DataFrame({'ID': [product_id], 'Product Name': ['New Product'], 'Quantity': [0], 'Price': [0.0]}, index=[0])
        inventory_data = pd.concat([inventory_data, new_product])
        return f'Product {product_id} added successfully.'
    except Exception as e:
        return f'Failed to add product: {e}'

# 回调函数 - 删除产品
@app.callback(
    Output('product-list', 'children'),
    [Input('remove-product-button', 'n_clicks')],
    [State('product-id-input', 'value')],
)
def remove_product(n_clicks, product_id):
    if n_clicks is None or product_id is None:  # 避免初始加载时的更新
        raise PreventUpdate
    try:
        inventory_data = inventory_data[inventory_data['ID'] != product_id]
        return f'Product {product_id} removed successfully.'
    except Exception as e:
        return f'Failed to remove product: {e}'

# 回调函数 - 更新表格视图
@app.callback(
    Output('table', 'children'),
    [Input('product-list', 'children')],
)
def update_table(children):
    return html.Table(
        [html.Thead(html.Tr([html.Th(col) for col in inventory_data.columns]))] +
        [html.Tbody([html.Tr([html.Td(cell) for cell in row]) for row in inventory_data.values])]
    )

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
