import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv 
import os
import joblib
import numpy as np
from datetime import datetime
from app.utils.helpers import get_data_summary
from app.utils.ml_models import preprocess_data, train_model, predict, save_model, load_model

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

df = pd.read_csv(f"F:\\study\\hydro ai\\data\\gujarat_groundwater_merged_final.csv")

st.set_page_config(page_title="Water Quality Expert")
st.title("Groundwater Quality Analysis Platform")
st.subheader("Professional water quality assessment, predictions, and regional analysis")

tab1, tab2 = st.tabs(["Chat Analysis", "ML Predictions"])

data_summary = get_data_summary(df)

with tab1:
    st.success(f"Dataset loaded: {len(df):,} groundwater samples")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask about Gujarat groundwater (add a district to focus)...")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            model = genai.GenerativeModel("gemini-1.5-flash")
            district_col = next((col for col in df.columns if 'district' in col.lower() or 'location' in col.lower()), None)
            district_names = df[district_col].unique().astype(str).tolist() if district_col is not None else []
            city = next((word for word in prompt.split() if word.lower() in [name.lower() for name in district_names]), None)
            
            if city and district_col:
                city_data = df[df[district_col].str.lower() == city.lower()].copy()
                city_summary = city_data.describe(include='all').to_string()
                sample_data = city_data.head(5).to_string()
                
                context_prompt = f"""
                You are a water quality expert analyzing groundwater data for {city}. 
                
                City Data Summary:
                - Total samples: {len(city_data):,}
                - Data columns: {', '.join(city_data.columns)}
                
                Sample Data (first 5 rows):
                {sample_data}
                
                Statistics:
                {city_summary}
                
                User Request: {prompt}
                
                Provide a clear, concise analysis focusing on key metrics. 
                Keep the response under 100 lines. Highlight any concerning water quality issues.
                """
            else:
                context_prompt = f"""
                You are a water quality expert analyzing Gujarat groundwater data. Use ONLY the dataset text provided.
                
                Dataset Summary:
                {data_summary}
                
                User Request: {prompt}
                
                Provide a clear, quantitative answer with specific numbers when possible. 
                If a city is mentioned, focus on that city's data. 
                Keep the response under 250 lines.
                """
            response = model.generate_content(context_prompt)
            response_text = response.text
            st.markdown(response_text)
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})

with tab2:
    st.header("Water Quality Prediction")
    st.write("Use machine learning to predict water quality parameters.")
    
    if 'ml_model' not in st.session_state:
        st.session_state.ml_model = None
    if 'model_trained' not in st.session_state:
        st.session_state.model_trained = False
    
    with st.sidebar:
        st.subheader("Model Configuration")
        target_column = st.selectbox("Select target variable to predict:", 
                                   [col for col in df.select_dtypes(include=['float64', 'int64']).columns])
        
        if st.button("Train Model"):
            with st.spinner("Training model... This may take a few minutes."):
                X, y, label_encoders, feature_columns = preprocess_data(df, target_column)
                model, scaler, metrics = train_model(X, y, label_encoders)
                st.session_state.ml_model = {
                    'model': model,
                    'scaler': scaler,
                    'label_encoders': label_encoders,
                    'feature_columns': feature_columns,
                    'target_column': target_column
                }
                st.session_state.model_trained = True
                st.success("Model trained successfully!")
                st.metric("R² Score", f"{metrics['r2']:.3f}")
                st.metric("Mean Squared Error", f"{metrics['mse']:.4f}")
                
                st.subheader("Feature Importance")
                feature_importance = pd.DataFrame({
                    'Feature': list(metrics['feature_importances'].keys()),
                    'Importance': list(metrics['feature_importances'].values())
                }).sort_values('Importance', ascending=False)
                st.bar_chart(feature_importance.set_index('Feature'))
    
    st.subheader("Make a Prediction")
    
    if not st.session_state.model_trained:
        st.warning("Please train a model using the sidebar first.")
    else:
        input_data = {}
        col1, col2 = st.columns(2)
        
        features = st.session_state.ml_model['feature_columns']
        for i, feature in enumerate(features):
            col = col1 if i % 2 == 0 else col2
            with col:
                if feature in df.select_dtypes(include=['object', 'category']).columns:
                    input_data[feature] = st.selectbox(f"{feature}:", options=df[feature].unique())
                else:
                    min_val = float(df[feature].min())
                    max_val = float(df[feature].max())
                    mean_val = float(df[feature].mean())
                    input_data[feature] = st.number_input(
                        f"{feature}:",
                        min_value=min_val,
                        max_value=max_val,
                        value=mean_val,
                        step=(max_val - min_val) / 100
                    )
        
        if st.button("Predict"):
            prediction = predict(
                input_data,
                st.session_state.ml_model['model'],
                st.session_state.ml_model['scaler'],
                st.session_state.ml_model['label_encoders'],
                st.session_state.ml_model['feature_columns']
            )
            st.success(f"Predicted {st.session_state.ml_model['target_column']}: **{prediction:.4f}**")
            st.subheader("Prediction Context")
            
            target_values = df[st.session_state.ml_model['target_column']].dropna()
            percentile = (target_values < prediction).mean() * 100
            
            st.write(f"### Prediction Details")
            st.write(f"- **Predicted Value**: {prediction:.4f}")
            st.write(f"- **Dataset Statistics for {st.session_state.ml_model['target_column']}:**")
            st.write(f"  - Minimum: {target_values.min():.4f}")
            st.write(f"  - 25th Percentile: {target_values.quantile(0.25):.4f}")
            st.write(f"  - Median: {target_values.median():.4f}")
            st.write(f"  - 75th Percentile: {target_values.quantile(0.75):.4f}")
            st.write(f"  - Maximum: {target_values.max():.4f}")
            st.write(f"- **Percentile Rank**: Your prediction is higher than {percentile:.1f}% of values in the dataset.")
            
            if percentile < 25:
                st.info("This is a relatively low prediction compared to the dataset.")
            elif percentile > 75:
                st.warning("This is a relatively high prediction compared to the dataset.")
            else:
                st.info("This prediction is within the typical range of values in the dataset.")
