import pandas as pd

def clean_csv_file():
    input_file = "data/finaldataset.csv"
    output_file = "data/finaldataset_clean.csv"
    
    df = pd.read_csv(input_file, encoding='latin-1', comment='#', on_bad_lines='skip')
    
    df.columns = df.columns.str.strip().str.replace('\n', '').str.replace('\r', '')
    
    df = df.dropna(how='all')
    
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"Data cleaned successfully!")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Rows: {len(df)}")
    print(f"Cleaned file saved as: {output_file}")

if __name__ == "__main__":
    clean_csv_file()
