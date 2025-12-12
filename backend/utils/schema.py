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
