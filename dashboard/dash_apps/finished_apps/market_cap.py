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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('MarketCap', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(
        dcc.Graph(
            id='market-cap-pie',
            figure={
                'data': [
                    go.Pie(
                        labels=selected_coins,
                        values=market_cap,
                        marker=dict(colors=px.colors.qualitative.Plotly),
                        textinfo='label+percent'
                    )
                ],
                'layout': go.Layout(
                    title={
                        'text': f'Market Cap Distribution by Coin<br>Total Market Cap: ${total_market_cap:,.2f}',
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                    height=300,
                    width=400,
                    margin=dict(l=30, r=30, t=50, b=30)
                )
            },
            style={'display': 'inline-block'}
        ),
        style={'textAlign': 'center'}
    )
])
