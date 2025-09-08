import pandas as pd

def get_data_summary(df: pd.DataFrame) -> str:
    # Print debug information
    print("\n=== Debug Info ===")
    print(f"DataFrame shape: {df.shape}")
    print("Columns in DataFrame:", list(df.columns))
    print("First few rows:")
    print(df.head(2).to_string())
    print("=================\n")
    
    # Try to find the state column with various possible names
    state_col = None
    for col in df.columns:
        if 'state' in str(col).lower() or 'stn_name' in str(col).lower():
            state_col = col
            break
    
    # Try to find district column
    district_col = None
    for col in df.columns:
        if 'district' in str(col).lower() or 'location' in str(col).lower():
            district_col = col
            break
    
    # Try to find year column
    year_col = None
    for col in df.columns:
        if 'year' in str(col).lower() or 'date' in str(col).lower() or 'yr' in str(col).lower():
            year_col = col
            break
    
    # Process states
    states = df[state_col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True).str.title() if state_col is not None else pd.Series()
    
    # Process districts
    districts = df[district_col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True).str.title() if district_col is not None else pd.Series()
    
    # Process years
    years = pd.to_numeric(df[year_col], errors='coerce') if year_col is not None else pd.Series()
    
    # Calculate metrics
    num_states = states.nunique() if not states.empty else 0
    num_districts = districts.nunique() if not districts.empty else 0
    year_min = int(years.min()) if not years.empty and not pd.isna(years.min()) else 'N/A'
    year_max = int(years.max()) if not years.empty and not pd.isna(years.max()) else 'N/A'
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

