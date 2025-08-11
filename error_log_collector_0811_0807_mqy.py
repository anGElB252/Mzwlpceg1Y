# 代码生成时间: 2025-08-11 08:07:47
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import logging
import logging.handlers
import os
from datetime import datetime

# 设置日志格式
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# 配置日志文件
log_filename = 'error_log.txt'
if not os.path.exists(log_filename):
    with open(log_filename, 'w') as f:
        f.write('')
logger = logging.getLogger('error_logger')
logger.setLevel(logging.ERROR)

# 配置日志文件处理器
file_handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=100000, backupCount=10)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(file_handler)

# 定义Dash应用
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Error Log Collector'),
    dcc.Input(id='log-input', type='text', placeholder='Enter log message'),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='log-output')
])

# 回调函数，处理提交的日志消息
@app.callback(
    Output('log-output', 'children'),
    Input('submit-button', 'n_clicks'),
    State('log-input', 'value')
)
def submit_log(n_clicks, log_message):
    if n_clicks > 0 and log_message:
        try:
            # 将日志信息写入文件
            with open(log_filename, 'a') as f:
                f.write(f'
{log_message}
')
            # 将日志信息添加到滚动日志处理器
            logger.error(log_message)
            # 返回提交成功的信息
            return 'Log submitted successfully!'
        except Exception as e:
            # 异常处理，记录错误信息
            logger.error(f'Error submitting log: {str(e)}')
            # 返回错误信息
            return f'Error submitting log: {str(e)}'
    # 如果没有点击提交或日志消息为空，返回空字符串
    return ''

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)