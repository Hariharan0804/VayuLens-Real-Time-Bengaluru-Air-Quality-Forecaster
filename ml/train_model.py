import os
import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'VayuLens_Training_Dataset.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
MODEL_FILE = os.path.join(MODEL_DIR, 'vayulens_model.pkl')
METADATA_FILE = os.path.join(MODEL_DIR, 'model_metadata.json')

def train_model():
    print("Loading dataset...")
    df = pd.read_csv(DATA_FILE)
    
    # Process timestamp
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values(by='Timestamp')
    
    # Identify numerical features and target
    target = 'PM2.5_Next_Hour'
    if target not in df.columns:
        raise ValueError(f"Target column {target} not found in dataset.")
    
    # Select features - dropping non-numerical or ID columns
    drop_cols = ['Timestamp', 'Station ID', 'State', 'City', 'Station Name', target]
    features = [col for col in df.columns if col not in drop_cols and pd.api.types.is_numeric_dtype(df[col])]
    
    print(f"Features ({len(features)}): {features}")
    
    # Handle missing values
    df[features] = df[features].fillna(df[features].median())
    df = df.dropna(subset=[target])
    
    # Time-aware split (80/20)
    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    X_train, y_train = train_df[features], train_df[target]
    X_test, y_test = test_df[features], test_df[target]
    
    print(f"Training on {len(X_train)} rows, testing on {len(X_test)} rows.")
    
    # Train model
    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluation
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    
    print(f"Evaluation: MAE={mae:.4f}, RMSE={rmse:.4f}, R2={r2:.4f}")
    
    # Save model
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_FILE)
    
    # Feature importance
    importance = dict(zip(features, model.feature_importances_))
    # convert np.float64 to float for json
    importance = {k: float(v) for k, v in importance.items()}
    
    import sklearn
    # Save metadata
    metadata = {
        "model_name": "RandomForestRegressor",
        "target": target,
        "features": features,
        "training_rows": len(X_train),
        "testing_rows": len(X_test),
        "MAE": float(mae),
        "RMSE": float(rmse),
        "R2": float(r2),
        "training_timestamp": datetime.now().isoformat(),
        "sklearn_version": sklearn.__version__,
        "feature_importance": importance
    }
    
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print("Model and metadata saved successfully.")

if __name__ == "__main__":
    train_model()
