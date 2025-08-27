# 代码生成时间: 2025-08-28 01:06:31
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from dash.exceptions import PreventUpdate
import plotly.express as px
import base64
import io

def generate_excel(dataframe, filename): # 函数用于生成Excel文件
    """Generate an Excel file from a Pandas DataFrame."""
    output = io.BytesIO()
    dataframe.to_excel(output, index=False)
    output.seek(0)
    return output

def excel_to_df(uploaded_file): # 函数用于将上传的Excel文件转换为DataFrame
    """Convert an uploaded Excel file to a Pandas DataFrame."""
    try:
        return pd.read_excel(uploaded_file)
    except Exception as e:
        print(e)
        raise PreventUpdate

def serve_layout(): # Dash应用布局函数
    app = dash.Dash(__name__)
    app.layout = html.Div(children=[
        html.H1(children='Excel Generator App'),
        html.P("Upload an Excel file to generate a new Excel file."),
        dcc.Upload(
            id='upload-data',
            children=html.Button('Upload'),
            multiple=False,
            # Allow only .xlsx files to be uploaded
            accept_extensions=['.xlsx', '.xls']
        ),
        html.Div(id='output-data-upload'),
    ])
    return app

def register_callbacks(app): # 注册回调函数
    @app.callback(
        Output('output-data-upload', 'children'),
        [Input('upload-data', 'contents')]
    )
    def update_output(contents): # 定义回调函数处理上传的文件
        if contents is None: # 如果没有上传文件，则不进行处理
            return None
        try:
            filename = contents.filename
            content_type, content_string = contents.split(',')[0], contents.split(',')[1]
            decoded = base64.b64decode(content_string)
            df = excel_to_df(io.BytesIO(decoded))
            output = generate_excel(df, filename)
            # 生成Excel文件的下载链接
            href = f'<a download="{filename}" href="data:application/vnd.ms-excel;base64,{base64.b64encode(output.getvalue()).decode()}">Download {filename}</a>'
            return href
        except Exception as e: # 错误处理
            return f'An error occurred: {str(e)}'

def main(): # 主函数
    app = serve_layout()
    register_callbacks(app)
    app.run_server(debug=True)

def __name__ == '__main__':
    main()