from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go


def candlestick(request):
    return render(request, 'dashboard/candlestick.html')


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def about(request):
    return render(request, 'dashboard/about.html')
