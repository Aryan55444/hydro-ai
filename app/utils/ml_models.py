import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from typing import Dict, Tuple, Any, Union, Optional

def preprocess_data(df: pd.DataFrame, target_column: str) -> Tuple[pd.DataFrame, pd.Series, Dict, list]:
    df_processed = df.copy()
    categorical_cols = df_processed.select_dtypes(include=['object', 'category']).columns.tolist()
    label_encoders = {}
    
    for col in categorical_cols:
        if col != target_column:
            le = LabelEncoder()
            df_processed[col] = le.fit_transform(df_processed[col].astype(str))
            label_encoders[col] = le
    
    X = df_processed.drop(columns=[target_column])
    y = df_processed[target_column]
    feature_columns = X.columns.tolist()
    
    return X, y, label_encoders, feature_columns

def train_model(
    X: pd.DataFrame,
    y: pd.Series,
    label_encoders: Dict,
    test_size: float = 0.2,
    random_state: int = 42,
    n_estimators: int = 100
) -> Tuple[RandomForestRegressor, StandardScaler, Dict]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    metrics = {
        'mse': mse,
        'r2': r2,
        'mae': mae,
        'feature_importances': dict(zip(X.columns, model.feature_importances_))
    }
    
    return model, scaler, metrics

def predict(
    input_data: Union[Dict, pd.DataFrame],
    model: RandomForestRegressor,
    scaler: StandardScaler,
    label_encoders: Dict,
    feature_columns: list
) -> float:
    if not isinstance(input_data, pd.DataFrame):
        input_data = pd.DataFrame([input_data])
    
    for col, encoder in label_encoders.items():
        if col in input_data.columns:
            input_data[col] = input_data[col].map(
                lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1
            )
    
    for col in feature_columns:
        if col not in input_data.columns:
            input_data[col] = 0
    
    input_data = input_data[feature_columns]
    input_scaled = scaler.transform(input_data)
    return model.predict(input_scaled)[0]

def save_model(
    model: RandomForestRegressor,
    scaler: StandardScaler,
    label_encoders: Dict,
    feature_columns: list,
    target_column: str,
    path: str = 'water_quality_model.joblib'
) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump({
        'model': model,
        'scaler': scaler,
        'label_encoders': label_encoders,
        'feature_columns': feature_columns,
        'target_column': target_column
    }, path)

def load_model(path: str = 'water_quality_model.joblib') -> Dict[str, Any]:
    return