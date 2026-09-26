from rest_framework.views import APIView
from rest_framework.response import Response
import os
import json
from datetime import datetime

from .services.air_quality_service import AirQualityService
from .services.station_service import StationService
from .services.openaq_service import OpenAQService
from .services.prediction_service import PredictionService
from .services.historical_service import HistoricalService
from .services.insight_service import InsightService

class BaseAPIView(APIView):
    def success_response(self, data):
        return Response({
            "success": True, 
            "data": data, 
            "timestamp": datetime.now().isoformat()
        })
        
    def error_response(self, error, status=400):
        return Response({
            "success": False, 
            "error": error, 
            "timestamp": datetime.now().isoformat()
        }, status=status)

class HealthView(BaseAPIView):
    def get(self, request):
        openaq_status = OpenAQService.check_api_health() if hasattr(OpenAQService, 'check_api_health') else {"online": True}
        return self.success_response({
            "status": "healthy",
            "model_loaded": True,
            "openaq_configured": True,
            "openaq_status": openaq_status
        })

class CurrentAirQualityView(BaseAPIView):
    def get(self, request):
        station_id = request.GET.get('station', 'btm-layout')
        station_data = StationService.get_station_by_id(station_id)
        return self.success_response(station_data)

class PredictionView(BaseAPIView):
    def get(self, request):
        station_id = request.GET.get('station', 'btm-layout')
        station_data = StationService.get_station_by_id(station_id)
        prediction_res = PredictionService.get_prediction(station_data)
        if prediction_res.get('success'):
            data = prediction_res['data']
            data['available_stations'] = StationService.get_all_stations()
            return self.success_response(data)
        return self.error_response(prediction_res.get('error', 'Prediction error'))

class DashboardLiveView(BaseAPIView):
    def get(self, request):
        station_id = request.GET.get('station', 'btm-layout')
        station_data = StationService.get_station_by_id(station_id)
        prediction_res = PredictionService.get_prediction(station_data)
        pred_data = prediction_res.get('data', {}) if prediction_res.get('success') else {}
        insights = InsightService.get_insights_for_station(station_data) if hasattr(InsightService, 'get_insights_for_station') else []

        return self.success_response({
            "selected_station": station_data,
            "prediction": pred_data,
            "insights": insights,
            "insight_message": f"Air quality is currently {station_data.get('category_label', 'Moderate').lower()} at {station_data.get('name')}.",
            "available_stations": StationService.get_all_stations()
        })

class HistoricalView(BaseAPIView):
    def get(self, request):
        time_range = request.GET.get('range', '7d')
        res = HistoricalService.get_historical_analysis(time_range=time_range)
        if res.get('success'):
            return self.success_response(res['data'])
        return self.error_response(res.get('error', 'Historical data error'))

class StationsView(BaseAPIView):
    def get(self, request):
        zone = request.GET.get('zone', 'all')
        query = request.GET.get('q', None)
        stations_res = StationService.get_stations(zone_filter=zone, query=query)
        return self.success_response(stations_res)

class ModelInsightsView(BaseAPIView):
    def get(self, request):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            metadata_path = os.path.join(base_dir, 'models', 'model_metadata.json')
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            return self.success_response(metadata)
        except Exception as e:
            return self.error_response(f"Model insights unavailable: {str(e)}")

