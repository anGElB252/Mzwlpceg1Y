# 代码生成时间: 2025-08-03 19:18:08
import os
import shutil
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# 定义常量
SOURCE_FOLDER = "/path/to/source"
DESTINATION_FOLDER = "/path/to/destination"

# 文件同步函数
def sync_files(source, destination):
    try:
        # 复制文件并保留目录结构
        for item in os.listdir(source):
            s = os.path.join(source, item)
            d = os.path.join(destination, item)
            if os.path.isdir(s):
                if not os.path.exists(d):
                    os.makedirs(d)
                sync_files(s, d)
            else:
                shutil.copy2(s, d)
        print(f"Files synced from {source} to {destination}")
    except Exception as e:
        print(f"Error syncing files: {e}")

# 文件备份函数
def backup_files(source, destination, backup_name):
    try:
        # 创建备份目录
        backup_path = os.path.join(destination, backup_name)
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        # 复制文件到备份目录
        for item in os.listdir(source):
            s = os.path.join(source, item)
            d = os.path.join(backup_path, item)
            if os.path.isdir(s):
                backup_files(s, backup_path, item)
            else:
                shutil.copy2(s, d)
        print(f"Files backed up from {source} to {backup_path}")
    except Exception as e:
        print(f"Error backing up files: {e}")

# 创建Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div(children=[
    html.H1("File Backup and Sync Tool"),
    html.Div(
        children=[
            html.P("Source Folder: "),
            dcc.Input(id="source-folder", type="text", placeholder=SOURCE_FOLDER),
        ]
    ),
    html.Div(
        children=[
            html.P("Destination Folder: "),
            dcc.Input(id="destination-folder", type="text", placeholder=DESTINATION_FOLDER),
        ]
    ),
    html.Button("Sync Files", id="sync-button", n_clicks=0),
    html.Button("Backup Files", id="backup-button", n_clicks=0),
    html.Div(id="output"),
])

# 同步文件回调函数
@app.callback(
    Output("output", "children"),
    [Input("sync-button", "n_clicks")],
    [State("source-folder", "value"), State("destination-folder", "value")],
)
def sync_output(n_clicks, source_folder, destination_folder):
    if n_clicks > 0:
        sync_files(source_folder, destination_folder)
        return "Files synced successfully"
    return ""

# 备份文件回调函数
@app.callback(
    Output("output", "children"),
    [Input("backup-button", "n_clicks")],
    [State("source-folder", "value"), State("destination-folder", "value")],
)
def backup_output(n_clicks, source_folder, destination_folder):
    if n_clicks > 0:
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_files(source_folder, destination_folder, backup_name)
        return "Files backed up successfully"
    return ""

if __name__ == "__main__":
    app.run_server(debug=True)