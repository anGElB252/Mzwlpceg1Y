# 代码生成时间: 2025-08-17 13:32:45
import os
from pathlib import Path
from dash import Dash, html, dcc, Input, Output, State
import re


"""
Batch Rename Tool using Dash framework
This tool allows users to rename multiple files based on a given pattern.

Attributes:
    None

Methods:
    - generate_pattern: Generates a naming pattern based on user input.
    - rename_files: Renames files in the specified directory according to the generated pattern.

Todo:
    - Add functionality to handle file types and extensions.
    - Add a progress bar for the renaming process.

"""

# Define the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Input(id='source-directory', type='text', placeholder='Enter the source directory'),
    dcc.Input(id='naming-pattern', type='text', placeholder='Enter the naming pattern (e.g., {index}-filename.ext)'),
    html.Button('Rename Files', id='rename-button', n_clicks=0),
    dcc.Output('rename-output', 'children')
])


# Callback to handle file renaming
@app.callback(
    Output('rename-output', 'children'),
    [Input('rename-button', 'n_clicks')],
    state=[State('source-directory', 'value'), State('naming-pattern', 'value')])
def rename_files(n_clicks, source_directory, naming_pattern):
    # Check if the user has provided a source directory and a naming pattern
    if not source_directory or not naming_pattern:
        return 'Please provide a source directory and a naming pattern.'

    # Try to rename the files
    try:
        # Get the list of files in the source directory
        files = os.listdir(source_directory)

        # Initialize a counter for the file names
        file_index = 1

        # Iterate over the files and rename them
        for file in files:
            # Create the new file name using the provided pattern
            file_path = Path(source_directory) / file
            if file_path.is_file():
                new_name = re.sub(r'{index}', str(file_index), naming_pattern)
                new_file_path = Path(source_directory) / new_name

                # Rename the file
                os.rename(file_path, new_file_path)
                file_index += 1

        return 'Files renamed successfully.'
    except Exception as e:
        # Handle any exceptions that occur during the renaming process
        return f'An error occurred: {str(e)}'


if __name__ == '__main__':
    # Run the Dash app
    app.run_server(debug=True)