# 代码生成时间: 2025-08-19 02:20:55
import requests
from bs4 import BeautifulSoup
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import urllib.parse

# 定义一个函数用于抓取网页内容
def fetch_web_content(url):
    try:
        # 发送请求
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.prettify()  # 返回格式化的HTML内容
    except requests.RequestException as e:
        # 处理请求异常
        return f"An error occurred: {e}"

# 定义Dash应用
app = dash.Dash(__name__)

# 设置布局
app.layout = html.Div(
    children=[
        dcc.Input(id=\