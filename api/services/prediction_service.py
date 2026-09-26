import os
import json
import pandas as pd
import joblib
from datetime import datetime, timedelta
from pathlib import Path
from .air_quality_service import AirQualityService

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

            # Construct input row using station's current atmospheric metrics
            input_dict = {}
            for feat in features:
                if 'PM2.5' in feat:
                    input_dict[feat] = float(current_data.get('pm25', current_data.get('PM2.5', 42.5)))
                elif 'PM10' in feat:
                    input_dict[feat] = float(current_data.get('pm10', current_data.get('PM10', 81.2)))
                elif 'NO2' in feat:
                    input_dict[feat] = float(current_data.get('no2', current_data.get('NO2', 27.5)))
                elif 'SO2' in feat:
                    input_dict[feat] = float(current_data.get('so2', current_data.get('SO2', 13.5)))
                elif 'CO' in feat:
                    input_dict[feat] = float(current_data.get('co', current_data.get('CO', 1.05)))
                elif 'Ozone' in feat:
                    input_dict[feat] = float(current_data.get('o3', current_data.get('O3', 28.4)))
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
                    input_dict[feat] = 0.0

            input_df = pd.DataFrame([input_dict])
            predicted_pm25 = float(model.predict(input_df)[0])

            predicted_aqi = AirQualityService.calculate_aqi(predicted_pm25)
            cat_info = AirQualityService.get_aqi_category(predicted_aqi)

            # Current station PM2.5 and AQI
            current_pm25 = float(current_data.get('pm25', 50.0))
            current_aqi = AirQualityService.calculate_aqi(current_pm25)
            current_cat = AirQualityService.get_aqi_category(current_aqi)

            # Change percentage
            if current_pm25 > 0:
                change_pct = round(((predicted_pm25 - current_pm25) / current_pm25) * 100, 1)
            else:
                change_pct = 0.0

            # Multi-step hourly forecast generation (h=1 to 24)
            hourly_forecast = []
            curr_step_pm25 = predicted_pm25
            sim_dict = dict(input_dict)
            mae = float(metadata.get('MAE', 4.33))

            for h in range(1, 25):
                sim_dict['PM2.5 (\u00b5g/m\u00b3)'] = curr_step_pm25
                sim_dict['Hour'] = (now.hour + h) % 24
                
                sim_df = pd.DataFrame([sim_dict])
                step_pred = float(model.predict(sim_df)[0])
                step_pred = max(5.0, round(step_pred, 1))

                step_aqi = AirQualityService.calculate_aqi(step_pred)
                step_cat_info = AirQualityService.get_aqi_category(step_aqi)

                uncertainty = round(mae * (1 + 0.03 * h), 1)
                lower_ci = max(0.0, round(step_pred - uncertainty, 1))
                upper_ci = round(step_pred + uncertainty, 1)

                future_dt = now + timedelta(hours=h)
                time_str = future_dt.strftime("%H:00")

                hourly_forecast.append({
                    "step": h,
                    "label": f"+{h} HR" if h > 0 else "NOW",
                    "time": time_str,
                    "pm25": step_pred,
                    "aqi": step_aqi,
                    "category": step_cat_info["category"],
                    "category_label": step_cat_info["label"],
                    "badge_bg": step_cat_info["badge_bg"],
                    "badge_text": step_cat_info["badge_text"],
                    "lower_ci": lower_ci,
                    "upper_ci": upper_ci
                })
                curr_step_pm25 = step_pred

            # AQI Horizons (1h, 3h, 6h, 12h, 24h)
            aqi_horizons = [
                {"horizon": "Next Hour", "step": 1, "data": hourly_forecast[0]},
                {"horizon": "Next 3 Hours", "step": 3, "data": hourly_forecast[2]},
                {"horizon": "Next 6 Hours", "step": 6, "data": hourly_forecast[5]},
                {"horizon": "Next 12 Hours", "step": 12, "data": hourly_forecast[11]},
                {"horizon": "Next 24 Hours", "step": 24, "data": hourly_forecast[23]},
            ]

            # Feature importance list
            feat_imp = metadata.get('feature_importance', {})
            sorted_imp = sorted(feat_imp.items(), key=lambda x: x[1], reverse=True)[:8]
            top_features = [{"feature": k.split(' ')[0], "importance": round(v * 100, 1)} for k, v in sorted_imp]

            station_name = current_data.get('name', current_data.get('station', 'Bengaluru Station'))
            station_id = current_data.get('id', 'btm-layout')

            # Weather Impact
            temp = current_data.get('temperature', 28.1)
            rh = current_data.get('humidity', 66)
            ws = current_data.get('wind_speed', 1.9)
            wd = current_data.get('wind_direction', 'SE')
            bp = "752 mmHg"

            if ws < 1.5 and rh > 60:
                weather_exp = f"Stagnant air (wind speed {ws} m/s {wd}) and high relative humidity ({rh}%) promote localized particulate accumulation at {station_name}."
            elif ws >= 2.5:
                weather_exp = f"Active wind velocity ({ws} m/s {wd}) facilitates atmospheric particulate dispersion across the local canopy at {station_name}."
            else:
                weather_exp = f"Moderate ambient wind ({ws} m/s {wd}) and temperature ({temp}°C) maintain stable atmospheric mixing at {station_name}."

            # AI Forecast Insight
            direction = "increase" if change_pct > 0 else ("decrease" if change_pct < 0 else "remain stable")
            change_str = f"+{change_pct}%" if change_pct > 0 else f"{change_pct}%"
            ai_insight = f"PM2.5 concentration at {station_name} is projected to {direction} ({change_str}) over the next hour from {current_pm25} to {round(predicted_pm25, 1)} µg/m³. Primary driving factors include ambient PM2.5 persistence and local atmospheric conditions."

            from .station_service import StationService
            all_stations = StationService.get_all_stations()
            comp_stations = []
            for st_info in all_stations[:4]:
                st_detail = StationService.get_station_by_id(st_info['id'])
                input_tmp = {}
                for feat in features:
                    if 'PM2.5' in feat: input_tmp[feat] = float(st_detail.get('pm25', 42.5))
                    elif 'PM10' in feat: input_tmp[feat] = float(st_detail.get('pm10', 81.2))
                    elif 'NO2' in feat: input_tmp[feat] = float(st_detail.get('no2', 27.5))
                    elif 'SO2' in feat: input_tmp[feat] = float(st_detail.get('so2', 13.5))
                    elif 'CO' in feat: input_tmp[feat] = float(st_detail.get('co', 1.05))
                    elif 'Ozone' in feat: input_tmp[feat] = float(st_detail.get('o3', 28.4))
                    elif 'AT' in feat: input_tmp[feat] = float(st_detail.get('temperature', 28.1))
                    elif 'RH' in feat: input_tmp[feat] = float(st_detail.get('humidity', 68.0))
                    elif 'WS' in feat and 'VWS' not in feat: input_tmp[feat] = float(st_detail.get('wind_speed', 1.9))
                    elif 'Hour' in feat: input_tmp[feat] = now.hour
                    elif 'Day_of_Week' in feat: input_tmp[feat] = now.weekday()
                    elif 'Day' in feat: input_tmp[feat] = now.day
                    elif 'Month' in feat: input_tmp[feat] = now.month
                    else: input_tmp[feat] = 0.0
                pred_tmp = float(model.predict(pd.DataFrame([input_tmp]))[0])
                aqi_tmp = AirQualityService.calculate_aqi(pred_tmp)

                comp_stations.append({
                    "id": st_detail["id"],
                    "name": st_detail["name"],
                    "current_pm25": st_detail["pm25"],
                    "current_aqi": st_detail["aqi"],
                    "next_pm25": round(pred_tmp, 1),
                    "next_aqi": aqi_tmp,
                    "category_label": st_detail["category_label"],
                    "badge_bg": st_detail["badge_bg"],
                    "badge_text": st_detail["badge_text"]
                })

            return {
                "success": True,
                "data": {
                    "station_id": station_id,
                    "station": station_name,
                    "current_pm25": current_pm25,
                    "current_aqi": current_aqi,
                    "current_category": current_cat.get("label", "Moderate"),
                    "current_badge_bg": current_cat.get("badge_bg", "bg-amber-100"),
                    "current_badge_text": current_cat.get("badge_text", "text-amber-800"),
                    "prediction": round(predicted_pm25, 2),
                    "predicted_aqi": predicted_aqi,
                    "category": cat_info.get("category", "MODERATE"),
                    "category_label": cat_info.get("label", "Moderate"),
                    "badge_bg": cat_info.get("badge_bg", "bg-amber-100"),
                    "badge_text": cat_info.get("badge_text", "text-amber-800"),
                    "change_pct": change_pct,
                    "change_pct_str": change_str,
                    "confidence_pct": round(metadata.get('R2', 0.862) * 100, 1),
                    "unit": "µg/m³",
                    "target": metadata.get('target', 'PM2.5_Next_Hour'),
                    "model": metadata.get('model_name', 'RandomForestRegressor'),
                    "mae": round(metadata.get('MAE', 4.40), 2),
                    "r2": round(metadata.get('R2', 0.86), 3),
                    "feature_importance": top_features,
                    "trend_24h": current_data.get("trend_24h", []),
                    "hourly_forecast": hourly_forecast,
                    "aqi_horizons": aqi_horizons,
                    "weather_impact": {
                        "temperature": temp,
                        "humidity": rh,
                        "wind_speed": ws,
                        "wind_direction": wd,
                        "pressure": bp,
                        "explanation": weather_exp
                    },
                    "ai_insight": ai_insight,
                    "comparison_stations": comp_stations,
                    "pollutants": {
                        "pm25": {"current": current_data.get("pm25", 72.4), "unit": "µg/m³", "forecast": round(predicted_pm25, 1), "is_ml_predicted": True},
                        "pm10": {"current": current_data.get("pm10", 118.2), "unit": "µg/m³", "forecast": "Live measurement / trend", "is_ml_predicted": False},
                        "no2": {"current": current_data.get("no2", 32.1), "unit": "µg/m³", "forecast": "Live measurement / trend", "is_ml_predicted": False},
                        "co": {"current": current_data.get("co", 1.2), "unit": "mg/m³", "forecast": "Live measurement / trend", "is_ml_predicted": False},
                        "so2": {"current": current_data.get("so2", 14.5), "unit": "µg/m³", "forecast": "Live measurement / trend", "is_ml_predicted": False},
                        "o3": {"current": current_data.get("o3", 28.5), "unit": "µg/m³", "forecast": "Live measurement / trend", "is_ml_predicted": False}
                    },
                    "timestamp": now.isoformat()
                }
            }
        except Exception as e:
            print(f"[PredictionService] Inference Error: {e}")
            return {
                "success": False,
                "error": f"Prediction unavailable: {str(e)}"
            }

