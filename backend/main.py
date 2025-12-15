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
from backend.services.explain import generate_shap_explanation, simulate_prediction, generate_report
from backend.utils.schema import (
    UploadResponse, TrainRequest, TrainResponse, PredictRequest, PredictionResponse,
    ExplainRequest, ExplainResponse, SimulateRequest, SimulateResponse, ReportRequest
)

app = FastAPI(title="ML Full-Stack App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-csv", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    content = await file.read()
    file_id = save_upload_file(content, file.filename)
    
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
        model_id = request.file_id + "_" + request.target 
        
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
    
    
    file_path = get_file_path(request.file_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="Prediction file not found.")
        
    try:
        predictions, result_filename = make_prediction(request.model_id, file_path)
        
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

@app.get("/download-model/{model_id}")
async def download_model(model_id: str):
    model_path = f"backend/models/{model_id}.pkl"
    if os.path.exists(model_path):
        return FileResponse(model_path, filename=f"{model_id}.pkl")
    raise HTTPException(status_code=404, detail="Model not found")

@app.post("/upload-model")
async def upload_model(file: UploadFile = File(...)):
    if not file.filename.endswith(".pkl"):
        raise HTTPException(status_code=400, detail="Only .pkl files are allowed.")
    
    model_dir = "backend/models"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        

    
    file_path = os.path.join(model_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"message": "Model uploaded successfully", "model_id": file.filename.replace(".pkl", "")}

@app.post("/explain", response_model=ExplainResponse)
async def explain(request: ExplainRequest):
    file_path = get_file_path(request.file_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found.")
        
    try:
        feature_importance, plot_filename = generate_shap_explanation(request.model_id, file_path)
        
        plot_url = f"/download/{plot_filename}"
        
        return ExplainResponse(
            summary_plot_url=plot_url,
            feature_importance=feature_importance
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate", response_model=SimulateResponse)
async def simulate(request: SimulateRequest):
    try:
        prediction = simulate_prediction(request.model_id, request.features)
        return SimulateResponse(prediction=prediction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-report")
async def report(request: ReportRequest):
    file_path = get_file_path(request.file_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found.")
        
    try:
        report_filename = generate_report(
            request.model_id, 
            file_path, 
            request.thresholds, 
            request.recommendations
        )
        return {"download_url": f"/download/{report_filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "ML API is running"}
