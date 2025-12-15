import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
import io

def load_data(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

def get_column_info(df: pd.DataFrame):
    columns = df.columns.tolist()
    dtypes = {}
    for col in columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            dtypes[col] = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            dtypes[col] = "datetime"
        else:
            dtypes[col] = "categorical"
    return columns, dtypes

def build_pipeline(numeric_features, categorical_features):
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    return preprocessor

def clean_data(df: pd.DataFrame, target: str = None):
    
    if target and target in df.columns:
        df = df.dropna(subset=[target])
    return df
