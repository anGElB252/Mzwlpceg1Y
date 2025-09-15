# 代码生成时间: 2025-09-16 01:19:41
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

# 购物车内商品的数据，简化为一个列表，每个商品为一个字典
SHOPPING_CART = []

# 可用商品的列表
ITEMS = [
    {"id": 1, "name": "Apple", "price": 1.50},
    {"id": 2, "name": "Banana", "price": 0.50},
    {"id": 3, "name": "Cherry", "price": 2.00},
]

# 购物车应用
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Shopping Cart"),
    html.Ul([
        html.Li(
            html.Div([
                html.P(f"{item['name']} - ${item['price']:.2f}"),
                html.Button("Add to Cart", id=f"add-to-cart-{item['id']}", n_clicks=0),
                html.Button("Remove from Cart", id=f"remove-from-cart-{item['id']}", n_clicks=0),
            ], style={"display": "flex", "justifyContent": "space-between"}),
            id=f"item-{item['id']}",
        ) for item in ITEMS
    ]),
    html.Hr(),
    html.H2("Cart"),
    html.Ul(id="cart-items"),
])

# 回调函数，添加商品到购物车
@app.callback(
    Output("cart-items", "children"),
    [Input(f"add-to-cart-{i}", "n_clicks") for i in range(1, len(ITEMS) + 1)],
    [State("cart-items", "children"), State("SHOPPING_CART", "data")]
)
def add_to_cart(n_clicks, cart_items, shopping_cart):
    if not n_clicks:
        raise PreventUpdate
    item_id = int(n_clicks.args[0].split("-")[2])
    if item_id in [item['id'] for item in shopping_cart]:
        return cart_items
    item = next((item for item in ITEMS if item['id'] == item_id), None)
    if item:
        shopping_cart.append(item)
        return html.Ul([html.Li(html.P(f"{item['name']} - ${item['price']:.2f} ({item['id']})"))] + [html.Li(child) for child in cart_items])
    else:
        return cart_items

# 回调函数，从购物车中移除商品
@app.callback(
    Output("cart-items", "children"),
    [Input(f"remove-from-cart-{i}", "n_clicks") for i in range(1, len(ITEMS) + 1)],
    [State("cart-items", "children"), State("SHOPPING_CART", "data"), State("SHOPPING_CART", "modified_timestamp")]
)
def remove_from_cart(n_clicks, cart_items, shopping_cart, modified_timestamp):
    if not n_clicks:
        raise PreventUpdate
    item_id = int(n_clicks.args[0].split("-")[2])
    if item_id not in [item['id'] for item in shopping_cart]:
        return cart_items
    shopping_cart = [item for item in shopping_cart if item['id'] != item_id]
    return html.Ul([html.Li(child) for child in cart_items if not child.endswith(str(item_id))])

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)