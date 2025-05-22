from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')