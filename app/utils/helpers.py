import pandas as pd

def get_data_summary(df: pd.DataFrame) -> str:
    state_col = next((col for col in df.columns if 'state' in str(col).lower() or 'stn_name' in str(col).lower()), None)
    district_col = next((col for col in df.columns if 'district' in str(col).lower() or 'location' in str(col).lower()), None)
    year_col = next((col for col in df.columns if any(x in str(col).lower() for x in ['year', 'date', 'yr'])), None)
    
    states = df[state_col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True).str.title() if state_col is not None else pd.Series()
    districts = df[district_col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True).str.title() if district_col is not None else pd.Series()
    years = pd.to_numeric(df[year_col], errors='coerce') if year_col is not None else pd.Series()
    
    num_states = states.nunique() if not states.empty else 0
    num_districts = districts.nunique() if not districts.empty else 0
    year_min = int(years.min()) if not years.empty and not pd.isna(years.min()) else 'N/A'
    year_max = int(years.max()) if not years.empty and not pd.isna(years.max()) else 'N/A'
    
    return f"""
    Loaded groundwater quality dataset with {len(df)} samples.
    Columns: {', '.join(df.columns.tolist())}
    Number of states: {num_states}
    Number of districts: {num_districts}
    Year range: {year_min} - {year_max}
    
    First few rows of data:
    {df.head(3).to_string()}
    """
