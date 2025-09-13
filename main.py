import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv 
import os
import joblib
import numpy as np
import tempfile
from datetime import datetime
from app.utils.helpers import get_data_summary
from app.utils.ml_models import preprocess_data, load_model, train_model, predict, save_model
from app.utils.report_generator import generate_prediction_report
from app.utils.ui_components import (
    apply_theme, create_header, create_sidebar_header, 
    metric_card, loading_spinner, info_card
)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

df = pd.read_csv(f"F:\\study\\hydro ai\\data\\gujarat_groundwater_merged_final.csv")

apply_theme()
create_header()
create_sidebar_header()

info_card(
    "About This Dataset",
    "This dashboard analyzes groundwater quality data from Gujarat, India. "
    "Explore the data, get insights, and make predictions using the tools below.",
    "info"
)

tab1, tab2 = st.tabs(["💬 Chat Analysis", "📊 ML Predictions"])

data_summary = get_data_summary(df)

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Samples", f"{len(df):,}", icon="dataset")
    with col2:
        metric_card("Features", f"{len(df.columns)}", icon="category")
    with col3:
        numeric_cols = len(df.select_dtypes(include=['int64', 'float64']).columns)
        metric_card("Numeric Features", str(numeric_cols), icon="calculate")
    with col4:
        cat_cols = len(df.select_dtypes(include=['object', 'category']).columns)
        metric_card("Categorical Features", str(cat_cols), icon="list")

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
    st.markdown("##  Water Quality Prediction")
    st.markdown("Leverage machine learning to predict and analyze water quality parameters with high accuracy.")
    
    info_card(
        "How to Use",
        "Select a target variable and input features, then click 'Train Model' to create predictions. "
        "The model will show performance metrics and allow you to make new predictions.",
        "help_outline"
    )
    
    if 'ml_model' not in st.session_state:
        st.session_state.ml_model = None
    if 'model_trained' not in st.session_state:
        st.session_state.model_trained = False
    
    with st.sidebar:
        st.markdown("###  Target Variable")
        target_column = st.selectbox(
            "Select target variable to predict:",
            [col for col in df.select_dtypes(include=['float64', 'int64']).columns],
            help="Choose the water quality parameter you want to predict."
        )
        
        st.markdown("---")
        st.markdown("###  Model Settings")
        
        test_size = st.slider(
            "Test Set Size (%)",
            min_value=10,
            max_value=50,
            value=20,
            step=5,
            help="Percentage of data to use for testing the model"
        )
        
        n_estimators = st.slider(
            "Number of Trees",
            min_value=10,
            max_value=200,
            value=100,
            step=10,
            help="Number of trees in the random forest"
        )
        
        if st.button("Train Model"):
            with st.spinner("Training model... This may take a few minutes."):
                X, y, label_encoders, feature_columns = preprocess_data(df, target_column)
                model, scaler, metrics = train_model(X, y, label_encoders, test_size=test_size/100, n_estimators=n_estimators)
                st.session_state.ml_model = {
                    'model': model,
                    'scaler': scaler,
                    'label_encoders': label_encoders,
                    'feature_columns': feature_columns,
                    'target_column': target_column,
                    'metrics': metrics
                }
                st.session_state.model_trained = True
                st.rerun()
    
    if st.session_state.model_trained and st.session_state.ml_model:
        metrics = st.session_state.ml_model['metrics']
        col1, col2, col3 = st.columns(3)
        with col1:
            metric_card("R² Score", f"{metrics['r2']:.3f}", trend='up' if metrics['r2'] > 0.7 else 'down')
        with col2:
            metric_card("MAE", f"{metrics['mae']:.3f}", trend='down' if metrics['mae'] < 0.5 else 'up')
        with col3:
            # Format MSE to show full value without scientific notation
            mse_formatted = f"{metrics['mse']:.2f}" if metrics['mse'] < 1000 else f"{int(metrics['mse']):,}"
            # Use a more appropriate threshold for MSE trend (lower is better)
            mse_trend = 'down' if metrics['mse'] < 100 else 'up'
            metric_card("MSE", mse_formatted, trend=mse_trend)
        
        st.markdown("### Feature Importance")
        feature_importance = pd.DataFrame({
            'Feature': st.session_state.ml_model['feature_columns'],
            'Importance': st.session_state.ml_model['model'].feature_importances_
        }).sort_values('Importance', ascending=False)
        st.bar_chart(feature_importance.set_index('Feature')['Importance'])
        
        st.markdown("### Make a Prediction")
        with st.form("prediction_form"):
            input_data = {}
            for feature in st.session_state.ml_model['feature_columns']:
                if feature in df.select_dtypes(include=['float64', 'int64']).columns:
                    input_data[feature] = st.number_input(
                        f"{feature}:",
                        min_value=float(df[feature].min()),
                        max_value=float(df[feature].max()),
                        value=float(df[feature].median())
                    )
                else:
                    input_data[feature] = st.selectbox(
                        f"{feature}:",
                        options=df[feature].unique()
                    )
            
            submit_button = st.form_submit_button("Make Prediction")
            
            if submit_button:
                # Make prediction
                prediction = predict(
                    input_data,
                    st.session_state.ml_model['model'],
                    st.session_state.ml_model['scaler'],
                    st.session_state.ml_model['label_encoders']
                )
                
                target_values = df[st.session_state.ml_model['target_column']].dropna()
                percentile = (target_values < prediction).mean() * 100
                
                st.write(f"### Prediction Details")
                st.write(f"- **Predicted Value**: {prediction[0]:.4f}")
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
                
                analysis_prompt = f"""
                You are a water quality expert. Analyze the following prediction results and provide a professional assessment:
                
                Parameter: {st.session_state.ml_model['target_column']}
                Predicted Value: {prediction[0]:.4f}
                
                Dataset Statistics:
                - Minimum: {target_values.min():.4f}
                - 25th Percentile: {target_values.quantile(0.25):.4f}
                - Median: {target_values.median():.4f}
                - 75th Percentile: {target_values.quantile(0.75):.4f}
                - Maximum: {target_values.max():.4f}
                - Percentile Rank: {percentile:.1f}%
                
                Feature Values:
                """
                
                for feature, value in input_data.items():
                    analysis_prompt += f"- {feature}: {value}\n"
                    
                analysis_prompt += "\nProvide a detailed analysis of this prediction, including potential implications and recommendations."
            
            with st.spinner("Generating professional analysis..."):
                model = genai.GenerativeModel("gemini-1.5-flash")
                analysis_response = model.generate_content(analysis_prompt)
                analysis_text = analysis_response.text
                
                st.subheader("Professional Analysis")
                st.write(analysis_text)
                
                with st.spinner("Generating PDF report..."):
                    prediction_data = {
                        'target_column': st.session_state.ml_model['target_column'],
                        'prediction': prediction,
                        'stats': {
                            'min': target_values.min(),
                            '25%': target_values.quantile(0.25),
                            '50%': target_values.median(),
                            '75%': target_values.quantile(0.75),
                            'max': target_values.max(),
                        },
                        'percentile': percentile,
                        'features': input_data
                    }
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        report_path = generate_prediction_report(
                            prediction_data=prediction_data,
                            analysis_text=analysis_text,
                            output_path=tmp_file.name
                        )
                    
                    with open(report_path, 'rb') as f:
                        st.download_button(
                            label="📥 Download Full Report (PDF)",
                            data=f,
                            file_name=f"water_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime='application/pdf'
                        )
                    
                    try:
                        os.unlink(report_path)
                    except:
                        pass
