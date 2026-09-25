import os
import json
import pandas as pd
import joblib
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "models" / "vayulens_model.pkl"
METADATA_PATH = BASE_DIR / "models" / "model_metadata.json"

class PredictionService:
    @staticmethod
    def get_prediction(current_data=None):
        if current_data is None:
            current_data = {}
            
        try:
            if not MODEL_PATH.exists() or not METADATA_PATH.exists():
                return {
                    "success": False,
                    "error": "ML Model or Metadata file missing in models/"
                }

            model = joblib.load(MODEL_PATH)
            with open(METADATA_PATH, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            features = metadata.get('features', [])
            now = datetime.now()

            # Construct row with mapped feature defaults or current inputs
            input_dict = {}
            for feat in features:
                if 'PM2.5' in feat:
                    input_dict[feat] = float(current_data.get('PM2.5', 42.5))
                elif 'PM10' in feat:
                    input_dict[feat] = float(current_data.get('PM10', 81.2))
                elif 'NO2' in feat:
                    input_dict[feat] = float(current_data.get('NO2', 27.5))
                elif 'SO2' in feat:
                    input_dict[feat] = float(current_data.get('SO2', 13.5))
                elif 'CO' in feat:
                    input_dict[feat] = float(current_data.get('CO', 1.05))
                elif 'Ozone' in feat:
                    input_dict[feat] = float(current_data.get('O3', 28.4))
                elif 'AT' in feat:
                    input_dict[feat] = float(current_data.get('temperature', 28.1))
                elif 'RH' in feat:
                    input_dict[feat] = float(current_data.get('humidity', 68.0))
                elif 'WS' in feat and 'VWS' not in feat:
                    input_dict[feat] = float(current_data.get('wind_speed', 1.9))
                elif 'Hour' in feat:
                    input_dict[feat] = now.hour
                elif 'Day_of_Week' in feat:
                    input_dict[feat] = now.weekday()
                elif 'Day' in feat:
                    input_dict[feat] = now.day
                elif 'Month' in feat:
                    input_dict[feat] = now.month
                else:
                    # Sensor defaults matching typical dataset medians
                    input_dict[feat] = 0.0

            input_df = pd.DataFrame([input_dict])
            predicted_pm25 = float(model.predict(input_df)[0])

            # Calculate AQI equivalent for predicted PM2.5
            from .openaq_service import OpenAQService
            predicted_aqi = OpenAQService.calculate_aqi(predicted_pm25)
            cat_info = OpenAQService.get_aqi_category(predicted_aqi)

            # Feature importance list (top 6)
            feat_imp = metadata.get('feature_importance', {})
            sorted_imp = sorted(feat_imp.items(), key=lambda x: x[1], reverse=True)[:6]
            top_features = [{"feature": k.split(' ')[0], "importance": round(v * 100, 1)} for k, v in sorted_imp]

            return {
                "success": True,
                "data": {
                    "prediction": round(predicted_pm25, 2),
                    "predicted_aqi": predicted_aqi,
                    "category": cat_info["category"],
                    "unit": "µg/m³",
                    "target": metadata.get('target', 'PM2.5_Next_Hour'),
                    "model": metadata.get('model_name', 'RandomForestRegressor'),
                    "mae": round(metadata.get('MAE', 4.40), 2),
                    "r2": round(metadata.get('R2', 0.86), 3),
                    "feature_importance": top_features,
                    "timestamp": now.isoformat()
                }
            }
        except Exception as e:
            print(f"[PredictionService] Inference Error: {e}")
            return {
                "success": False,
                "error": f"Prediction unavailable: {str(e)}"
            }
