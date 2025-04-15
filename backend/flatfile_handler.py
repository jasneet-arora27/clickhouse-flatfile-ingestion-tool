import pandas as pd

def read_flatfile_schema(file_path: str, delimiter: str = ','):
    """
    Reads the CSV (or flat file) and returns the column headers.
    """
    try:
        df = pd.read_csv(file_path, delimiter=delimiter, nrows=1)
        return list(df.columns)
    except Exception as e:
        print(f"Error reading file schema from {file_path}: {e}")
        return []

def preview_data(file_path: str, delimiter: str = ',', rows: int = 100):
    """
    Reads the first 'rows' of the CSV for preview purposes.
    """
    try:
        df = pd.read_csv(file_path, delimiter=delimiter, nrows=rows)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error previewing data from {file_path}: {e}")
        return []
