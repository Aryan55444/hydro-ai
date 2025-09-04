import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv 
import os
from app.utils.helpers import get_data_summary, detect_user_type, get_tabular_data
from app.database.db import log_query

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
if google_api_key:
    genai.configure(api_key=google_api_key)
else:
    st.error("Please set your Google API key in the .env file")
    st.stop()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

df = pd.read_csv("F:\study\hydro ai\data\gujarat_groundwater_merged_final.csv")

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
    log_query("chat", {"prompt": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            user_type = detect_user_type(prompt)
            tabular_data = get_tabular_data(df, prompt)
            
            if user_type == "farmer":
                context_prompt = f"""
                You are a water quality expert helping farmers in Gujarat. Provide simple, practical advice.
                
                Scope:
                - Gujarat data only
                - Focus on practical farming implications
                - Use simple language
                - Provide actionable recommendations
                
                Dataset Summary:
                {data_summary}
                
                Tabular Data:
                {tabular_data}
                
                User Request: {prompt}
                
                Give a simple, practical answer with:
                1. Brief explanation in simple terms
                2. What it means for farming
                3. Any precautions or recommendations
                4. Keep it under 100 words
                """
            else:
                context_prompt = f"""
                You are a professional water quality researcher analyzing Gujarat groundwater data.
                
                Scope:
                - Gujarat data only
                - Provide comprehensive technical analysis
                - Include statistical insights
                - Reference specific data points
                
                Dataset Summary:
                {data_summary}
                
                Tabular Data:
                {tabular_data}
                
                User Request: {prompt}
                
                Provide a detailed technical analysis including:
                1. Statistical summary of relevant parameters
                2. Data patterns and trends
                3. Technical implications
                4. Research insights
                5. Include specific numbers and correlations
                """
            
            response = model.generate_content(context_prompt)
            response_text = response.text
            st.markdown(response_text)
            log_query("response", {"prompt": prompt, "response": response_text, "user_type": user_type})
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
