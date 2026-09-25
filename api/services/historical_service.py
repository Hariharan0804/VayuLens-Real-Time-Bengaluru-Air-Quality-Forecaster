import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from .openaq_service import OpenAQService

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASET_PATH = BASE_DIR / "data" / "VayuLens_Training_Dataset.csv"

class HistoricalService:
    @staticmethod
    def get_historical_analysis(time_range="7d"):
        try:
            if not DATASET_PATH.exists():
                return {"success": False, "error": "Historical dataset file missing"}

            df = pd.read_csv(DATASET_PATH)
            
            # Limit slice according to requested range
            total_rows = len(df)
            if time_range == "7d":
                subset = df.tail(min(168, total_rows))
            elif time_range == "30d":
                subset = df.tail(min(720, total_rows))
            elif time_range == "90d":
                subset = df.tail(min(2160, total_rows))
            else:
                subset = df

            # Aggregations
            pm25_series = subset["PM2.5 (µg/m³)"].dropna()
            pm10_series = subset["PM10 (µg/m³)"].dropna() if "PM10 (µg/m³)" in subset.columns else pd.Series()
            no2_series = subset["NO2 (µg/m³)"].dropna() if "NO2 (µg/m³)" in subset.columns else pd.Series()
            so2_series = subset["SO2 (µg/m³)"].dropna() if "SO2 (µg/m³)" in subset.columns else pd.Series()
            co_series = subset["CO (mg/m³)"].dropna() if "CO (mg/m³)" in subset.columns else pd.Series()
            ozone_series = subset["Ozone (µg/m³)"].dropna() if "Ozone (µg/m³)" in subset.columns else pd.Series()

            avg_pm25 = float(pm25_series.mean()) if not pm25_series.empty else 45.0
            max_pm25 = float(pm25_series.max()) if not pm25_series.empty else 110.0
            min_pm25 = float(pm25_series.min()) if not pm25_series.empty else 12.0

            avg_aqi = OpenAQService.calculate_aqi(avg_pm25)
            max_aqi = OpenAQService.calculate_aqi(max_pm25)
            min_aqi = OpenAQService.calculate_aqi(min_pm25)

            # Daily Trend (sample ~14 data points or days for smooth Chart.js line)
            step = max(1, len(subset) // 14)
            trend_sample = subset.iloc[::step].tail(14)
            
            daily_labels = []
            daily_pm25 = []
            daily_aqi = []
            
            for idx, row in trend_sample.iterrows():
                ts_str = str(row.get("Timestamp", ""))
                label = ts_str.split(" ")[0] if " " in ts_str else f"Day {idx}"
                p25 = float(row.get("PM2.5 (µg/m³)", 40.0))
                daily_labels.append(label)
                daily_pm25.append(round(p25, 1))
                daily_aqi.append(OpenAQService.calculate_aqi(p25))

            # Hourly Diurnal Pattern (averages grouped by 'Hour' column if available)
            hourly_pattern = []
            if "Hour" in subset.columns:
                grouped_hour = subset.groupby("Hour")["PM2.5 (µg/m³)"].mean()
                for hr in range(24):
                    val = float(grouped_hour.get(hr, 40.0))
                    hourly_pattern.append(round(val, 1))
            else:
                hourly_pattern = [round(30 + 15 * np.sin(h/3), 1) for h in range(24)]

            # Pollutant Comparison Averages
            pollutant_averages = {
                "PM2.5": round(avg_pm25, 1),
                "PM10": round(float(pm10_series.mean()) if not pm10_series.empty else 82.0, 1),
                "NO2": round(float(no2_series.mean()) if not no2_series.empty else 26.5, 1),
                "SO2": round(float(so2_series.mean()) if not so2_series.empty else 14.2, 1),
                "CO": round(float(co_series.mean()) if not co_series.empty else 1.1, 2),
                "O3": round(float(ozone_series.mean()) if not ozone_series.empty else 31.0, 1)
            }

            return {
                "success": True,
                "data": {
                    "time_range": time_range,
                    "total_records": len(subset),
                    "metrics": {
                        "average_aqi": avg_aqi,
                        "maximum_aqi": max_aqi,
                        "minimum_aqi": min_aqi,
                        "average_pm25": round(avg_pm25, 1),
                        "maximum_pm25": round(max_pm25, 1),
                        "minimum_pm25": round(min_pm25, 1)
                    },
                    "daily_trend": {
                        "labels": daily_labels,
                        "pm25": daily_pm25,
                        "aqi": daily_aqi
                    },
                    "hourly_diurnal": hourly_pattern,
                    "pollutant_averages": pollutant_averages
                }
            }
        except Exception as e:
            print(f"[HistoricalService] Error: {e}")
            return {"success": False, "error": str(e)}
