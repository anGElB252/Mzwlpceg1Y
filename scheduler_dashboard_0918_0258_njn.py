# 代码生成时间: 2025-09-18 02:58:10
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import threading

# 初始化Dash应用
app = dash.Dash(__name__)

# 定义定时任务调度器
scheduler = BackgroundScheduler()
scheduler.start()

# 定义定时任务列表
tasks = []

def add_task(interval, func):
    """添加定时任务到调度器"""
    job = scheduler.add_job(func, 'interval', seconds=interval, id=str(len(tasks)))
    tasks.append(job)


def remove_task(job_id):
    """从调度器中移除定时任务"""
    for job in tasks:
        if job.id == job_id:
            job.remove()
            tasks.remove(job)
            break

# 定义布局
app.layout = html.Div([
    html.H1("定时任务调度器"),
    html.Div([
        dcc.Input(id='task-interval', type='number', placeholder='输入任务间隔时间（秒）'),
        dcc.Button('添加任务', id='add-task-button', n_clicks=0),
    ]),
    html.Div(id='task-list'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        disabled=False,
    ),
])

# 定义回调函数，添加任务
@app.callback(
    Output('task-list', 'children'),
    [Input('add-task-button', 'n_clicks')],
    [State('task-interval', 'value')]
)
def add_task_callback(n_clicks, interval):
    if not interval:
        return '请输入任务间隔时间'
    try:
        interval = int(interval)
    except ValueError:
        return '请输入有效的间隔时间'
    if n_clicks:
        add_task(interval, lambda: print(f'任务执行于: {datetime.datetime.now()}'))
        return f'任务已添加，间隔时间: {interval} 秒'
    return ''

# 定义回调函数，移除任务
@app.callback(
    Output('task-list', 'children'),
    [Input('interval-component', 'n_clicks')]
)
def update_output(n_clicks):
    task_list = ''
    for i, job in enumerate(tasks):
        task_list += f'任务{i}: 间隔时间: {job.interval} 秒, 状态: {job.state}<br>'
    return task_list

# 定义回调函数，移除指定任务
@app.callback(
    Output('task-list', 'children'),
    [Input('remove-task-button', 'n_clicks')],
    [State('task-list', 'children')]
)
def remove_task_callback(n_clicks, task_list):
    if n_clicks:
        job_id = n_clicks
        remove_task(job_id)
        return '任务已移除'
    return task_list

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)
