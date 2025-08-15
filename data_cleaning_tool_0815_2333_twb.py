# 代码生成时间: 2025-08-15 23:33:57
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# 定义数据清洗和预处理工具的类
class DataCleaningTool:
    def __init__(self, df):
        """
        初始化数据清洗工具。
        :param df: 待清洗的DataFrame。
        """
        self.df = df
        self.cleaned_df = df.copy()  # 复制原始DataFrame

    def handle_missing_values(self, method='mean'):
        """
        处理缺失值。
        :param method: 填充策略，可以是'mean', 'median', 'mode'或'drop'。
        """
        if method == 'mean':
            self.cleaned_df = self.cleaned_df.fillna(self.cleaned_df.mean())
        elif method == 'median':
            self.cleaned_df = self.cleaned_df.fillna(self.cleaned_df.median())
        elif method == 'mode':
            self.cleaned_df = self.cleaned_df.fillna(self.cleaned_df.mode().iloc[0])
        elif method == 'drop':
            self.cleaned_df = self.cleaned_df.dropna()
        else:
            raise ValueError('未知的缺失值处理方法')
        return self.cleaned_df

    def remove_outliers(self, method='z-score', threshold=3):
        """
        移除异常值。
        :param method: 异常值检测方法，可以是'z-score'或'iqr'。
        :param threshold: 异常值阈值。
        """
        if method == 'z-score':
            mean = self.cleaned_df.mean()
            std = self.cleaned_df.std()
            self.cleaned_df = self.cleaned_df[(self.cleaned_df - mean).abs() <= threshold * std]
        elif method == 'iqr':
            Q1 = self.cleaned_df.quantile(0.25)
            Q3 = self.cleaned_df.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - (1.5 * IQR)
            upper_bound = Q3 + (1.5 * IQR)
            self.cleaned_df = self.cleaned_df[(self.cleaned_df >= lower_bound) & (self.cleaned_df <= upper_bound)]
        else:
            raise ValueError('未知的异常值检测方法')
        return self.cleaned_df

    def normalize_data(self, method='min-max'):
        """
        数据归一化。
        :param method: 归一化方法，可以是'min-max'或'standard'。
        "