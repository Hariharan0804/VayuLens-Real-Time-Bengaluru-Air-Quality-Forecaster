from django.urls import path
from . import views

urlpatterns = [
    path('', views.root_redirect, name='root_redirect'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('monitoring/', views.monitoring_view, name='monitoring'),
    path('forecast/', views.forecast_view, name='forecast'),
    path('historical/', views.historical_view, name='historical'),
    path('stations/', views.stations_view, name='stations'),
    path('model-insights/', views.model_insights_view, name='model_insights'),
    path('about/', views.about_view, name='about'),
]
