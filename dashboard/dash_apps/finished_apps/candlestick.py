from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from crypto_manager import CryptoManager
from datetime import datetime, timedelta

manager = CryptoManager()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('Candlestick', external_stylesheets=external_stylesheets)

# Time ranges and corresponding intervals
RANGE_TO_INTERVAL = {
    '5y': ('1w', timedelta(weeks=260)),
    '1y': ('1d', timedelta(weeks=52)),
    '30d': ('4h', timedelta(days=30)),
    '1d': ('1h', timedelta(days=1)),
    '1h': ('1m', timedelta(hours=1)),
    '5m': ('1m', timedelta(minutes=5))
}

app.layout = html.Div(
    style={'width': '95%', 'margin': '0 auto', 'padding': '40px', 'fontFamily': 'Arial, sans-serif'},
    children=[
        html.H2("Cryptocurrency Candlestick Chart", style={'textAlign': 'center'}),

        html.Div(style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px'}, children=[
            dcc.Dropdown(
                id='coin-dropdown',
                options=[{'label': coin, 'value': coin} for coin in manager.get_selected_coins()],
                value='BTC',
                style={'width': '200px'}
            ),
            dcc.Dropdown(
                id='range-dropdown',
                options=[
                    {'label': 'Last 5 Years', 'value': '5y'},
                    {'label': 'Last 1 Year', 'value': '1y'},
                    {'label': 'Last 30 Days', 'value': '30d'},
                    {'label': 'Last 1 Day', 'value': '1d'},
                    {'label': 'Last 1 Hour', 'value': '1h'},
                    {'label': 'Last 5 Minutes', 'value': '5m'}
                ],
                value='30d',
                style={'width': '200px'}
            )
        ]),

        dcc.Graph(id='candlestick-chart', style={'width': '95%', 'height': '600px', 'margin': '40px auto 0'})
    ]
)

@app.callback(
    Output('candlestick-chart', 'figure'),
    [Input('coin-dropdown', 'value'),
     Input('range-dropdown', 'value')]
)
def update_chart(selected_coin, selected_range):
    interval, delta = RANGE_TO_INTERVAL[selected_range]
    end_date = datetime.utcnow()
    start_date = end_date - delta

    data = manager.get_coin_prices(
        selected_coin,
        start_date.strftime('%Y-%m-%d %H:%M:%S'),
        end_date.strftime('%Y-%m-%d %H:%M:%S'),
        interval=interval
    )

    if not data:
        return go.Figure()

    figure = go.Figure(data=[go.Candlestick(
        x=[datetime.fromtimestamp(d['timestamp'] / 1000) for d in data],
        open=[d['open'] for d in data],
        high=[d['high'] for d in data],
        low=[d['low'] for d in data],
        close=[d['close'] for d in data],
        name=selected_coin
    )])
    figure.update_layout(
        title=f'{selected_coin} Price ({selected_range.upper()}, Interval: {interval})',
        xaxis_title='Date',
        yaxis_title='Price (USDT)',
        xaxis_rangeslider_visible=False
    )
    return figure
