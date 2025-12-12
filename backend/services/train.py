import pandas as pd
import numpy as np
from sklearn.base import is_classifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
import joblib
import os
from .preprocess import build_pipeline, get_column_info

# Using relative path from where main.py is likely run (root or backend)
# We will ensure helpers uses absolute or relative correctly. Here we assume we pass a directory.
MODEL_DIR = "backend/models"

def train_model(file_path: str, target: str, task: str, model_id: str):
    df = pd.read_csv(file_path)
    
    # Drop target rows that are NaN
    df = df.dropna(subset=[target])
    
    X = df.drop(columns=[target])
    y = df[target]
    
    # Separate features
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'bool']).columns.tolist()
    
    # Build Preprocessing Pipeline
    preprocessor = build_pipeline(numeric_features, categorical_features)
    
    # Select Model
    if task == "classification":
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    elif task == "regression":
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    else:
        raise ValueError("Invalid task type. Choose 'classification' or 'regression'.")
    
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('classifier', model)])
    
    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    metrics = {}
    
    if task == "classification":
        metrics['accuracy'] = accuracy_score(y_test, y_pred)
        # For multi-class or binary, handle properly. Assuming binary for simple average or micro/macro
        is_binary = len(np.unique(y)) == 2
        avg_method = 'binary' if is_binary else 'weighted'
        
        metrics['precision'] = precision_score(y_test, y_pred, average=avg_method, zero_division=0)
        metrics['recall'] = recall_score(y_test, y_pred, average=avg_method, zero_division=0)
        metrics['f1'] = f1_score(y_test, y_pred, average=avg_method, zero_division=0)
        
        if is_binary and hasattr(clf, "predict_proba"):
             try:
                 metrics['auc'] = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])
             except:
                 pass
                 
    else: # Regression
        metrics['rmse'] = np.sqrt(mean_squared_error(y_test, y_pred))
        metrics['mae'] = mean_absolute_error(y_test, y_pred)
        metrics['r2'] = r2_score(y_test, y_pred)
        
    # Feature Importance
    # We need to access the model step and then the preprocessor to get feature names
    feature_importance = {}
    try:
        rf_model = clf.named_steps['classifier']
        
        # Get feature names from preprocessor
        # OneHotEncoder names are tricky, we rely on having access to transformers
        preprocessor_step = clf.named_steps['preprocessor']
        
        # This is complex with pipelines. We will approximate or try to extract
        
        cat_names = preprocessor_step.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_features)
        feature_names = numeric_features + list(cat_names)
        
        importances = rf_model.feature_importances_
        
        if len(feature_names) == len(importances):
            feature_importance = dict(zip(feature_names, importances))
            # Sort and take top 20
            feature_importance = dict(sorted(feature_importance.items(), key=lambda item: item[1], reverse=True)[:20])
    except Exception as e:
        print(f"Could not extract feature importance: {e}")
        
    # Save Model
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        
    model_path = os.path.join(MODEL_DIR, f"{model_id}.pkl")
    joblib.dump(clf, model_path)
    
    return metrics, feature_importance
