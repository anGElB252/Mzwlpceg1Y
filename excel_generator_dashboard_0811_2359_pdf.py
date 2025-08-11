# 代码生成时间: 2025-08-11 23:59:08
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from dash.exceptions import PreventUpdate

# 主函数
def generate_excel_table(app: dash.Dash, layout: html.Div):
    # 定义Dash应用
    app.layout = layout

    # 定义回调函数，当表单数据更新时触发
    @app.callback(
        Output('output-table', 'data'),
        [Input('input-range', 'value'), Input('input-number', 'value')],
        prevent_initial_call=True
    )
    def generate_table(number_of_rows, number_of_columns):
        
        try:
            # 检查输入参数，确保它们是整数
            if not isinstance(number_of_rows, int) or not isinstance(number_of_columns, int):
                raise ValueError("Input values must be integers.")

            # 生成Excel表格数据
            df = pd.DataFrame(np.random.randn(number_of_rows, number_of_columns), 
                             columns=["Column {}".format(i) for i in range(number_of_columns)])

            # 将DataFrame转换为Excel文件
            excel_buffer = pd.ExcelWriter(pd.ExcelFile("empty_file.xlsx"), engine="openpyxl")
            df.to_excel(excel_buffer, index=False)
            excel_buffer.save("output_file.xlsx")

            # 将文件存储在一个字典中，以便Dash可以下载
            return [
                {
                    "name": "output_file.xlsx",
                    "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                }
            ]
        except ValueError as e:
            # 捕获值错误并返回错误信息
            return [
                {
                    "name": "error_file.xlsx",
                    "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "data": str(e)
                }
            ]
        except Exception as e:
            # 捕获其他异常并返回错误信息
            return [
                {
                    "name": "error_file.xlsx",
                    "type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "data": str(e)
                }
            ]

    # 定义下载回调
    @app.callback(
        Output('download-link', 'href'),
        [Input('output-table', 'data')],
    )
    def download_link(filedata):
        if filedata is None:
            raise PreventUpdate
        return filedata[0]['name']

# 创建Dash应用
app = dash.Dash(__name__)

# 定义应用布局
app.layout = html.Div(children=[
    html.H1(children='Excel Table Generator Dashboard'),
    html.Div(children=[
        'Number of Rows: ',
        dcc.Input(id='input-range', type='number', value=10, min=1),
    ]),
    html.Div(children=[
        'Number of Columns: ',
        dcc.Input(id='input-number', type='number', value=5, min=1),
    ]),
    dcc.Download(id='download-link'),
    dcc.Download(id='download-link-error'),
    dcc.DataTable(
        id='output-table',
        download=True,
        filter_action="download",
        sort_action="download",
        sort_mode="multi",
        column_selectable=False,
        row_selectable='multi',
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    )
])

# 调用主函数
generate_excel_table(app, app.layout)

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)