from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from crypto_manager import CryptoManager

manager = CryptoManager()
bitcoin_dominance = manager.get_bitcoin_dominance()

# Optional external CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Register the Dash app with Django
app = DjangoDash('BitcoinDominance', external_stylesheets=external_stylesheets)

app.layout = html.Div(
    style={'width': '50%', 'margin': 'auto', 'padding': '40px', 'fontFamily': 'Arial, sans-serif'},
    children=[
        html.H3('Bitcoin Dominance', style={'textAlign': 'center'}),
        html.Div(id='dominance-text', style={'textAlign': 'center', 'fontSize': '24px', 'marginBottom': '20px'}),
        html.Div(
            dcc.Slider(
                id='dominance-slider',
                min=0,
                max=100,
                step=0.1,
                value=bitcoin_dominance,
                marks={0: '0%', 25: '25%', 50: '50%', 75: '75%', 100: '100%'},
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode='drag',
                included=True,
                vertical=False,
            ),
            style={'pointerEvents': 'none'}
        )
    ]
)

@app.callback(
    Output('dominance-text', 'children'),
    Input('dominance-slider', 'value')
)
def update_text(value):
    return html.Span(f'{value:.1f}%')
