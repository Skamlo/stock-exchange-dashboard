from django.urls import path
from . import views
from dashboard.dash_apps.finished_apps import simple_example

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
