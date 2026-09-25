from datetime import datetime
from .air_quality_service import AirQualityService

STATIONS_DATA = [
    {
        "id": "btm-layout",
        "name": "BTM Layout",
        "zone": "south",
        "zone_label": "South Zone",
        "ward": "Ward 176 - Udupi Garden Lake",
        "pm25": 72.4,
        "pm10": 118.2,
        "no2": 32.1,
        "so2": 14.5,
        "co": 1.2,
        "o3": 28.5,
        "temperature": 28.1,
        "humidity": 66,
        "wind_speed": 1.9,
        "wind_direction": "SE",
        "microclimate": "28.1°C • 66% RH • 1.9 m/s SE",
        "sensor_array": "Optical Laser Particle",
        "status": "Active • Validated",
        "updated": "2m ago",
        "trend_24h": [
            {"time": "00:00", "pm25": 58.2},
            {"time": "03:00", "pm25": 62.0},
            {"time": "06:00", "pm25": 69.5},
            {"time": "09:00", "pm25": 81.4},
            {"time": "12:00", "pm25": 74.0},
            {"time": "15:00", "pm25": 68.2},
            {"time": "18:00", "pm25": 76.8},
            {"time": "21:00", "pm25": 75.1},
            {"time": "Now", "pm25": 72.4}
        ]
    },
    {
        "id": "central-silk-board",
        "name": "Central Silk Board",
        "zone": "south",
        "zone_label": "South-East Arterial",
        "ward": "Ward 174 - Flyover Junction",
        "pm25": 91.8,
        "pm10": 146.0,
        "no2": 45.8,
        "so2": 18.2,
        "co": 1.9,
        "o3": 22.0,
        "temperature": 30.4,
        "humidity": 58,
        "wind_speed": 0.8,
        "wind_direction": "E",
        "microclimate": "30.4°C • 58% RH • 0.8 m/s E",
        "sensor_array": "Dual Beta BAM",
        "status": "Active • Stagnation Hub",
        "updated": "3m ago",
        "trend_24h": [
            {"time": "00:00", "pm25": 82.0},
            {"time": "03:00", "pm25": 85.5},
            {"time": "06:00", "pm25": 94.2},
            {"time": "09:00", "pm25": 108.6},
            {"time": "12:00", "pm25": 96.0},
            {"time": "15:00", "pm25": 89.4},
            {"time": "18:00", "pm25": 98.2},
            {"time": "21:00", "pm25": 93.8},
            {"time": "Now", "pm25": 91.8}
        ]
    },
    {
        "id": "peenya",
        "name": "Peenya Industrial",
        "zone": "west",
        "zone_label": "West Industrial",
        "ward": "Phase II - Metal Cluster",
        "pm25": 88.5,
        "pm10": 152.4,
        "no2": 41.2,
        "so2": 24.8,
        "co": 2.1,
        "o3": 19.5,
        "temperature": 31.2,
        "humidity": 52,
        "wind_speed": 2.2,
        "wind_direction": "NW",
        "microclimate": "31.2°C • 52% RH • 2.2 m/s NW",
        "sensor_array": "Laser Scintillation",
        "status": "Active • Validated",
        "updated": "1m ago",
        "trend_24h": [
            {"time": "00:00", "pm25": 78.5},
            {"time": "03:00", "pm25": 82.1},
            {"time": "06:00", "pm25": 91.0},
            {"time": "09:00", "pm25": 102.4},
            {"time": "12:00", "pm25": 94.5},
            {"time": "15:00", "pm25": 86.0},
            {"time": "18:00", "pm25": 95.8},
            {"time": "21:00", "pm25": 90.2},
            {"time": "Now", "pm25": 88.5}
        ]
    },
    {
        "id": "cubbon-park",
        "name": "Cubbon Park Grove",
        "zone": "central",
        "zone_label": "Central Eco-Core",
        "ward": "Bamboo Pavilion Sector",
        "pm25": 22.1,
        "pm10": 48.3,
        "no2": 14.2,
        "so2": 8.1,
        "co": 0.6,
        "o3": 38.0,
        "temperature": 25.3,
        "humidity": 74,
        "wind_speed": 2.6,
        "wind_direction": "S",
        "microclimate": "25.3°C • 74% RH • 2.6 m/s S",
        "sensor_array": "Grimm Spectrometer",
        "status": "Active • Reference Base",
        "updated": "4m ago",
        "trend_24h": [
            {"time": "00:00", "pm25": 18.5},
            {"time": "03:00", "pm25": 19.2},
            {"time": "06:00", "pm25": 24.0},
            {"time": "09:00", "pm25": 28.5},
            {"time": "12:00", "pm25": 25.1},
            {"time": "15:00", "pm25": 21.0},
            {"time": "18:00", "pm25": 26.4},
            {"time": "21:00", "pm25": 23.8},
            {"time": "Now", "pm25": 22.1}
        ]
    },
    {
        "id": "jayanagar",
        "name": "Jayanagar 4th Block",
        "zone": "south",
        "zone_label": "South Residential",
        "ward": "Residential Green Belt",
        "pm25": 45.0,
        "pm10": 82.3,
        "no2": 22.4,
        "so2": 11.2,
        "co": 0.9,
        "o3": 32.4,
        "temperature": 27.6,
        "humidity": 68,
        "wind_speed": 1.5,
        "wind_direction": "SSE",
        "microclimate": "27.6°C • 68% RH • 1.5 m/s SSE",
        "sensor_array": "Laser Resonator",
        "status": "Active • Validated",
        "updated": "2m ago",
        "trend_24h": [
            {"time": "00:00", "pm25": 38.0},
            {"time": "03:00", "pm25": 41.2},
            {"time": "06:00", "pm25": 48.6},
            {"time": "09:00", "pm25": 54.0},
            {"time": "12:00", "pm25": 47.5},
            {"time": "15:00", "pm25": 42.0},
            {"time": "18:00", "pm25": 49.8},
            {"time": "21:00", "pm25": 46.2},
            {"time": "Now", "pm25": 45.0}
        ]
    },
    {
        "id": "hebbal",
        "name": "Hebbal Interchange",
        "zone": "north",
        "zone_label": "North Corridor",
        "ward": "Airport Expressway Core",
        "pm25": 54.2,
        "pm10": 104.0,
        "no2": 31.0,
        "so2": 13.6,
        "co": 1.4,
        "o3": 29.1,
        "temperature": 28.9,
        "humidity": 60,
        "wind_speed": 3.1,
        "wind_direction": "NE",
        "microclimate": "28.9°C • 60% RH • 3.1 m/s NE",
        "sensor_array": "BAM 1020",
        "status": "Active • Validated",
        "updated": "5m ago",
        "trend_24h": [
            {"time": "00:00", "pm25": 46.0},
            {"time": "03:00", "pm25": 49.5},
            {"time": "06:00", "pm25": 58.2},
            {"time": "09:00", "pm25": 66.0},
            {"time": "12:00", "pm25": 56.4},
            {"time": "15:00", "pm25": 50.8},
            {"time": "18:00", "pm25": 61.2},
            {"time": "21:00", "pm25": 55.9},
            {"time": "Now", "pm25": 54.2}
        ]
    },
    {
        "id": "kasturi-nagar",
        "name": "Kasturi Nagar",
        "zone": "east",
        "zone_label": "East Tech Corridor",
        "ward": "Outer Ring Road Corridor",
        "pm25": 49.8,
        "pm10": 94.1,
        "no2": 28.3,
        "so2": 12.0,
        "co": 1.1,
        "o3": 30.5,
        "temperature": 29.1,
        "humidity": 63,
        "wind_speed": 2.0,
        "wind_direction": "E",
        "microclimate": "29.1°C • 63% RH • 2.0 m/s E",
        "sensor_array": "Hybrid Optical",
        "status": "Active • Validated",
        "updated": "2m ago",
        "trend_24h": [
            {"time": "00:00", "pm25": 42.0},
            {"time": "03:00", "pm25": 45.1},
            {"time": "06:00", "pm25": 52.8},
            {"time": "09:00", "pm25": 60.4},
            {"time": "12:00", "pm25": 51.2},
            {"time": "15:00", "pm25": 46.0},
            {"time": "18:00", "pm25": 55.6},
            {"time": "21:00", "pm25": 51.0},
            {"time": "Now", "pm25": 49.8}
        ]
    },
    {
        "id": "hombegowda-nagar",
        "name": "Hombegowda Nagar",
        "zone": "south",
        "zone_label": "Institutional South",
        "ward": "NIMHANS Adjacent Belt",
        "pm25": 41.5,
        "pm10": 76.0,
        "no2": 24.1,
        "so2": 10.8,
        "co": 0.8,
        "o3": 33.2,
        "temperature": 27.0,
        "humidity": 71,
        "wind_speed": 1.7,
        "wind_direction": "SE",
        "microclimate": "27.0°C • 71% RH • 1.7 m/s SE",
        "sensor_array": "Attenuation Monitor",
        "status": "Active • Validated",
        "updated": "6m ago",
        "trend_24h": [
            {"time": "00:00", "pm25": 35.0},
            {"time": "03:00", "pm25": 38.2},
            {"time": "06:00", "pm25": 44.5},
            {"time": "09:00", "pm25": 51.0},
            {"time": "12:00", "pm25": 43.8},
            {"time": "15:00", "pm25": 39.2},
            {"time": "18:00", "pm25": 47.0},
            {"time": "21:00", "pm25": 42.8},
            {"time": "Now", "pm25": 41.5}
        ]
    },
    {
        "id": "whitefield",
        "name": "Whitefield Export Zone",
        "zone": "east",
        "zone_label": "East Tech Corridor",
        "ward": "ITPL Main Road",
        "pm25": 62.1,
        "pm10": 112.5,
        "no2": 34.6,
        "so2": 16.0,
        "co": 1.5,
        "o3": 27.2,
        "temperature": 30.1,
        "humidity": 56,
        "wind_speed": 1.4,
        "wind_direction": "E",
        "microclimate": "30.1°C • 56% RH • 1.4 m/s E",
        "sensor_array": "Laser Particle Counter",
        "status": "Active • Validated",
        "updated": "3m ago",
        "trend_24h": [
            {"time": "00:00", "pm25": 52.0},
            {"time": "03:00", "pm25": 55.8},
            {"time": "06:00", "pm25": 66.4},
            {"time": "09:00", "pm25": 74.0},
            {"time": "12:00", "pm25": 64.8},
            {"time": "15:00", "pm25": 58.5},
            {"time": "18:00", "pm25": 68.2},
            {"time": "21:00", "pm25": 64.0},
            {"time": "Now", "pm25": 62.1}
        ]
    },
    {
        "id": "electronic-city",
        "name": "Electronic City Phase 1",
        "zone": "south",
        "zone_label": "South Tech Corridor",
        "ward": "Hosur Road Expressway",
        "pm25": 58.4,
        "pm10": 108.0,
        "no2": 33.1,
        "so2": 14.2,
        "co": 1.3,
        "o3": 28.8,
        "temperature": 29.5,
        "humidity": 59,
        "wind_speed": 1.6,
        "wind_direction": "SE",
        "microclimate": "29.5°C • 59% RH • 1.6 m/s SE",
        "sensor_array": "Dual Beta BAM",
        "status": "Active • Validated",
        "updated": "4m ago",
        "trend_24h": [
            {"time": "00:00", "pm25": 48.0},
            {"time": "03:00", "pm25": 52.0},
            {"time": "06:00", "pm25": 62.1},
            {"time": "09:00", "pm25": 70.5},
            {"time": "12:00", "pm25": 60.8},
            {"time": "15:00", "pm25": 54.2},
            {"time": "18:00", "pm25": 64.5},
            {"time": "21:00", "pm25": 60.0},
            {"time": "Now", "pm25": 58.4}
        ]
    },
    {
        "id": "yelahanka",
        "name": "Yelahanka New Town",
        "zone": "north",
        "zone_label": "North Sector",
        "ward": "Suburban Green Belt",
        "pm25": 32.5,
        "pm10": 64.0,
        "no2": 18.5,
        "so2": 9.4,
        "co": 0.7,
        "o3": 36.1,
        "temperature": 26.4,
        "humidity": 72,
        "wind_speed": 2.8,
        "wind_direction": "N",
        "microclimate": "26.4°C • 72% RH • 2.8 m/s N",
        "sensor_array": "Optical Particle Sampler",
        "status": "Active • Validated",
        "updated": "1m ago",
        "trend_24h": [
            {"time": "00:00", "pm25": 26.0},
            {"time": "03:00", "pm25": 28.5},
            {"time": "06:00", "pm25": 35.0},
            {"time": "09:00", "pm25": 40.2},
            {"time": "12:00", "pm25": 34.0},
            {"time": "15:00", "pm25": 30.5},
            {"time": "18:00", "pm25": 36.8},
            {"time": "21:00", "pm25": 34.1},
            {"time": "Now", "pm25": 32.5}
        ]
    },
    {
        "id": "kengeri",
        "name": "Mysuru Road Kengeri",
        "zone": "west",
        "zone_label": "West Transit Corridor",
        "ward": "Transit Hub Hubballi Line",
        "pm25": 51.0,
        "pm10": 98.4,
        "no2": 29.4,
        "so2": 12.8,
        "co": 1.2,
        "o3": 31.0,
        "temperature": 28.5,
        "humidity": 64,
        "wind_speed": 2.1,
        "wind_direction": "W",
        "microclimate": "28.5°C • 64% RH • 2.1 m/s W",
        "sensor_array": "Laser Scintillation",
        "status": "Active • Validated",
        "updated": "5m ago",
        "trend_24h": [
            {"time": "00:00", "pm25": 44.0},
            {"time": "03:00", "pm25": 47.0},
            {"time": "06:00", "pm25": 54.8},
            {"time": "09:00", "pm25": 62.0},
            {"time": "12:00", "pm25": 53.5},
            {"time": "15:00", "pm25": 48.0},
            {"time": "18:00", "pm25": 56.4},
            {"time": "21:00", "pm25": 52.5},
            {"time": "Now", "pm25": 51.0}
        ]
    }
]

