from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from crypto_manager import CryptoManager

manager = CryptoManager()
coins = manager.get_top_n_coin_volumes()
symbols = [coin['symbol'] for coin in coins]
volumes = [coin['volume'] for coin in coins]
# Optional external CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Register the Dash app with Django
app = DjangoDash('Volume', external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.H3("Volume of Top Cryptocurrencies"),
    dcc.Graph(
        id='market-cap-bar',
        figure={
            'data': [
                go.Bar(
                    x=symbols,
                    y=volumes,
                    marker_color='blue'
                )
            ],
            'layout': go.Layout(
                title='Volume by Coin',
                xaxis={'title': 'Coin'},
                yaxis={'title': 'Volume', 'type': 'linear'}
            )
        }
    ),
])