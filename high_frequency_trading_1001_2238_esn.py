# 代码生成时间: 2025-10-01 22:38:50
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from threading import Thread

"""
High Frequency Trading System using Dash
"""

# Define the app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div(children=[
    html.H1(children='High Frequency Trading System'),
    dcc.Dropdown(id='stock-dropdown', options=[{'label': i, 'value': i} for i in yf.tickers],
                placeholder='Select a stock...'),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    ),
])

"""
Function to fetch stock data
"""
def fetch_stock_data(stock_symbol):
    return yf.download(stock_symbol, period='1d')

"""
Callback function to update the graph
"""
@app.callback(Output('live-update-graph', 'figure'), [Input('interval-component', 'n_intervals')],
              [State('stock-dropdown', 'value')])
def update_graph_live(n, stock_symbol):
    if stock_symbol:
        try:
            df = fetch_stock_data(stock_symbol)
            fig = px.line(df, x='Close', y=df.index, title=f'{stock_symbol} Stock Price')
            return fig
        except Exception as e:
            return {'layout': {'annotations': [dict(text=f'Error: {str(e)}', x=0.5, y=0.5,
                                                xref='paper', yref='paper', showarrow=False)]}}
    return dash.no_update

"""
Thread to run the app
"""
def run_app(server):
    server.run_forever()

"""
Main function
"""
if __name__ == '__main__':
    # Start Flask server in a separate thread
    Thread(target=run_app, args=(app.server,)).start()
    # Start Dash app
    app.run_server(host='127.0.0.1', port=8050, debug=True)
