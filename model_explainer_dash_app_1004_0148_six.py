# 代码生成时间: 2025-10-04 01:48:24
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import plot_partial_dependence

# 初始化 Dash 应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div(children=[
    html.H1(children='模型解释工具'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
               'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
               'textAlign': 'center', 'margin': '10px'},
        # 允许上传.csv文件
        accept= ".csv"
    ),
    dcc.Graph(id='partial-dependence-plot'),
    dcc.Store(id='uploaded-data')
])

# 回调函数：处理上传数据
@app.callback(
    Output('uploaded-data', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(contents, filename, last_modified):
    if contents is not None:
        data = pd.read_csv(
            contents,
            filename=filename,
            skipinitialspace=True
        )
        return data.to_dict('records')
    raise PreventUpdate

# 回调函数：生成部分依赖图
@app.callback(
    Output('partial-dependence-plot', 'figure'),
    Input('uploaded-data', 'data')
)
def create_partial_dependence_plot(data):
    if data is not None:
        # 假设数据已经是适合的特征和目标变量
        df = pd.DataFrame(data)
        X, y = df.drop('target', axis=1), df['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        # 选择第一个特征生成部分依赖图
        feature_name = X.columns[0]
        pdp_fig = px.line(
            plot_partial_dependence(model, X_train, features=[0], grid_resolution=50),
            x=df[feature_name].min(), y=df[feature_name].max(),
            labels={'x': feature_name, 'y': 'Partial dependence', 'color': 'feature'}
        )
        pdp_fig.update_layout(title='Partial Dependence Plot')
        return pdp_fig
    return dash.no_update

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)
