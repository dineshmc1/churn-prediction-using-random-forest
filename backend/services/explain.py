import pandas as pd
import shap
import joblib
import os
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
from .preprocess import load_data
from ..utils.helpers import UPLOAD_DIR
import uuid

MODEL_DIR = "backend/models" 

def load_model(model_id: str):
    model_path = os.path.join(MODEL_DIR, f"{model_id}.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model {model_id} not found.")
    return joblib.load(model_path)

def get_feature_names(model, numeric_cols, categorical_cols):
    """
    Attempt to extract feature names from the pipeline preprocessor.
    """
    try:
        preprocessor = model.named_steps['preprocessor']
        if 'cat' in preprocessor.named_transformers_:
            cat_transformer = preprocessor.named_transformers_['cat']
            if hasattr(cat_transformer, 'named_steps'):
                 onehot = cat_transformer.named_steps['onehot']
            else:
                 onehot = cat_transformer 
            
            
            if hasattr(cat_transformer, 'named_steps') and 'onehot' in cat_transformer.named_steps:
                onehot = cat_transformer.named_steps['onehot']
                cat_names = onehot.get_feature_names_out(categorical_cols)
                return numeric_cols + list(cat_names)
    except Exception as e:
        print(f"Error extracting feature names: {e}")
    
    return []

def generate_shap_explanation(model_id: str, file_path: str):
    model = load_model(model_id)
    df = load_data(file_path) 
    
    
    preprocessor = model.named_steps['preprocessor']
    X_transformed = preprocessor.transform(df)
    
    rf = model.named_steps['classifier']
    
    
    explainer = shap.TreeExplainer(rf)
    shap_values = explainer.shap_values(X_transformed)
    
    if isinstance(shap_values, list):
         shap_values = shap_values[1]
    
    
    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = df.select_dtypes(include=['object', 'bool']).columns.tolist()
    
    feature_names = get_feature_names(model, numeric_features, categorical_features)
    if len(feature_names) != X_transformed.shape[1]:
        feature_names = [f"Feature {i}" for i in range(X_transformed.shape[1])]

    plt.figure()
    shap.summary_plot(shap_values, X_transformed, feature_names=feature_names, show=False)
    
    plot_filename = f"shap_summary_{uuid.uuid4()}.png"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    plot_path = os.path.join(UPLOAD_DIR, plot_filename)
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()
    
    global_shap_importance = np.abs(shap_values).mean(0)
    importance_dict = dict(zip(feature_names, global_shap_importance))
    importance_dict = dict(sorted(importance_dict.items(), key=lambda item: item[1], reverse=True)[:20])
    
    return importance_dict, plot_filename

def simulate_prediction(model_id: str, features: dict):
    model = load_model(model_id)
    
    input_df = pd.DataFrame([features])
    
    
    rf = model.named_steps['classifier']
    
    
    
    is_classifier = hasattr(rf, 'predict_proba')
    
    if is_classifier:
        try:
            prob = model.predict_proba(input_df)
            return prob[0][1] 
        except:
             return model.predict(input_df)[0]
    else:
        return model.predict(input_df)[0]


class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Churn Prediction & Explainability Report', 0, 1, 'C')
        self.ln(10)

def generate_report(model_id: str, file_path: str, thresholds: dict, recommendations: dict):
    model = load_model(model_id)
    df = load_data(file_path)
    
    
    predictions = model.predict(df)
    
    rf = model.named_steps['classifier']
    if hasattr(rf, 'predict_proba'):
        probs = model.predict_proba(df)[:, 1]
    else:
        probs = predictions 
        
    
    df['Churn Probability'] = probs
    
    def get_risk(prob):
        if prob >= thresholds.get('high', 0.75):
            return 'High Risk'
        elif prob >= thresholds.get('medium', 0.5):
            return 'Medium Risk'
        else:
            return 'Low Risk'
            
    df['Risk Level'] = df['Churn Probability'].apply(get_risk)
    
    
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    
    high_risk_count = df[df['Risk Level'] == 'High Risk'].shape[0]
    medium_risk_count = df[df['Risk Level'] == 'Medium Risk'].shape[0]
    
    pdf.cell(0, 10, f"Total Customers: {len(df)}", 0, 1)
    pdf.cell(0, 10, f"High Risk: {high_risk_count} (Recommendation: {recommendations.get('high', 'N/A')})", 0, 1)
    pdf.cell(0, 10, f"Medium Risk: {medium_risk_count} (Recommendation: {recommendations.get('medium', 'N/A')})", 0, 1)
    pdf.ln(10)
    
    
    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    numeric_features = [f for f in numeric_features if f not in ['Churn Probability', 'Risk Level']]
    
    categorical_features = df.select_dtypes(include=['object', 'bool']).columns.tolist()
    categorical_features = [f for f in categorical_features if f not in ['Risk Level']]

    feature_names = get_feature_names(model, numeric_features, categorical_features)
    
    if hasattr(rf, 'feature_importances_') and len(feature_names) == len(rf.feature_importances_):
        importances = rf.feature_importances_
        indices = np.argsort(importances)[::-1][:10]
        
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, "Top 10 Global Drivers of Churn", 0, 1)
        pdf.set_font('Arial', '', 12)
        
        for i in indices:
            pdf.cell(0, 10, f"{feature_names[i]}: {importances[i]:.4f}", 0, 1)
    
    pdf.ln(10)
    
    
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "High Risk Customers (Top 50)", 0, 1)
    pdf.set_font('Arial', '', 10)
    
    high_risk_df = df[df['Risk Level'] == 'High Risk'].sort_values(by='Churn Probability', ascending=False).head(50)
    
    
    
    
    for idx, row in high_risk_df.iterrows():
        row_str = f"ID: {idx} | Prob: {row['Churn Probability']:.2f}"
        pdf.cell(0, 8, row_str, 0, 1)
        
    report_filename = f"churn_report_{uuid.uuid4()}.pdf"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        
    report_path = os.path.join(UPLOAD_DIR, report_filename)
    pdf.output(report_path)
    
    return report_filename
