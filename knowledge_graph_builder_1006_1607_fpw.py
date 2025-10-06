# 代码生成时间: 2025-10-06 16:07:43
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import networkx as nx
import pandas as pd

# 定义一个函数来加载和处理数据
def load_and_process_data():
    # 这里只是一个示例，实际应用中需要加载和处理你的数据
    # 假设我们有一个简单的知识图谱数据集
    data = {
        'source': ['A', 'B', 'C', 'D'],
        'target': ['B', 'C', 'D', 'A'],
        'value': [1, 2, 3, 4]
    }
    df = pd.DataFrame(data)
    return df

# 创建一个Dash应用
app = dash.Dash(__name__)

# 定义应用布局
app.layout = html.Div(children=[
    html.H1(children='知识图谱构建'),
    dcc.Graph(id='knowledge-graph'),
])

# 定义回调函数来更新图表
@app.callback(
    Output('knowledge-graph', 'figure'),
    [Input('knowledge-graph', 'id')]
)
def update_graph(input_id):
    try:
        # 加载和处理数据
        df = load_and_process_data()

        # 创建一个NetworkX图
        edges = df[['source', 'target']].values.tolist()
        G = nx.DiGraph()
        G.add_edges_from(edges)

        # 使用Plotly Express创建图表
        fig = px.line_networkx(G, x=df['source'], y=df['target'],
                              edge_color=df['value'],
                              size=df['value'],
                              color_continuous_scale='Viridis')
        fig.update_layout(title='知识图谱', margin=dict(t=0, l=0, r=0, b=0))
        return fig
    except Exception as e:
        print(f"发生错误: {e}")
        return {'data': [{'x': [], 'y': [], 'type': 'scatter', 'mode': 'lines'}]}

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
