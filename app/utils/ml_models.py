import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

class WaterQualityPredictor:
    def __init__(self, model_path='water_quality_model.joblib'):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.model_path = model_path
        self.feature_columns = None
        self.target_column = None
        
    def preprocess_data(self, df, target_column):
        df_processed = df.copy()
        categorical_cols = df_processed.select_dtypes(include=['object', 'category']).columns.tolist()
        
        for col in categorical_cols:
            if col != target_column:
                self.label_encoders[col] = LabelEncoder()
                df_processed[col] = self.label_encoders[col].fit_transform(df_processed[col].astype(str))
        
        X = df_processed.drop(columns=[target_column])
        y = df_processed[target_column]
        
        self.feature_columns = X.columns.tolist()
        self.target_column = target_column
        
        return X, y
    
    def train_model(self, X, y, test_size=0.2, random_state=42):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model = RandomForestRegressor(n_estimators=100, random_state=random_state)
        self.model.fit(X_train_scaled, y_train)
        
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        return {'mse': mse, 'r2': r2, 'features_importance': dict(zip(X.columns, self.model.feature_importances_))}
    
    def predict(self, input_data):
        if not isinstance(input_data, pd.DataFrame):
            input_data = pd.DataFrame([input_data])
        
        for col, encoder in self.label_encoders.items():
            if col in input_data.columns:
                input_data[col] = input_data[col].map(lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1)
        
        for col in self.feature_columns:
            if col not in input_data.columns:
                input_data[col] = 0
        
        input_data = input_data[self.feature_columns]
        input_scaled = self.scaler.transform(input_data)
        return self.model.predict(input_scaled)[0]
    
    def save_model(self, path=None):
        path = path or self.model_path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns,
            'target_column': self.target_column
        }, path)
    
    def load_model(self, path=None):
        path = path or self.model_path
        loaded_data = joblib.load(path)
        self.model = loaded_data['model']
        self.scaler = loaded_data['scaler']
        self.label_encoders = loaded_data['label_encoders']
        self.feature_columns = loaded_data['feature_columns']
        self.target_column = loaded_data['target_column']
        return self
