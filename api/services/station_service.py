from datetime import datetime
from .openaq_service import OpenAQService

STATIONS_DATA = [
    {
        "id": "CA-BLR-004",
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
        "microclimate": "28.1°C • 66% RH • 1.9 m/s SE",
        "sensor_array": "Optical Laser Particle",
        "status": "Active • Validated",
        "updated": "2m ago"
    },
    {
        "id": "CA-BLR-001",
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
        "microclimate": "30.4°C • 58% RH • 0.8 m/s E",
        "sensor_array": "Dual Beta BAM",
        "status": "Active • Stagnation Hub",
        "updated": "3m ago"
    },
    {
        "id": "CA-BLR-008",
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
        "microclimate": "31.2°C • 52% RH • 2.2 m/s NW",
        "sensor_array": "Laser Scintillation",
        "status": "Active • Validated",
        "updated": "1m ago"
    },
    {
        "id": "CA-BLR-012",
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
        "microclimate": "25.3°C • 74% RH • 2.6 m/s S",
        "sensor_array": "Grimm Spectrometer",
        "status": "Active • Reference Base",
        "updated": "4m ago"
    },
    {
        "id": "CA-BLR-003",
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
        "microclimate": "27.6°C • 68% RH • 1.5 m/s SSE",
        "sensor_array": "Laser Resonator",
        "status": "Active • Validated",
        "updated": "2m ago"
    },
    {
        "id": "CA-BLR-007",
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
        "microclimate": "28.9°C • 60% RH • 3.1 m/s NE",
        "sensor_array": "BAM 1020",
        "status": "Active • Validated",
        "updated": "5m ago"
    },
    {
        "id": "CA-BLR-009",
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
        "microclimate": "29.1°C • 63% RH • 2.0 m/s E",
        "sensor_array": "Hybrid Optical",
        "status": "Active • Validated",
        "updated": "2m ago"
    },
    {
        "id": "CA-BLR-005",
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
        "microclimate": "27.0°C • 71% RH • 1.7 m/s SE",
        "sensor_array": "Attenuation Monitor",
        "status": "Active • Validated",
        "updated": "6m ago"
    },
    {
        "id": "CA-BLR-010",
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
        "microclimate": "30.1°C • 56% RH • 1.4 m/s E",
        "sensor_array": "Laser Particle Counter",
        "status": "Active • Validated",
        "updated": "3m ago"
    },
    {
        "id": "CA-BLR-011",
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
        "microclimate": "29.5°C • 59% RH • 1.6 m/s SE",
        "sensor_array": "Dual Beta BAM",
        "status": "Active • Validated",
        "updated": "4m ago"
    },
    {
        "id": "CA-BLR-002",
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
        "microclimate": "26.4°C • 72% RH • 2.8 m/s N",
        "sensor_array": "Optical Particle Sampler",
        "status": "Active • Validated",
        "updated": "1m ago"
    },
    {
        "id": "CA-BLR-006",
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
        "microclimate": "28.5°C • 64% RH • 2.1 m/s W",
        "sensor_array": "Laser Scintillation",
        "status": "Active • Validated",
        "updated": "5m ago"
    }
]

class StationService:
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

            aqi = OpenAQService.calculate_aqi(st["pm25"])
            cat_info = OpenAQService.get_aqi_category(aqi)

            item = dict(st)
            item["aqi"] = aqi
            item["category"] = cat_info["category"]
            item["category_bg"] = cat_info["bg"]
            item["category_text"] = cat_info["text"]
            processed.append(item)

        return {
            "total": len(processed),
            "stations": processed
        }
