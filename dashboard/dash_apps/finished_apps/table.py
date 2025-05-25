from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from crypto_manager import CryptoManager
import dash_table
import pandas as pd

manager = CryptoManager()
df = manager.get_dataframe()

# Optional external CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Register the Dash app with Django
app = DjangoDash('Table', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H3("Data Table"),
    dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        sort_action='native',
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
    )
])

