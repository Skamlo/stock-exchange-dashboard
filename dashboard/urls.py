from django.urls import path
from . import views
from dashboard.dash_apps.finished_apps import fear_greed_chart, bitcoin_dominance, market_cap, volume

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('candlestick/', views.candlestick, name='candlestick'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
]
