# 代码生成时间: 2025-08-01 06:58:39
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output

# 定义一个生成测试数据的函数
def generate_test_data(n_samples=100, n_features=5):
    """
    生成具有指定样本数和特征数的随机测试数据。
    
    参数:
    n_samples (int): 样本数量。
    n_features (int): 数据特征数量。
    
    返回:
    pd.DataFrame: 包含随机测试数据的DataFrame。
    """
    # 生成随机浮点数数据
    data = np.random.randn(n_samples, n_features)
    # 将numpy数组转换成pandas DataFrame
    df = pd.DataFrame(data, columns=[f'feature_{i}' for i in range(n_features)])
    return df

# 创建Dash应用
app = Dash(__name__)

# 定义应用布局
app.layout = html.Div([
    html.H1('Test Data Generator'),
    dcc.Input(id='n_samples', type='number', min=1, value=100,
         debounce=True),
    dcc.Input(id='n_features', type='number', min=1, value=5,
         debounce=True),
    html.Button('Generate Data', id='generate-button', n_clicks=0),
    dcc.Download(id='download-data'),
    dcc.Graph(id='data-visualization'),
])

# 定义回调函数以响应按钮点击
@app.callback(
    Output('data-visualization', 'figure'),
    Output('download-data', 'data'),
    Input('generate-button', 'n_clicks'),
    Input('n_samples', 'value'),
    Input('n_features', 'value'),
    prevent_initial_call=True
)
def generate_and_download(n_clicks, n_samples, n_features):
    # 错误处理，确保输入值有效
    if n_clicks is None or not isinstance(n_samples, int) or not isinstance(n_features, int):
        raise ValueError("Invalid input values.")

    # 生成测试数据
    test_data = generate_test_data(n_samples, n_features)

    # 创建数据可视化图
    fig = px.line(test_data)

    # 生成CSV文件内容
    csv_string = test_data.to_csv(index=False).encode('utf-8')

    return fig, dcc.send_data_frame(
        test_data.to_csv, "test_data.csv", index=False,
        as_string=True)

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)
