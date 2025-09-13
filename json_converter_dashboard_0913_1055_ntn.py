# 代码生成时间: 2025-09-13 10:55:27
import json
from dash import Dash, html, dcc, Input, Output

# 创建Dash应用
app = Dash(__name__)

# 应用布局
app.layout = html.Div([
    html.H1("JSON数据格式转换器"),
    dcc.Textarea(
        id='json-input',
        placeholder='输入JSON数据...',
        style={'width': '600px', 'height': '200px'},
    ),
    html.Button('转换', id='convert-button', n_clicks=0),
    html.Div(id='json-output'),
])

# 回调函数，处理JSON转换
@app.callback(
    Output('json-output', 'children'),
    [Input('convert-button', 'n_clicks')],
    prevent_initial_call=True,
)
def convert_json(n_clicks):
    # 获取输入的JSON数据
    try:
        input_json = json.loads(dash.callback_context.inputs_list[0].value)
    except json.JSONDecodeError:
        return '输入的不是有效的JSON格式！'
    except Exception as e:
        return f'发生错误：{str(e)}'

    # 尝试将JSON数据转换为Python对象
    try:
        python_object = json.dumps(input_json, indent=4)
    except Exception as e:
        return f'转换错误：{str(e)}'

    # 返回转换结果
    return html.Pre(python_object)

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)