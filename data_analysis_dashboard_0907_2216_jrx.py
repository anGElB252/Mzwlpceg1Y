# 代码生成时间: 2025-09-07 22:16:54
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate

# 定义数据分析器应用
class DataAnalysisDashboard:
    def __init__(self, dataframe):
        """
        构造函数，初始化Dash应用并设置数据源。
        :param dataframe: 包含待分析数据的Pandas DataFrame。
        """
        self.app = dash.Dash(__name__)
        self.dataframe = dataframe
        self.layout = self.create_layout()

    def create_layout(self):
        """
        创建Dash应用的布局。
        """
        return html.Div([
            html.H1("数据分析器"),
            dcc.Dropdown(
                id='column-selector',
                options=[{'label': col, 'value': col} for col in self.dataframe.columns],
                value=['所有列'],
                multi=True
            ),
            dcc.Graph(id='data-graphic'),
            dcc.RadioItems(
                id='chart-type-selector',
                options=[{'label': '柱状图', 'value': 'bar'},
                         {'label': '折线图', 'value': 'line'},
                         {'label': '散点图', 'value': 'scatter'}],
                value='bar',
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Checklist(
                id='filter',
                options=[{'label': '过滤器', 'value': 'filter'}],
                value=['filter'],
                labelStyle={'display': 'inline-block'}
            )
        ])

    @app.callback(
        Output('data-graphic', 'figure'),
        [Input('column-selector', 'value'),
         Input('chart-type-selector', 'value')]
    )
    def update_graph(selected_columns, chart_type):
        """
        根据选定的列和图表类型更新图表。
        """
        if selected_columns == ['所有列']:
            selected_columns = self.dataframe.columns.tolist()
        else:
            selected_columns = selected_columns
        if len(selected_columns) == 0:
            raise PreventUpdate

        filtered_data = self.dataframe[selected_columns]

        if chart_type == 'bar':
            fig = px.bar(filtered_data,
                        x=selected_columns[0],
                        y=selected_columns[1] if len(selected_columns) > 1 else None)
        elif chart_type == 'line':
            fig = px.line(filtered_data,
                          x=selected_columns[0],
                          y=selected_columns[1] if len(selected_columns) > 1 else None)
        elif chart_type == 'scatter':
            fig = px.scatter(filtered_data,
                             x=selected_columns[0],
                             y=selected_columns[1] if len(selected_columns) > 1 else None)
        else:
            fig = px.line(filtered_data)
        return fig

    def run(self):
        """
        运行Dash应用。
        """
        self.app.layout = self.layout
        self.app.run_server(debug=True)

# 使用示例
if __name__ == '__main__':
    # 假设有一个名为 'data.csv' 的CSV文件，包含待分析的数据
    df = pd.read_csv('data.csv')
    dashboard = DataAnalysisDashboard(df)
    dashboard.run()