from django.contrib import admin
from django.urls import path, include
from frontend import views as frontend_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # Page Routes
    path('', frontend_views.root_redirect, name='root'),
    path('dashboard/', frontend_views.dashboard_view, name='dashboard'),
    path('monitoring/', frontend_views.monitoring_view, name='monitoring'),
    path('forecast/', frontend_views.forecast_view, name='forecast'),
    path('historical/', frontend_views.historical_view, name='historical'),
    path('stations/', frontend_views.stations_view, name='stations'),
    path('model-insights/', frontend_views.model_insights_view, name='model_insights'),
    path('about/', frontend_views.about_view, name='about'),
]
