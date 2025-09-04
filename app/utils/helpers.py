import pandas as pd

def get_data_summary(df: pd.DataFrame) -> str:
    states = df['STATE'].astype(str).str.strip().str.replace("\s+", " ", regex=True).str.title() if 'STATE' in df.columns else pd.Series([])
    districts = df['DISTRICT'].astype(str).str.strip().str.replace("\s+", " ", regex=True).str.title() if 'DISTRICT' in df.columns else pd.Series([])
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

def detect_user_type(prompt: str) -> str:
    prompt_lower = prompt.lower()
    
    farmer_keywords = ['farmer', 'agriculture', 'crop', 'irrigation', 'soil', 'simple', 'easy', 'basic', 'what is', 'how to', 'help']
    researcher_keywords = ['analysis', 'research', 'study', 'statistical', 'correlation', 'trend', 'pattern', 'comprehensive', 'detailed', 'investigation', 'examination']
    
    farmer_score = sum(1 for keyword in farmer_keywords if keyword in prompt_lower)
    researcher_score = sum(1 for keyword in researcher_keywords if keyword in prompt_lower)
    
    if researcher_score > farmer_score:
        return "researcher"
    else:
        return "farmer"

def get_tabular_data(df: pd.DataFrame, query: str) -> str:
    query_lower = query.lower()
    
    if 'district' in query_lower and 'DISTRICT' in df.columns:
        districts = df['DISTRICT'].astype(str).str.strip().str.replace("\s+", " ", regex=True).str.title()
        for district in districts.unique():
            if district.lower() in query_lower:
                district_data = df[df['DISTRICT'] == district]
                return f"District {district} Data:\n{district_data.head(10).to_string(index=False)}"
    
    if 'parameter' in query_lower or 'quality' in query_lower:
        numeric_cols = ['pH', 'EC', 'F', 'NO3', 'Cl', 'SO4', 'TH', 'TDS']
        available_cols = [col for col in numeric_cols if col in df.columns]
        if available_cols:
            sample_data = df[available_cols].dropna().head(10)
            return f"Water Quality Parameters:\n{sample_data.to_string(index=False)}"
    
    return f"Sample Data:\n{df.head(10).to_string(index=False)}"
