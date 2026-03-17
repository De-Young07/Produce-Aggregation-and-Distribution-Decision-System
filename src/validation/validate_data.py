import pandas as pd

def validate_dataset(path):

    df = pd.read_csv(path)

    if df.isnull().sum().sum() > 0:
        raise ValueError(f"Missing values detected in {path}")

    if len(df) == 0:
        raise ValueError(f"Dataset {path} is empty")

    print(f"{path} validation passed")