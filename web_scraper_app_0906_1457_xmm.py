# 代码生成时间: 2025-09-06 14:57:28
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 定义一个函数来抓取和解析网页内容
def scrape_web_content(url):
    try:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        # 检查请求是否成功
        response.raise_for_status()
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 提取网页的标题和内容
        title = soup.title.string if soup.title else 'No title found'
        content = soup.get_text()
        return {'title': title, 'content': content}
    except requests.RequestException as e:
        # 处理请求异常
        return {'error': str(e)}
    except Exception as e:
        # 处理其他异常
        return {'error': 'An error occurred: ' + str(e)}

# 创建Dash应用
app = dash.Dash(__name__)

# 定义应用布局
app.layout = html.Div([
    dcc.Input(id='url-input', type='text', placeholder='Enter a URL here', value='https://example.com'),
    html.Button('Scrape', id='scrape-button', n_clicks=0),
    dcc.Markdown(id='web-content'),
])

# 定义回调函数来处理按钮点击事件
@app.callback(
    Output('web-content', 'children'),
    [Input('scrape-button', 'n_clicks')],
    [State('url-input', 'value')]
)
def scrape_content(n_clicks, url):
    # 检查按钮是否被点击
    if n_clicks > 0:
        # 抓取网页内容
        result = scrape_web_content(url)
        # 根据结果生成Markdown格式的输出
        if 'error' in result:
            return f'Error: {result[