class StationService:
    @staticmethod
    def get_all_stations():
        """Returns simplified list for selectors."""
        return [
            {"id": st["id"], "name": st["name"], "zone": st["zone"], "ward": st["ward"]}
            for st in STATIONS_DATA
        ]

    @staticmethod
    def get_station_by_id(station_id):
        """Returns detailed station payload for a specific station_id."""
        if not station_id:
            station_id = "btm-layout"
            
        station_id = str(station_id).lower().strip()
        
        target = None
        for st in STATIONS_DATA:
            if st["id"] == station_id or st["name"].lower().replace(" ", "-") == station_id:
                target = st
                break

        if not target:
            target = STATIONS_DATA[0] # Fallback to BTM Layout

        aqi = AirQualityService.calculate_aqi(target["pm25"])
        cat_info = AirQualityService.get_aqi_category(aqi)

        res = dict(target)
        res["aqi"] = aqi
        res["category"] = cat_info["category"]
        res["category_label"] = cat_info["label"]
        res["category_bg"] = cat_info["bg"]
        res["category_text"] = cat_info["text"]
        res["badge_bg"] = cat_info["badge_bg"]
        res["badge_text"] = cat_info["badge_text"]
        res["description"] = f"Air quality is currently {cat_info['label'].lower()} at {target['name']}. {cat_info['description']}"
        return res

    @staticmethod
    def get_stations(zone_filter="all", query=None):
        processed = []
        for st in STATIONS_DATA:
            if zone_filter != "all" and st["zone"] != zone_filter:
                continue
            if query:
                q = query.lower().strip()
                if q not in st["name"].lower() and q not in st["ward"].lower() and q not in st["id"].lower():
                    continue

            aqi = AirQualityService.calculate_aqi(st["pm25"])
            cat_info = AirQualityService.get_aqi_category(aqi)

            item = dict(st)
            item["aqi"] = aqi
            item["category"] = cat_info["category"]
            item["category_label"] = cat_info["label"]
            item["category_bg"] = cat_info["bg"]
            item["category_text"] = cat_info["text"]
            item["badge_bg"] = cat_info["badge_bg"]
            item["badge_text"] = cat_info["badge_text"]
            processed.append(item)

        return {
            "total": len(processed),
            "stations": processed
        }
