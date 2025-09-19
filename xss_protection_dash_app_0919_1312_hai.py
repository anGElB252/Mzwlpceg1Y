# 代码生成时间: 2025-09-19 13:12:08
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from bs4 import BeautifulSoup
import bleach

# 定义允许的HTML标签
ALLOWED_TAGS = ['b', 'i', 'u', 'p', 'a', 'br', 'div', 'span', 'em', 'strong', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

# 定义允许的属性
ALLOWED_ATTRIBUTES = {
    '*': ['class', 'style'],
    'a': ['href', 'title'],
    'img': ['src', 'alt']
}

# 定义允许的样式
ALLOWED_STYLES = ['color', 'font-size', 'font-weight', 'text-decoration']

# 创建Dash应用
app = dash.Dash(__name__)

# 定义路由
app.layout = html.Div([
    dbc.Container([
        html.H1("XSS Attack Prevention"),
        html.P("Enter your input below:"),
        dcc.Input(id='input', type='text', value='', placeholder='Type your text here...'),
        html.Button('Submit', id='submit-button', n_clicks=0),
        html.Div(id='output-container', children=[]),
    ]),
], className='app-container')

# 定义回调函数处理提交的数据
@app.callback(
    Output("output-container", "children"),
    [Input("submit-button", "n_clicks"), Input("input", "value")],
    [State("input", "value")]
)
def submit_button_click(n_clicks, value):
    """
    处理提交的数据，进行XSS防护。
    :param n_clicks: 按钮点击次数
    :param value: 用户输入的文本
    :return: 处理后的文本
    """
    if n_clicks > 0:
        try:
            # 使用BeautifulSoup解析文本
            soup = BeautifulSoup(value, 'html.parser')
            """
            清除所有标签
            """
            for element in soup.find_all():
                element.replace_with(element.text)
            """
            使用bleach清洗文本，只保留允许的标签和属性
            """
            clean_text = bleach.clean(
                soup.prettify(),
                tags=ALLOWED_TAGS,
                attributes=ALLOWED_ATTRIBUTES,
                styles=ALLOWED_STYLES
            )
            # 返回处理后的文本
            return html.Div([html.P("Processed Output:"), html.Pre(clean_text)])
        except Exception as e:
            # 出错时返回错误信息
            return html.Div([html.P("Error processing input: " + str(e))])
    return html.Div([])

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)