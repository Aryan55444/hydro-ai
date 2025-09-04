import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv 
import os
from app.utils.helpers import get_data_summary
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
            context_prompt = f"""
            You are a professional water quality analyst. Use ONLY the dataset text provided.
            Scope:
            - Gujarat data only.
            - If a district is mentioned, focus on that district within Gujarat.
            - If no district is specified, give Gujarat-wide analysis.
            - Ignore other states and external knowledge.

            Dataset (Gujarat) Summary:
            {data_summary}

            User Request: {prompt}

            Provide a concise, quantitative answer based solely on the dataset. If a metric is unavailable, say so briefly.
            """
            response = model.generate_content(context_prompt)
            response_text = response.text
            st.markdown(response_text)
            log_query("response", {"prompt": prompt, "response": response_text})
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
