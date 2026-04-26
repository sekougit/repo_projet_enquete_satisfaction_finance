from django.urls import path
from django_plotly_dash.views import add_to_session
from .views import dashboard_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
]