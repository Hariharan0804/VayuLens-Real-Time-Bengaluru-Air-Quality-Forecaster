from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.HealthView.as_view(), name='health'),
    path('air-quality/current/', views.CurrentAirQualityView.as_view(), name='current-air-quality'),
    path('prediction/', views.PredictionView.as_view(), name='prediction'),
    path('dashboard/live/', views.DashboardLiveView.as_view(), name='dashboard-live'),
    path('historical/', views.HistoricalView.as_view(), name='historical'),
    path('stations/', views.StationsView.as_view(), name='stations'),
    path('model/insights/', views.ModelInsightsView.as_view(), name='model-insights'),
]
