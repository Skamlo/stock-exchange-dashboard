from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from crypto_manager import CryptoManager

manager = CryptoManager()

# Optional external CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Register the Dash app with Django
app = DjangoDash('BitcoinDominance', external_stylesheets=external_stylesheets)

app.layout = html.Div(
    style={'width': '50%', 'margin': 'auto', 'padding': '40px', 'fontFamily': 'Arial, sans-serif'},
    children=[
        html.Div(id='dominance-text', style={'textAlign': 'center', 'fontSize': '24px', 'marginBottom': '20px'}),
        dcc.Dropdown(
            id='coin-dropdown',
            options=[{'label': coin, 'value': coin} for coin in manager.get_selected_coins()],
            value="BTC",
            clearable=False,
            style={'marginBottom': '30px'}
        ),
        html.Div(
            dcc.Slider(
                id='dominance-slider',
                min=0,
                max=100,
                step=0.1,
                value=0,
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
    Output('dominance-slider', 'value'),
    Input('coin-dropdown', 'value')
)
def update_dominance(coin):
    dominance = manager.get_dominance(coin)
    return f'{coin} Dominance: {dominance:.1f}%', dominance
