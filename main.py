import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv 
import os
from app.utils.helpers import get_data_summary

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


df = pd.read_csv(f"F:\\study\\hydro ai\\data\\gujarat_groundwater_merged_final.csv")

st.set_page_config(page_title="Water Quality Expert")
st.title("Groundwater Quality Analysis Platform")
st.subheader("Professional water quality assessment and regional analysis")

data_summary = get_data_summary(df)

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
            
            # Find district column name (case-insensitive)
            district_col = next((col for col in df.columns if 'district' in col.lower() or 'location' in col.lower()), None)
            
            # Get unique district names if column exists, otherwise use empty list
            district_names = df[district_col].unique().astype(str).tolist() if district_col is not None else []
            
            # Find city in prompt
            city = next(
                (word for word in prompt.split() 
                 if word.lower() in [name.lower() for name in district_names]),
                None
            )
            
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
                Keep the response under 100 lines.
                """
            response = model.generate_content(context_prompt)
            response_text = response.text
            st.markdown(response_text)
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
