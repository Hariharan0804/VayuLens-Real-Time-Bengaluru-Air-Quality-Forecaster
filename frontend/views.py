from django.shortcuts import render, redirect

def root_redirect(request):
    return redirect('dashboard')

def dashboard_view(request):
    return render(request, 'dashboard.html', {
        'active_page': 'dashboard',
        'page_title': 'Dashboard',
        'page_subtitle': 'Real-time environmental intelligence & station telemetry'
    })

def monitoring_view(request):
    return render(request, 'monitoring.html', {
        'active_page': 'monitoring',
        'page_title': 'Live Station Monitoring',
        'page_subtitle': 'Real-time station telemetry across Bengaluru urban corridors'
    })

def forecast_view(request):
    return render(request, 'forecast.html', {
        'active_page': 'forecast',
        'page_title': 'AI PM2.5 Forecast',
        'page_subtitle': 'Next-hour air quality predictions driven by Random Forest ML'
    })

def historical_view(request):
    return render(request, 'historical.html', {
        'active_page': 'historical',
        'page_title': 'Historical Air Quality Analysis',
        'page_subtitle': 'Aggregated environmental telemetry trends and diurnal profiles'
    })

def stations_view(request):
    return render(request, 'stations.html', {
        'active_page': 'stations',
        'page_title': 'Bengaluru Station Network',
        'page_subtitle': 'Continuous Ambient Air Quality Monitoring Station (CAAQMS) directory'
    })

def model_insights_view(request):
    return render(request, 'model_insights.html', {
        'active_page': 'model_insights',
        'page_title': 'ML Model Insights',
        'page_subtitle': 'Random Forest Regressor performance metrics, features, and validation'
    })

def about_view(request):
    return render(request, 'about.html', {
        'active_page': 'about',
        'page_title': 'About VayuLens',
        'page_subtitle': 'Real-Time Bengaluru Air Quality Forecaster Architecture'
    })
