# 代码生成时间: 2025-08-17 03:53:13
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os

# 数据库配置
DB_PATH = 'database.db'
DB_ENGINE = create_engine('sqlite:///' + DB_PATH)
Session = sessionmaker(bind=DB_ENGINE)

# 定义Dash应用
app = dash.Dash(__name__)

# 默认路由
app.layout = html.Div([
    html.H1('Secure SQL Dashboard'),
    dcc.Input(id='input-text', type='text', placeholder='Enter your text here...'),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output-container')
])

# 回调函数，防止SQL注入
@app.callback(
    Output('output-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input-text', 'value')
])
def process_input(n_clicks, value):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    try:
        session = Session()
        # 使用参数化查询防止SQL注入
        query = 'SELECT * FROM users WHERE name = :name'
        result = session.execute(query, {'name': value}).fetchall()
        session.close()
        # 处理查询结果
        return f'Results: {result}'
    except SQLAlchemyError as e:
        return f'An error occurred: {e}'

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
