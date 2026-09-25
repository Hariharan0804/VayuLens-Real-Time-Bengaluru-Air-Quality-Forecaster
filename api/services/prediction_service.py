import os
import json
import pandas as pd
import joblib
from datetime import datetime

class PredictionService:
    @staticmethod
    def get_prediction(current_data):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            model_path = os.path.join(base_dir, 'models', 'vayulens_model.pkl')
            metadata_path = os.path.join(base_dir, 'models', 'model_metadata.json')
            
            if not os.path.exists(model_path) or not os.path.exists(metadata_path):
                return {"success": False, "error": "Model not loaded"}
                
            model = joblib.load(model_path)
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                
            features = metadata['features']
            
            # Map current_data to features, use medians or 0 if missing
            # In a real scenario we use actual mappings
            input_dict = {}
            for f in features:
                if 'PM2.5' in f:
                    input_dict[f] = current_data.get('PM2.5', 40.0)
                elif 'PM10' in f:
                    input_dict[f] = current_data.get('PM10', 80.0)
                elif 'NO2' in f:
                    input_dict[f] = current_data.get('NO2', 20.0)
                elif 'SO2' in f:
                    input_dict[f] = current_data.get('SO2', 15.0)
                elif 'CO' in f:
                    input_dict[f] = current_data.get('CO', 1.0)
                elif 'Ozone' in f:
                    input_dict[f] = current_data.get('O3', 30.0)
                else:
                    input_dict[f] = 0.0 # Default fallback
                    
            input_df = pd.DataFrame([input_dict])
            prediction = model.predict(input_df)[0]
            
            return {
                "success": True,
                "data": {
                    "prediction": float(prediction),
                    "unit": "µg/m³",
                    "model": metadata['model_name'],
                    "timestamp": datetime.now().isoformat()
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
