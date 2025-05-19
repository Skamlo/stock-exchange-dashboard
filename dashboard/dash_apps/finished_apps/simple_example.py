from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

# Optional external CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Register the Dash app with Django
app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div([
    html.H1('Square Root Slider Graph'),
    dcc.Graph(
        id='slider-graph',
        animate=True,
        style={"backgroundColor": "#1a2d46", "color": "#ffffff"}
    ),
    dcc.Slider(
        id='slider-updatemode',
        marks={i: f'{i}' for i in range(21)},
        max=20,
        value=2,
        step=1,
        updatemode='drag',
    )
])

# Callback to update graph based on slider
@app.callback(
    Output('slider-graph', 'figure'),
    [Input('slider-updatemode', 'value')]
)
def display_value(value):
    x = list(range(value))
    y = [i * i for i in x]

    graph = go.Scatter(x=x, y=y, name='Manipulate Graph')
    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(range=[min(y), max(y)]),
        font=dict(color='white')
    )

    return {'data': [graph], 'layout': layout}
