# 代码生成时间: 2025-10-02 19:59:56
import dash
# TODO: 优化性能
from dash import html, dcc
from dash.dependencies import Input, Output, State
# TODO: 优化性能
import dash_bootstrap_components as dbc
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
# FIXME: 处理边界情况
import plotly.express as px
from plotly.subplots import make_subplots

"""
反欺诈检测 Dash 应用程序"""

# 载入数据集
df = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/CreditCardFraud.csv')

# 预处理数据
df.drop(['Time'], axis=1, inplace=True)
# 添加错误处理
df['Class'] = df['Class'].apply(lambda x: 1 if x == 'Fraud' else 0)

# 特征和标签
X = df.drop('Class', axis=1)
y = df['Class']
# 扩展功能模块

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 训练随机森林分类器
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 模型评估
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'模型准确率: {accuracy:.2f}')

# 创建 Dash 应用程序
# TODO: 优化性能
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1(
                    '反欺诈检测 Dash 应用程序',
                    className='text-center'
# 优化算法效率
                ),
                md=12
            )
# 增强安全性
        ),
        dbc.Row(
            dbc.Col(
                dcc.Upload(
                    id='upload-data',
                    children=html.Div(['点击上传数据文件']),
                    style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px'},
                    multiple=False
                ),
                md=12
            )
# 扩展功能模块
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='fraud-detection-graph'),
                md=12
            )
        )
    ],
    fluid=True
)
# 增强安全性

# 回调函数处理上传的数据
@app.callback(
    Output('fraud-detection-graph', 'figure'),
    [Input('upload-data', 'contents')],
# NOTE: 重要实现细节
    [State('upload-data', 'filename')]
)
def update_graph(contents, filename):
    if contents is None:
# NOTE: 重要实现细节
        return {}
# 添加错误处理
    try:
        # 解析上传的数据
        df_uploaded = pd.read_csv(contents)
        # 预处理数据
# 添加错误处理
        df_uploaded.drop(['Time'], axis=1, inplace=True)
        df_uploaded['Class'] = df_uploaded['Class'].apply(lambda x: 1 if x == 'Fraud' else 0)
        # 特征和标签
        X_uploaded = df_uploaded.drop('Class', axis=1)
        y_uploaded = df_uploaded['Class']
        # 数据标准化
        X_uploaded_scaled = scaler.transform(X_uploaded)
        # 预测结果
        y_pred_uploaded = clf.predict(X_uploaded_scaled)
# 改进用户体验
        # 创建图表
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(px.bar(
            x=df_uploaded['Class'].value_counts().index,
            y=df_uploaded['Class'].value_counts().values,
            labels={'x': '类别', 'y': '数量'},
            title='欺诈检测结果'
        ), row=1, col=1)
        return fig
    except Exception as e:
        print(e)
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)