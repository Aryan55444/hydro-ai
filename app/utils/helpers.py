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
