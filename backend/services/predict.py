import pandas as pd
import joblib
import os
import uuid
from .preprocess import load_data, clean_data

MODEL_DIR = "backend/models"
UPLOAD_DIR = "uploads" # Assuming predictions are saved here too or temp

def make_prediction(model_id: str, file_path: str):
    model_path = os.path.join(MODEL_DIR, f"{model_id}.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model {model_id} not found.")
    
    model = joblib.load(model_path)
    
    df = pd.read_csv(file_path)
    
    # Predict
    # The pipeline handles preprocessing, so we just pass the dataframe
    # But we should ensure the input dataframe has the same columns (excluding target)
    # The pipeline is robust enough to handle extra cols if we just select what we need?
    # No, we assume user uploads compatible CSV.
    
    predictions = model.predict(df)
    
    # Save results
    result_df = df.copy()
    result_df['prediction'] = predictions
    
    # Generate unique filename for prediction result
    pred_id = str(uuid.uuid4())
    result_filename = f"prediction_{pred_id}.csv"
    
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        
    result_path = os.path.join(UPLOAD_DIR, result_filename)
    result_df.to_csv(result_path, index=False)
    
    return predictions.tolist(), result_filename
