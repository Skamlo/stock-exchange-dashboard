from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from crypto_manager import CryptoManager

manager = CryptoManager()
fear_greed_value = manager.get_fear_and_greed_index()

# Optional external CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Register the Dash app with Django
app = DjangoDash('FearAndGreed', external_stylesheets=external_stylesheets)


app.layout = html.Div(
    style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'height': '100vh', 'backgroundColor': '#f9f9f9'},
    children=[
        dcc.Graph(
            figure=go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=fear_greed_value,
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': 'rgba(0,0,0,0)'},
                        'steps': [
                            {'range': [0, 25], 'color': "#d62728"},
                            {'range': [25, 50], 'color': "#ff7f0e"},
                            {'range': [50, 75], 'color': "#bcbd22"},
                            {'range': [75, 100], 'color': "#2ca02c"},
                        ],
                        'threshold': {
                            'line': {'color': "white", 'width': 8},
                            'thickness': 0.9,
                            'value': fear_greed_value
                        }
                    },
                    number={'font': {'size': 48}},
                    domain={'x': [0, 1], 'y': [0, 1]},
                )
            ).update_layout(
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor="#f9f9f9"
            ),
            config={'displayModeBar': False}
        )
    ]
)

