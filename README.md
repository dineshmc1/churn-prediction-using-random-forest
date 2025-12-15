# Random Forest Churn Prediction & Explainability App

A powerful full-stack machine learning application designed for automated churn prediction, regression analysis, and deep model explainability. Built with **FastAPI** and **React**, this tool allows users to train Random Forest models, visualize insights with **SHAP**, simulate "What-If" scenarios, and generate actionable PDF reports.

## 🚀 Key Features

### 1. **Automated Machine Learning (AutoML)**
- **Drag & Drop Upload**: distinct CSV handling with automatic column & data type detection.
- **Dynamic Pipeline**: Automatically handles missing values (imputation), categorical variables (one-hot encoding), and feature scaling.
- **Flexible Training**: Supports both **Classification** (e.g., Churn Yes/No) and **Regression** (e.g., LTV prediction) tasks.

### 2. **Advanced Explainability & Insights**
- **SHAP Analysis**: Unveil the "Black Box" of Machine Learning. View global feature importance and summary plots to understand *why* the model makes specific decisions.
- **Feature Importance**: Interactive charts showing the top drivers of your target variable.
- **Model Metrics**: detailed performance evaluation (Accuracy, Precision, Recall, F1-Score, RMSE, R²).

### 3. **Interactive Simulation (What-If Analysis)**
- **Simulator**: Tweak input features in real-time to see how changes affect the predicted outcome (e.g., "If we increase tenure by 2 years, does churn risk drop?").

### 4. **Actionable Reporting**
- **PDF Reports**: Generate professional churn reports containing:
    - Executive summary of customer base risk profile.
    - Systematic risk categorization (High/Medium/Low) based on custom thresholds.
    - Tailored strategic recommendations for each risk segment.
    - Top 50 High-Risk customer lists.

### 5. **Model Management**
- **Persistence**: Save trained models to disk and reload them anytime for future predictions.
- **Portability**: Download `.pkl` model files and share them across environments.

---

## 🛠️ Tech Stack

### **Backend**
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance Async Python API)
- **ML Core**: [Scikit-Learn](https://scikit-learn.org/), [Pandas](https://pandas.pydata.org/), [Joblib](https://joblib.readthedocs.io/)
- **Explainability**: [SHAP](https://shap.readthedocs.io/) (SHapley Additive exPlanations)
- **Reporting**: [FPDF](https://pyfpdf.readthedocs.io/), [Matplotlib](https://matplotlib.org/)

### **Frontend**
- **Framework**: [React](https://react.dev/) (via [Vite](https://vitejs.dev/))
- **Language**: TypeScript
- **Styling**: [TailwindCSS](https://tailwindcss.com/)
- **Visualization**: [Recharts](https://recharts.org/)
- **Icons**: [Lucide React](https://lucide.dev/)

---

## 📂 Project Structure

```bash
/backend
    /models        # Directory for saved .pkl models
    /services      # Core logic: train, predict, explain, report
    /utils         # Helpers (file saving) and Pydantic schemas
    main.py        # FastAPI entry point & route definitions
    requirements.txt

/frontend
    /src
        /components # Reusable UI components (Charts, Forms)
        /pages      # Main application views
        api.ts      # Axios instance & API method definitions
    package.json
    vite.config.ts
```

---

## ⚡ How to Run Locally

### 1. Backend Setup
1.  Navigate to the root directory.
2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r backend/requirements.txt
    ```
4.  Start the server:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

### 2. Frontend Setup
1.  Open a new terminal and navigate to the frontend:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the dev server:
    ```bash
    npm run dev
    ```
    The app will be accessible at `http://localhost:5173`.

---

## 🚀 Deployment Guide

### Backend (Render / Railway)
1.  **Build Command**: `pip install -r backend/requirements.txt`
2.  **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
3.  **Python Version**: 3.9+

### Frontend (Vercel)
1.  **Framework Preset**: Vite
2.  **Root Directory**: `frontend`
3.  **Build Command**: `npm run build`
4.  **Output Directory**: `dist`
5.  **Environment Variables**:
    - `VITE_API_BASE_URL`: URL of your deployed backend (e.g., `https://your-api.onrender.com`).

---

## 📖 API Documentation
Once the backend is running, visit `http://localhost:8000/docs` to explore the interactive Swagger UI documentation for all endpoints.
