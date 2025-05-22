from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from crypto_manager import CryptoManager

import plotly.express as px

manager = CryptoManager()

total_market_cap = manager.get_total_crypto_market_cap()
selected_coins = manager.get_selected_coins()
market_cap = manager.get_coin_market_cap(selected_coins)
selected_coins.append("Other")
market_cap.append(total_market_cap - sum(market_cap))


# Optional external CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Register the Dash app with Django
app = DjangoDash('MarketCap', external_stylesheets=external_stylesheets)



app.layout = html.Div([
    html.H3("Market Caps of Selected Cryptocurrencies"),
    dcc.Graph(
        id='market-cap-pie',
        figure={
            'data': [
                go.Pie(
                    labels=selected_coins,
                    values=market_cap,
                    marker=dict(colors=px.colors.qualitative.Plotly)
                )
            ],
            'layout': go.Layout(
                title='Market Cap Distribution by Coin'
            )
        }
    ),
    html.Div(f"Total Market Cap: ${total_market_cap:,.2f}", style={'fontSize': 20, 'marginTop': 20})
])