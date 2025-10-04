# 代码生成时间: 2025-10-05 03:46:20
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
# 改进用户体验
import datetime
# 扩展功能模块
import schedule
import time

# 定义调度器任务函数
def scheduled_job():
    """示例任务：打印当前时间"""
    print("Scheduled job: ", datetime.datetime.now())

# 定义Dash应用
app = dash.Dash(__name__)

# 布局Dash应用
app.layout = html.Div([
    html.H1("定时任务调度器"),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # 1秒刷新一次
# 改进用户体验
        n_intervals=0
    ),
    html.Div(id='live-update-text')
# 改进用户体验
])

# 定时任务调度
schedule.every(1).seconds.do(scheduled_job) # 每秒执行一次
# NOTE: 重要实现细节

# Dash回调，用于更新页面显示时间
@app.callback(Output('live-update-text', 'children'), [Input('interval-component', 'n_intervals')])
def update_metrics(n):
# 优化算法效率
    """
    更新页面文本以显示当前时间。
    :param n: 从Interval组件传递的n_intervals参数
    :return: 当前时间的字符串表示"""
    return '当前时间：' + datetime.datetime.now().strftime("%H:%M:%S")

# 运行定时任务
if __name__ == '__main__':
    try:
        # 在后台线程中运行定时任务
        import threading
        thread = threading.Thread(target=schedule.run_pending)
        thread.start()
        
        # 启动Dash应用
        app.run_server(debug=True)
    except Exception as e:
        print("发生错误: ", str(e))
