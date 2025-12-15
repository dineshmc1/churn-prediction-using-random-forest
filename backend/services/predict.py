import pandas as pd
import joblib
import os
import uuid
from .preprocess import load_data, clean_data

MODEL_DIR = "backend/models"
UPLOAD_DIR = "uploads" 

def make_prediction(model_id: str, file_path: str):
    model_path = os.path.join(MODEL_DIR, f"{model_id}.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model {model_id} not found.")
    
    model = joblib.load(model_path)
    
    df = pd.read_csv(file_path)
    
    
    
    predictions = model.predict(df)
    
    result_df = df.copy()
    result_df['prediction'] = predictions
    
    pred_id = str(uuid.uuid4())
    result_filename = f"prediction_{pred_id}.csv"
    
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        
    result_path = os.path.join(UPLOAD_DIR, result_filename)
    result_df.to_csv(result_path, index=False)
    
    return predictions.tolist(), result_filename
