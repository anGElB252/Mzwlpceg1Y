# 代码生成时间: 2025-09-29 00:00:43
import dash\
import dash_core_components as dcc\
import dash_html_components as html\
from dash.dependencies import Input, Output, State\
import dash_bootstrap_components as dbc\
from dash.exceptions import PreventUpdate\
import pandas as pd\
import numpy as np\
\
# 虚拟滚动组件\
class VirtualScrollList:
    def __init__(self, app, dataframe, items_per_page=10, scrollable_width=1000, min_height=200):
        """
        初始化虚拟滚动列表
        :param app: Dash应用
        :param dataframe: 数据框，包含列表的数据
        :param items_per_page: 每页显示的条目数
        :param scrollable_width: 滚动容器的宽度
        :param min_height: 滚动容器的最小高度
        """
        self.app = app
        self.dataframe = dataframe
        self.items_per_page = items_per_page
        self.scrollable_width = scrollable_width
        self.min_height = min_height
        self.callback_id = f'{app.callback_id_prefix}virtual-scroll-list'
        self.layout = self.create_layout()

    def create_layout(self):
        """
        创建虚拟滚动列表的布局
        """
        return html.Div(
            [
                dcc.Loading(
                    id=self.callback_id,
                    children=html.Div(id=f'{self.callback_id}-container')
                ),
                html.Div(
                    id=f'{self.callback_id}-scrollbar',
                    style={'overflow-y': 'scroll',
                            'width': f'{self.scrollable_width}px',
                            'min-height': f'{self.min_height}px',
                            'border': '1px solid black'}
                ),
                html.Div(
                    id=f'{self.callback_id}-footer'
                )
            ],
            style={'width': '100%'}
        )

    def update_scrollbar(self, n_items, scroll_top):
        "