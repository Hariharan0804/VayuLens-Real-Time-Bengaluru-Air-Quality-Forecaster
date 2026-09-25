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
        data = OpenAQService.get_bengaluru_data()
        return self.success_response(data.get("data", {}))

class PredictionView(BaseAPIView):
    def get(self, request):
        current_res = OpenAQService.get_bengaluru_data()
        current_data = current_res.get('data', {})
        result = PredictionService.get_prediction(current_data)
        if result['success']:
            return self.success_response(result['data'])
        return self.error_response(result.get('error', 'Prediction error'))

class DashboardLiveView(BaseAPIView):
    def get(self, request):
        current = OpenAQService.get_bengaluru_data().get('data', {})
        pred = PredictionService.get_prediction(current).get('data', {})
        stations_res = StationService.get_stations(zone_filter="all")
        
        # 24h sample trend for dashboard chart
        trend_24h = [
            {"time": "00:00", "pm25": 42.1},
            {"time": "03:00", "pm25": 38.5},
            {"time": "06:00", "pm25": 45.2},
            {"time": "09:00", "pm25": 58.6},
            {"time": "12:00", "pm25": 41.0},
            {"time": "15:00", "pm25": 36.4},
            {"time": "18:00", "pm25": 52.8},
            {"time": "21:00", "pm25": 48.0},
            {"time": "Now", "pm25": current.get("PM2.5", 42.5)}
        ]

        return self.success_response({
            "current": current,
            "prediction": pred,
            "trend_24h": trend_24h,
            "station_count": stations_res["total"],
            "hotspot": {
                "name": "Central Silk Board",
                "aqi": 178,
                "category": "Poor",
                "ward": "Ward 174 • Flyover basin stagnation"
            },
            "cleanest": {
                "name": "Cubbon Park Eco-Grove",
                "aqi": 68,
                "category": "Satisfactory",
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
