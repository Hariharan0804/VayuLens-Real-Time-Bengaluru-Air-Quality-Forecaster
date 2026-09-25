from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

from .services.openaq_service import OpenAQService
from .services.prediction_service import PredictionService
from .services.historical_service import HistoricalService
from .services.station_service import StationService
from .services.insight_service import InsightService

class BaseAPIView(APIView):
    def success_response(self, data):
        return Response({
            "success": True,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        
    def error_response(self, error, status_code=400):
        return Response({
            "success": False,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }, status=status_code)

class HealthView(BaseAPIView):
    def get(self, request):
        return self.success_response({
            "status": "healthy",
            "model_loaded": True,
            "openaq_configured": True
        })

class CurrentAirQualityView(BaseAPIView):
    def get(self, request):
        station_id = request.query_params.get('station', 'btm-layout')
        station_data = StationService.get_station_by_id(station_id)
        return self.success_response(station_data)

class PredictionView(BaseAPIView):
    def get(self, request):
        station_id = request.query_params.get('station', 'btm-layout')
        station_data = StationService.get_station_by_id(station_id)
        result = PredictionService.get_prediction(station_data)
        if result['success']:
            return self.success_response(result['data'])
        return self.error_response(result.get('error', 'Prediction error'))

class DashboardLiveView(BaseAPIView):
    def get(self, request):
        station_id = request.query_params.get('station', 'btm-layout')
        station_data = StationService.get_station_by_id(station_id)
        pred_res = PredictionService.get_prediction(station_data)
        pred_data = pred_res.get('data', {}) if pred_res.get('success') else {}
        
        all_stations = StationService.get_all_stations()

        # Station-specific insights message
        primary_pollutant = "PM2.5"
        if station_data.get("no2", 0) > station_data.get("pm25", 0):
            primary_pollutant = "NO2 (Vehicular Emissions)"
        elif station_data.get("so2", 0) > 20:
            primary_pollutant = "SO2 (Industrial Sulfur)"

        insight_msg = f"{primary_pollutant} is currently the primary pollutant at {station_data['name']}. {station_data['description']}"

        return self.success_response({
            "selected_station": station_data,
            "prediction": pred_data,
            "all_stations": all_stations,
            "insight_message": insight_msg,
            "hotspot": {
                "name": "Central Silk Board",
                "aqi": 178,
                "category": "POOR",
                "label": "Poor",
                "ward": "Ward 174 • Flyover basin stagnation"
            },
            "cleanest": {
                "name": "Cubbon Park Eco-Grove",
                "aqi": 68,
                "category": "MODERATE",
                "label": "Satisfactory",
                "ward": "Canopy density filtering active"
            }
        })

class HistoricalView(BaseAPIView):
    def get(self, request):
        time_range = request.query_params.get("range", "7d")
        res = HistoricalService.get_historical_analysis(time_range)
        if res["success"]:
            return self.success_response(res["data"])
        return self.error_response(res["error"])

class StationsView(BaseAPIView):
    def get(self, request):
        zone = request.query_params.get("zone", "all")
        q = request.query_params.get("q", None)
        res = StationService.get_stations(zone_filter=zone, query=q)
        return self.success_response(res)

class ModelInsightsView(BaseAPIView):
    def get(self, request):
        res = InsightService.get_model_insights()
        if res["success"]:
            return self.success_response(res["data"])
        return self.error_response(res["error"])
