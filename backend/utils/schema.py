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
    task: str  # "classification" or "regression"

class TrainResponse(BaseModel):
    model_id: str
    metrics: Dict[str, float]
    feature_importance: Dict[str, float]

class PredictRequest(BaseModel):
    model_id: str
    file_id: str # We assume user uploads a new file for prediction and we get an ID

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
    features: Dict[str, Any] # Complete set of features for single prediction

class SimulateResponse(BaseModel):
    prediction: float # probability or value
    # diff or other info?

class ReportRequest(BaseModel):
    model_id: str
    file_id: str
    thresholds: Dict[str, float] # e.g., {"high": 0.75, "medium": 0.5}
    recommendations: Dict[str, str] # e.g., {"high": "Action A", "medium": "Action B"}
