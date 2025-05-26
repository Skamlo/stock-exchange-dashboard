from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from crypto_manager import CryptoManager
import dash_table
import pandas as pd

manager = CryptoManager()
df = manager.get_dataframe()

# Format numbers to align by decimal point
def align_by_decimal(val, max_int_len, max_frac_len):
    if pd.isna(val):
        return ""
    val_str = f"{val:.8f}".rstrip('0').rstrip('.')
    if '.' not in val_str:
        int_part, frac_part = val_str, ''
    else:
        int_part, frac_part = val_str.split('.')
    return f"{' ' * (max_int_len - len(int_part))}{int_part}.{frac_part}{' ' * (max_frac_len - len(frac_part))}"

# Preprocess numeric columns for alignment
formatted_df = df.copy()
for col in df.select_dtypes(include='number').columns:
    int_lens = df[col].apply(lambda x: len(str(int(abs(x)))) if pd.notna(x) else 0)
    frac_lens = df[col].apply(lambda x: len(str(x).split('.')[1]) if '.' in str(x) else 0)
    max_int_len = int_lens.max()
    max_frac_len = frac_lens.max()
    formatted_df[col] = df[col].apply(lambda x: align_by_decimal(x, max_int_len, max_frac_len))

# Optional external CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Register the Dash app with Django
app = DjangoDash('Table', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H3("Data Table"),
    dash_table.DataTable(
        data=formatted_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in formatted_df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'center',
            'fontFamily': 'Courier New, monospace',
            'whiteSpace': 'pre'
        }
    )
])
