# VayuLens

**Real-Time Bengaluru Air Quality Forecaster**

## Project Overview
VayuLens is an advanced AI-powered web application for real-time and predictive air quality monitoring in Bengaluru. It integrates real-time environmental data with machine learning forecasts using a clean, modern Django backend architecture.

## Features
- **Dashboard**: High-level overview of live AQI and predictive forecasts.
- **Live Monitoring**: Detailed telemetry from CPCB/KSPCB and OpenAQ stations.
- **Air Quality Forecast**: Next-hour PM2.5 forecasting powered by Random Forest Regression.
- **Historical Analysis**: Deep dive into air quality trends over time.
- **Monitoring Stations**: Network directory of air quality sensors.
- **Model Insights**: Detailed breakdown of machine learning model metrics (MAE, RMSE, R²).

## Architecture
- **Backend**: Django 5 + Django REST Framework
- **Machine Learning**: Scikit-learn (RandomForestRegressor), Pandas, NumPy
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript, Chart.js
- **Server**: Gunicorn
- **Data Source**: OpenAQ API & historical fallback datasets

## ML Pipeline
1. Ingest historical Bengaluru air quality data.
2. Clean missing values and extract numerical features.
3. Train Random Forest Regressor targeting `PM2.5_Next_Hour`.
4. Output model metadata and serialized `.pkl` for prediction endpoints.

### Model Metrics
- MAE: ~4.39
- RMSE: ~6.32
- R²: ~0.86

## Local Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file with `OPENAQ_API_KEY`, `DEBUG`, `SECRET_KEY`
6. Run migrations: `python manage.py migrate`
7. Start server: `python manage.py runserver`

## Deployment
VayuLens is designed for seamless deployment on Render.
Use `render.yaml` and standard Render configuration for Python.
Start Command: `gunicorn config.wsgi:application`

## API Documentation
- `GET /api/health/`: Service status
- `GET /api/air-quality/current/`: Latest AQI metrics
- `GET /api/prediction/`: Model forecasts for next hour
- `GET /api/dashboard/live/`: Aggregated dashboard telemetry
- `GET /api/historical/`: Time-series air quality data
- `GET /api/stations/`: Station directory
- `GET /api/model/insights/`: ML feature importance and evaluation metrics
