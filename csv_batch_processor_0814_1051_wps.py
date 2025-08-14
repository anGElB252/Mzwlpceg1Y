# 代码生成时间: 2025-08-14 10:51:52
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

# 定义应用
app = dash.Dash(__name__)

# 定义布局
app.layout = html.Div([
    html.H1("CSV文件批量处理器"),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    dcc.Button(
        id='process-button',
        children='Process Files',
        n_clicks=0
    ),
    html.Div(id='output-container')
])

# 回调函数，用于处理上传的文件
@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    State('upload-data', 'size')
)
def update_output(*args):
    if args[0] is not None:
        return [
            html.P(f'Filename: {args[1]}'),
            html.P(f'Last Modified: {args[2]}'),
            html.P(f'Size: {args[3]} bytes')
        ]
    else:
        return 'No file is selected yet.'

# 回调函数，用于处理文件并显示结果
@app.callback(
    Output('output-container', 'children'),
    Input('process-button', 'n_clicks'),
    State('upload-data', 'contents')
)
def process_files(n_clicks, uploaded_files):
    if n_clicks > 0 and uploaded_files is not None:
        # 确保文件已经上传
        if len(uploaded_files) > 0:
            try:
                # 读取第一个文件
                file = uploaded_files[0]
                df = pd.read_csv(file['content_type'], compression=None,
                                  storage_options=None,
                                  engine=None,
                                  index_col=None, 
                                  delim_whitespace=None, 
                                  na_filter=True,
                                  escapechar=None, 
                                  encoding=None, 
                                  low_memory=True, 
                                  memory_map=False, 
                                  float_precision=None,
                                  columns=None, 
                                  chunksize=None,
                                  verbose=False, 
                                  dtype=None, 
                                  converterd=None, 
                                  skipinitialspace=True, 
                                  skiprows=None, 
                                  skipfooter=None, 
                                  header=None, 
                                  names=None, 
                                  parse_dates=False, 
                                  date_parser=None, 
                                  dayfirst=False, 
                                  thousands=None, 
                                  decimal='.', 
                                  lineterminator=None, 
                                  chunksize=None, 
                                  iterator=False, 
                                  get_dummy_dates=False, 
                                  has_index_names=None, 
                                  tupleize_cols=None, 
                                  quoting=None, 
                                  doublequote=None, 
                                  escapechar=None, 
                                  comment=None, 
                                  encoding=None, 
                                  dialect=None, 
                                  on_bad_lines=None)

                # 显示处理后的结果
                return html.Div([
                    html.H2("Processed Data"),
                    dcc.Table(
                        id='table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records')
                    )
                ])
            except Exception as e:
                # 错误处理
                return f'Error processing files: {str(e)}'
        else:
            return 'No files selected to process.'
    return 'No files have been uploaded yet.'

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
