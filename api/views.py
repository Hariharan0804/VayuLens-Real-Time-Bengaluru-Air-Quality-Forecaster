from rest_framework.views import APIView
from rest_framework.response import Response
import os
import json
from .services.openaq_service import OpenAQService

class BaseAPIView(APIView):
    def success_response(self, data):
        return Response({"success": True, "data": data, "timestamp": "2024-01-01T00:00:00Z"})
        
    def error_response(self, error):
        return Response({"success": False, "error": error, "timestamp": "2024-01-01T00:00:00Z"}, status=400)

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
        return self.success_response(data)

from .services.prediction_service import PredictionService

class PredictionView(BaseAPIView):
    def get(self, request):
        current_data = OpenAQService.get_bengaluru_data().get('data', {})
        result = PredictionService.get_prediction(current_data)
        if result['success']:
            return self.success_response(result['data'])
        return self.error_response(result['error'])

class DashboardLiveView(BaseAPIView):
    def get(self, request):
        current = OpenAQService.get_bengaluru_data()
        pred = PredictionService.get_prediction(current.get('data', {}))
        return self.success_response({
            "current": current,
            "prediction": pred.get('data', {}),
            "trend": {},
            "weather": {},
            "stations": [],
            "insights": []
        })

class HistoricalView(BaseAPIView):
    def get(self, request):
        return self.success_response({
            "Average AQI": 85,
            "Maximum AQI": 120,
            "Minimum AQI": 50,
            "Average PM2.5": 42.5
        })

class StationsView(BaseAPIView):
    def get(self, request):
        return self.success_response([
            {"Station name": "Bengaluru Central", "AQI": 85, "PM2.5": 42.5, "Status": "Active"}
        ])

class ModelInsightsView(BaseAPIView):
    def get(self, request):
        try:
            from django.conf import settings
            import os
            metadata_path = os.path.join(settings.BASE_DIR, 'models', 'model_metadata.json')
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            return self.success_response(metadata)
        except Exception as e:
            return self.error_response(f"Model insights unavailable: {str(e)}")
