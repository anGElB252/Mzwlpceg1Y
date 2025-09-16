# 代码生成时间: 2025-09-16 22:50:07
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# 定义排序算法函数
def bubble_sort(arr):
# 优化算法效率
    n = len(arr)
    for i in range(n):  # 遍历所有数组元素
# 添加错误处理
        for j in range(0, n-i-1):  # 最后i个元素已经是排好序的了
            if arr[j] > arr[j+1]:  # 相邻元素两两比较
                arr[j], arr[j+1] = arr[j+1], arr[j]  # 元素交换
# TODO: 优化性能
    return arr
# FIXME: 处理边界情况

def selection_sort(arr):
# 添加错误处理
    n = len(arr)
    for i in range(n):  # 遍历数组
        min_idx = i  # 假设当前位置为最小值
        for j in range(i+1, n):  # 从当前位置的下一个元素开始比较
            if arr[min_idx] > arr[j]:  # 找到最小元素
                min_idx = j  # 更新最小元素的索引
        arr[i], arr[min_idx] = arr[min_idx], arr[i]  # 交换位置
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):  # 从第二个元素开始遍历
        key = arr[i]  # 待插入元素
# 增强安全性
        j = i-1  # 需要插入的位置
# 扩展功能模块
        while j >= 0 and key < arr[j]:  # 寻找插入位置
            arr[j+1] = arr[j]  # 元素向右移动
            j -= 1  # 更新位置
# 增强安全性
        arr[j+1] = key  # 插入元素
    return arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        # 分治递归排序两个子序列
        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        # 合并排序后的子序列
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
# NOTE: 重要实现细节
                j += 1
            k += 1
# 扩展功能模块

        while i < len(L):
            arr[k] = L[i]
            i += 1
# FIXME: 处理边界情况
            k += 1

        while j < len(R):
            arr[k] = R[j]
# 改进用户体验
            j += 1
            k += 1

    return arr
# NOTE: 重要实现细节

# 定义Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div([
    html.H1('排序算法可视化'),
    dcc.Dropdown(
# 扩展功能模块
        id='algorithm-dropdown',
        options=[
            {'label': '冒泡排序', 'value': 'bubble'},
            {'label': '选择排序', 'value': 'selection'},
            {'label': '插入排序', 'value': 'insertion'},
            {'label': '归并排序', 'value': 'merge'}
# 添加错误处理
        ],
        value='bubble'
    ),
    dcc.Graph(id='sort-graph'),
# NOTE: 重要实现细节
    dcc.Input(id='input-array', type='text', placeholder='输入数组，用逗号分隔',
               debounce=True),
    html.Button('排序', id='sort-button', n_clicks=0),
])
# NOTE: 重要实现细节

# 回调函数：根据选择的算法和输入数组，更新图表
@app.callback(
    Output('sort-graph', 'figure'),
    [Input('algorithm-dropdown', 'value'),
# 优化算法效率
     Input('input-array', 'value'),
     Input('sort-button', 'n_clicks')],
    [State('sort-graph', 'figure')]
)
def update_graph(algorithm, array_str, n_clicks, figure):
# 改进用户体验
    if n_clicks == 0 or not array_str:
        raise dash.exceptions.PreventUpdate()

    # 解析输入数组
    try:
        arr = list(map(float, array_str.split(',')))
    except ValueError:
        return {'data': [{'x': [], 'y': [], 'type': 'scatter',
                     'mode': 'lines'}]}  # 返回空图表

    # 根据选择的算法进行排序
    if algorithm == 'bubble':
        sorted_arr = bubble_sort(arr.copy())
    elif algorithm == 'selection':
        sorted_arr = selection_sort(arr.copy())
    elif algorithm == 'insertion':
        sorted_arr = insertion_sort(arr.copy())
    elif algorithm == 'merge':
# 优化算法效率
        sorted_arr = merge_sort(arr.copy())
    else:
        return {'data': [{'x': [], 'y': [], 'type': 'scatter',
# 增强安全性
                     'mode': 'lines'}]}  # 返回空图表

    # 创建图表
    steps = [arr]
    for i in range(len(arr)-1):
        steps.append(np.roll(steps[-1], -1))
# FIXME: 处理边界情况

    fig = make_subplots(rows=len(steps), cols=1)
# TODO: 优化性能
    for i, step in enumerate(steps):
        fig.add_trace(px.line(x=list(range(len(step))), y=step),
                     row=i+1, col=1)

    fig.update_layout(height=800, title=f'{algorithm} 排序过程')
    return fig

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)