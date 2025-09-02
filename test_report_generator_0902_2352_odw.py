# 代码生成时间: 2025-09-02 23:52:15
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
from io import StringIO
from jinja2 import Template

# 定义Dash应用
app = dash.Dash(__name__)

# 定义应用布局
app.layout = html.Div([
    html.H1("测试报告生成器"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={"width": "100%", "height": "60px", "lineHeight": "60px","borderWidth": "1px", "borderStyle": "dashed", "borderRadius": "5px","textAlign": "center", "margin": "10px"},
        # 允许上传的文件类型
        accept=".csv, .xlsx, .xls"
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(id='test-report-graph'),
    html.Div(id='test-report')
])

# 定义回调函数处理上传的文件
@app.callback(
    Output('output-data-upload', 'children'), [
    Input('upload-data', 'contents')]
)
def update_output(contents):
    # 检查是否有文件上传
    if contents is None:
        return None
    else:
        # 读取文件内容
        filename = contents.split("\")[-1]
        print(f"文件：{filename}")
        # 根据文件类型进行处理
        if "csv" in filename:
            df = pd.read_csv(StringIO(contents.decode("utf-8")))
        elif "xlsx" in filename or "xls" in filename:
            df = pd.read_excel(StringIO(contents.decode("utf-8")))
        else:
            return "Unsupported file format"
        return f"文件 {filename} 已上传"

def generate_test_report(df):
    # 生成测试报告
    # 可以在这里添加报告生成的逻辑
    report_template = Template("""
    <html>
        <body>
            <h1>测试报告</h1>
            <p>测试数据汇总</p>
            {{ summary | safe }}
            {{ chart | safe }}
        </body>
    </html>
    """)
    # 计算数据总览
    summary = df.describe().to_html()
    # 生成图表
    chart = px.bar(df, x="测试项", y="测试结果").to_html(full_html=False)
    # 渲染报告模板
    report = report_template.render(summary=summary, chart=chart)
    return report
def on_data_uploaded(uploaded_filename):
    # 读取上传的文件并生成测试报告
    df = pd.read_csv(f"uploads/{uploaded_filename}")
    report = generate_test_report(df)
    return report
# 定义回调函数生成测试报告
@app.callback(
    Output('test-report', 'children'), [
    Input('upload-data', 'filename')]
)
def generate_test_report_callback(uploaded_filename):
    # 检查是否有文件上传
    if uploaded_filename is None:
        return None
    else:
        return on_data_uploaded(uploaded_filename)

def main():
    app.run_server(debug=True)

if __name__ == '__main__':
    main()