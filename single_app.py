import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv 
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

df = pd.read_csv("F:\\study\\hydro ai\\data\\gujarat_groundwater_merged_final.csv")

st.set_page_config(page_title="Water Quality Expert")
st.title("Groundwater Quality Analysis Platform")
st.subheader("Professional water quality assessment and regional analysis")

def get_data_summary(df: pd.DataFrame) -> str:
    states = df['STATE'].astype(str).str.strip().str.replace("\\s+", " ", regex=True).str.title() if 'STATE' in df.columns else pd.Series([])
    districts = df['DISTRICT'].astype(str).str.strip().str.replace("\\s+", " ", regex=True).str.title() if 'DISTRICT' in df.columns else pd.Series([])
    years = df['Year'] if 'Year' in df.columns else pd.Series([])
    num_states = states.nunique() if len(states) else 0
    num_districts = districts.nunique() if len(districts) else 0
    year_min = int(years.min()) if len(years) else "?"
    year_max = int(years.max()) if len(years) else "?"
    return f"""
    Loaded groundwater quality dataset with {len(df)} samples.

    Columns: {', '.join(df.columns.tolist())}

    Coverage:
    - States: {num_states}
    - Districts: {num_districts}
    - Years: {year_min}-{year_max}

    Sample data:
    {df.head(3).to_string()}
    """



summary = get_data_summary(df)

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
            context = f"""
            You are a water quality expert analyzing Gujarat groundwater data. Use ONLY the dataset text provided.

            Dataset Summary:
            {summary}

            User Request: {prompt}

            Provide a clear, quantitative answer with specific numbers when possible. If a metric is unavailable, say so briefly.
            """
            response = model.generate_content(context)
            response_text = response.text
            st.markdown(response_text)
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
