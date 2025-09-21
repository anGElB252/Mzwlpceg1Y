# 代码生成时间: 2025-09-21 22:58:43
import dash\
import dash_core_components as dcc\
import dash_html_components as html\
import pandas as pd\
from dash.dependencies import Input, Output, State\
import plotly.express as px\
import base64\
from io import BytesIO\
import openpyxl\
from openpyxl.utils.dataframe import dataframe_to_rows\
from dash.exceptions import PreventUpdate\
\
# 定义全局变量保存DataFrame\
df = pd.DataFrame()\
\
app = dash.Dash(__name__)\
app.layout = html.Div([\
    html.H1("Excel表格自动生成器"),\
    dcc.Upload(\
        id='upload-data',\
        children=html.Div([html.Button('上传Excel文件'), html.Span(id='upload-data-text')],\
        style={
            'width': '50%',\
            'height': '60px',\
            'lineHeight': '60px',\
            'borderWidth': '1px',\
            'borderStyle': 'dashed',\
            'textAlign': 'center',\
            'margin': '10px'\
        },\
        # 允许上传的文件类型\
        accept='.xlsx'\
    ),\
    dcc.Download(id='download-button'),\
    dcc.Graph(id='excel-graph'),\
])\
\
# 回调：当上传文件时生成表格和图表\
@app.callback(\
   Output('excel-graph', 'figure'),\
   Output('download-button', 'href'),\
   Output('download-button', 'download'),\
   Input('upload-data', 'contents'),\
   State('upload-data', 'filename'),\
)\
def update_output(contents, filename):
    if contents is None:
        raise PreventUpdate  # 没有上传文件时不更新
    
    # 读取Excel文件并转换为DataFrame
    try:
        df = pd.read_excel(BytesIO(contents))
    except Exception as e:
        print(f"读取Excel文件错误：{e}")
        raise PreventUpdate
    
    # 生成图表
    fig = px.data_frame(df)
    
    # 保存DataFrame到Excel文件
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        writer.save()
        output.seek(0)
        
    download_link = f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{base64.b64encode(output.getvalue()).decode()}"
    return fig, download_link, filename

# 回调：更新上传文件信息
@app.callback(Output('upload-data-text', 'children'), Input('upload-data', 'contents'))
def update_output_div(contents):
    if contents is None:
        return 'No file yet'
    return f'文件名称：{(contents.get('filename') or 