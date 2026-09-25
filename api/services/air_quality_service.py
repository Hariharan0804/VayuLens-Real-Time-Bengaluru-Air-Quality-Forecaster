"""
Air Quality Service - Unified source of truth for AQI categories, levels, and descriptions.
"""

class AirQualityService:
    @staticmethod
    def calculate_aqi(pm25):
        """Standard CPCB AQI calculation for PM2.5."""
        if pm25 is None:
            return 50
        pm25 = float(pm25)
        if pm25 <= 30:
            return int((pm25 / 30) * 50)
        elif pm25 <= 60:
            return int(50 + ((pm25 - 30) / 30) * 50)
        elif pm25 <= 90:
            return int(100 + ((pm25 - 60) / 30) * 100)
        elif pm25 <= 120:
            return int(200 + ((pm25 - 90) / 30) * 100)
        elif pm25 <= 250:
            return int(300 + ((pm25 - 120) / 130) * 100)
        else:
            return int(400 + ((pm25 - 250) / 150) * 100)

    @staticmethod
    def get_aqi_category(aqi):
        aqi = int(aqi)
        if aqi <= 50:
            return {
                "category": "GOOD",
                "label": "Good",
                "level": "good",
                "color": "secondary",
                "bg": "bg-secondary-container",
                "text": "text-on-secondary-container",
                "badge_bg": "bg-emerald-100",
                "badge_text": "text-emerald-800",
                "description": "Air quality is considered satisfactory, and air pollution poses little or no risk."
            }
        elif aqi <= 100:
            return {
                "category": "MODERATE",
                "label": "Satisfactory",
                "level": "moderate",
                "color": "secondary",
                "bg": "bg-secondary-container",
                "text": "text-on-secondary-container",
                "badge_bg": "bg-lime-100",
                "badge_text": "text-lime-800",
                "description": "Air quality is acceptable; however, minor breathing discomfort for sensitive individuals."
            }
        elif aqi <= 200:
            return {
                "category": "MODERATE",
                "label": "Moderate",
                "level": "moderate",
                "color": "tertiary-fixed",
                "bg": "bg-surface-container-high",
                "text": "text-on-surface",
                "badge_bg": "bg-amber-100",
                "badge_text": "text-amber-800",
                "description": "May cause breathing discomfort to people with lung, heart disease, children and older adults."
            }
        elif aqi <= 300:
            return {
                "category": "POOR",
                "label": "Poor",
                "level": "poor",
                "color": "tertiary",
                "bg": "bg-tertiary-fixed",
                "text": "text-on-tertiary-fixed",
                "badge_bg": "bg-orange-100",
                "badge_text": "text-orange-800",
                "description": "Breathing discomfort to most people on prolonged exposure. Avoid strenuous outdoor activities."
            }
        elif aqi <= 400:
            return {
                "category": "VERY POOR",
                "label": "Very Poor",
                "level": "very_poor",
                "color": "error",
                "bg": "bg-error-container",
                "text": "text-on-error-container",
                "badge_bg": "bg-red-100",
                "badge_text": "text-red-800",
                "description": "Respiratory illness to people on prolonged exposure. High impact on people with heart disease."
            }
        else:
            return {
                "category": "SEVERE",
                "label": "Severe",
                "level": "severe",
                "color": "error",
                "bg": "bg-error-container",
                "text": "text-on-error-container",
                "badge_bg": "bg-rose-900",
                "badge_text": "text-white",
                "description": "Affects healthy people and seriously impacts those with existing health conditions."
            }
