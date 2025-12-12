from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import shutil
from typing import List

from backend.utils.schema import UploadResponse, TrainRequest, TrainResponse, PredictRequest, PredictionResponse
from backend.utils.helpers import save_upload_file, get_file_path, UPLOAD_DIR
from backend.services.preprocess import load_data, get_column_info
from backend.services.train import train_model
from backend.services.predict import make_prediction

app = FastAPI(title="ML Full-Stack App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-csv", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    # Read file content
    content = await file.read()
    file_id = save_upload_file(content, file.filename)
    
    # Load and inspect
    file_path = get_file_path(file_id)
    try:
        df = load_data(file_path)
        columns, dtypes = get_column_info(df)
        
        return UploadResponse(
            filename=file.filename,
            columns=columns,
            dtypes=dtypes,
            file_id=file_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train-model", response_model=TrainResponse)
async def train(request: TrainRequest):
    file_path = get_file_path(request.file_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found.")
    
    try:
        # Generate a model ID
        model_id = request.file_id + "_" + request.target # Simple ID strategy
        
        metrics, feature_importance = train_model(
            file_path=file_path, 
            target=request.target, 
            task=request.task, 
            model_id=model_id
        )
        
        return TrainResponse(
            model_id=model_id,
            metrics=metrics,
            feature_importance=feature_importance
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictRequest):
    # Depending on how the frontend handles it, we might receive a file_id (already uploaded via upload-csv)
    # or the frontend might need to upload the file first.
    # The requirement says "Upload new CSV for prediction".
    # So the flow is: Upload CSV -> Get ID -> Call /predict with ID and Model ID.
    
    file_path = get_file_path(request.file_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="Prediction file not found.")
        
    try:
        predictions, result_filename = make_prediction(request.model_id, file_path)
        
        # Construct download URL (assuming we have a download endpoint)
        download_url = f"/download/{result_filename}"
        
        return PredictionResponse(
            predictions=predictions,
            download_url=download_url
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/")
def read_root():
    return {"message": "ML API is running"}
