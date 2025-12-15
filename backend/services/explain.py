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

MODEL_DIR = "backend/models" # Should probably Centralize this config

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
        # Check if 'cat' transformer exists and has onehot
        if 'cat' in preprocessor.named_transformers_:
            cat_transformer = preprocessor.named_transformers_['cat']
            # Access the onehot step if it's a pipeline, or directly if it's the transformer
            if hasattr(cat_transformer, 'named_steps'):
                 onehot = cat_transformer.named_steps['onehot']
            else:
                 onehot = cat_transformer # Might be just the step if not nested pipeline
            
            # This depends on exact structure in train.py. 
            # In train.py: categorical_transformer = Pipeline(steps=[('imputer', ...), ('onehot', ...)])
            # So it is a pipeline.
            if hasattr(cat_transformer, 'named_steps') and 'onehot' in cat_transformer.named_steps:
                onehot = cat_transformer.named_steps['onehot']
                cat_names = onehot.get_feature_names_out(categorical_cols)
                return numeric_cols + list(cat_names)
    except Exception as e:
        print(f"Error extracting feature names: {e}")
    
    # Fallback: just return empty or indices if failed
    return []

def generate_shap_explanation(model_id: str, file_path: str):
    model = load_model(model_id)
    df = load_data(file_path) # Original Data
    
    # We need to know which cols are num/cat to extract names correctly
    # But the pipeline knows.
    # To get feature names cleanly, we need the original lists used during training.
    # Limitation: The pipeline object might not store the original column lists explicitly unless we stored them.
    # However, we can inspect correct columns from the dataframe if they match.
    
    # Preprocess
    preprocessor = model.named_steps['preprocessor']
    X_transformed = preprocessor.transform(df)
    
    # Model
    rf = model.named_steps['classifier']
    
    # Explainer
    # TreeExplainer is efficient for RF
    explainer = shap.TreeExplainer(rf)
    shap_values = explainer.shap_values(X_transformed)
    
    # For binary classification, shap_values is a list [class0, class1]. We usually want class1 (churn).
    if isinstance(shap_values, list):
         shap_values = shap_values[1]
    
    # Feature Names
    # We try to recover them. 
    # Current train.py splits X (drop target) -> num/cat. 
    # We can try to infer from the input df types, assuming they match training.
    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = df.select_dtypes(include=['object', 'bool']).columns.tolist()
    
    feature_names = get_feature_names(model, numeric_features, categorical_features)
    if len(feature_names) != X_transformed.shape[1]:
        # Fallback if mismatch (e.g. target column was present in df but not in X_transformed?? No, preprocessor takes selected cols)
        # Actually preprocessor uses column selector. modifying df to drop target if exists?
        # The service layer receiving the file usually doesn't know the target column name unless passed.
        # But 'explain' endpoint assumes we are explaining the dataset provided.
        # If the model was trained with 'Churn' as target, and we pass a DF with 'Churn', the preprocessor might fail or include it if not careful.
        # ColumnTransformer usually selects by name. If 'Churn' is not in the list of transformers, it is dropped or passed through?
        # In train.py: numeric_features = X.select_dtypes...
        # preprocessor uses these names.
        # So providing the whole DF is fine IF the columns match.
        feature_names = [f"Feature {i}" for i in range(X_transformed.shape[1])]

    # Summary Plot
    plt.figure()
    shap.summary_plot(shap_values, X_transformed, feature_names=feature_names, show=False)
    
    plot_filename = f"shap_summary_{uuid.uuid4()}.png"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    plot_path = os.path.join(UPLOAD_DIR, plot_filename)
    plt.savefig(plot_path, bbox_inches='tight')
    plt.close()
    
    # Calculate global feature importance from SHAP
    # Mean absolute SHAP value per feature
    global_shap_importance = np.abs(shap_values).mean(0)
    importance_dict = dict(zip(feature_names, global_shap_importance))
    # Sort
    importance_dict = dict(sorted(importance_dict.items(), key=lambda item: item[1], reverse=True)[:20])
    
    return importance_dict, plot_filename

def simulate_prediction(model_id: str, features: dict):
    model = load_model(model_id)
    
    # Convert dict to DataFrame
    # We need to make sure types are correct. 
    # The pipeline expects a DataFrame.
    input_df = pd.DataFrame([features])
    
    # Predict Proba if classification, Predict if regression
    rf = model.named_steps['classifier']
    
    # Pipeline 'predict' calls transform then predict
    # But we want 'predict_proba' for classification if available
    
    is_classifier = hasattr(rf, 'predict_proba')
    
    if is_classifier:
        try:
            prob = model.predict_proba(input_df)
            # return prob of class 1
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
    
    # 1. Predictions
    # Assume target is not in df or we ignore it.
    predictions = model.predict(df)
    
    # If classifier, get probabilities
    rf = model.named_steps['classifier']
    if hasattr(rf, 'predict_proba'):
        probs = model.predict_proba(df)[:, 1]
    else:
        probs = predictions # Validation/Regression?
        
    # 2. Risk Categorization
    df['Churn Probability'] = probs
    
    def get_risk(prob):
        if prob >= thresholds.get('high', 0.75):
            return 'High Risk'
        elif prob >= thresholds.get('medium', 0.5):
            return 'Medium Risk'
        else:
            return 'Low Risk'
            
    df['Risk Level'] = df['Churn Probability'].apply(get_risk)
    
    # 3. PDF Generation
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    # Summary Stats
    high_risk_count = df[df['Risk Level'] == 'High Risk'].shape[0]
    medium_risk_count = df[df['Risk Level'] == 'Medium Risk'].shape[0]
    
    pdf.cell(0, 10, f"Total Customers: {len(df)}", 0, 1)
    pdf.cell(0, 10, f"High Risk: {high_risk_count} (Recommendation: {recommendations.get('high', 'N/A')})", 0, 1)
    pdf.cell(0, 10, f"Medium Risk: {medium_risk_count} (Recommendation: {recommendations.get('medium', 'N/A')})", 0, 1)
    pdf.ln(10)
    
    # Top Features logic (Global)
    # We reuse the shap logic roughly or use feature importances from model if available
    # Let's use the model's feature importances for the global section
    # Re-extract names
    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    # Remove 'Churn Probability' and 'Risk Level' from numeric features list if they slipped in
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
    
    # High Risk Customers List (Top 50)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, "High Risk Customers (Top 50)", 0, 1)
    pdf.set_font('Arial', '', 10)
    
    high_risk_df = df[df['Risk Level'] == 'High Risk'].sort_values(by='Churn Probability', ascending=False).head(50)
    
    # We want to show Why. 
    # For a proper report, we'd run SHAP on these specific rows.
    # But running SHAP on loop might be slow.
    # We will just list basic info + probability for now to save time, 
    # or implementing lightweight contribution check?
    # Let's just dump the ID (if exists) or Index and Prob.
    
    # Heuristic for "Why":
    # Just show the probability and maybe the values of the top 3 global features for that user?
    
    for idx, row in high_risk_df.iterrows():
        # Clean string
        row_str = f"ID: {idx} | Prob: {row['Churn Probability']:.2f}"
        pdf.cell(0, 8, row_str, 0, 1)
        
    report_filename = f"churn_report_{uuid.uuid4()}.pdf"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        
    report_path = os.path.join(UPLOAD_DIR, report_filename)
    pdf.output(report_path)
    
    return report_filename
