from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class UploadResponse(BaseModel):
    filename: str
    columns: List[str]
    dtypes: Dict[str, str]
    file_id: str

class TrainRequest(BaseModel):
    file_id: str
    target: str
    task: str  

class TrainResponse(BaseModel):
    model_id: str
    metrics: Dict[str, float]
    feature_importance: Dict[str, float]

class PredictRequest(BaseModel):
    model_id: str
    file_id: str 

class PredictionResponse(BaseModel):
    predictions: List[Any]
    download_url: str

class ExplainRequest(BaseModel):
    model_id: str
    file_id: str

class ExplainResponse(BaseModel):
    summary_plot_url: str
    feature_importance: Dict[str, float]

class SimulateRequest(BaseModel):
    model_id: str
    features: Dict[str, Any] 

class SimulateResponse(BaseModel):
    prediction: float 

class ReportRequest(BaseModel):
    model_id: str
    file_id: str
    thresholds: Dict[str, float] 
    recommendations: Dict[str, str] 
