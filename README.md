# Random Forest ML Full-Stack App

A complete full-stack web application for automated machine learning using Random Forest. Users can upload CSVs, train models, and make predictions.

## Features

- **Upload & Analyze**: Drag-and-drop CSV upload with automatic column detection.
- **Dynamic Training**: Choose target column and problem type (Classification vs Regression).
- **AutoML Pipeline**:
    - Automatic imputation of missing values.
    - One-hot encoding for categorical variables.
    - Standard scaling for numeric variables.
    - Train/Test split and evaluation.
- **Insights**: View accuracy/RMSE, precision/recall, and feature importance charts.
- **Predictions**: Upload new datasets to generate predictions using trained models.
- **Download**: Download prediction results as CSV.

## Tech Stack

- **Backend**: FastAPI, Scikit-Learn, Pandas, Joblib.
- **Frontend**: React, Vite, TypeScript, TailwindCSS, Recharts.

## Folder Structure

```
/backend
    /models        # Saved .pkl models
    /services      # Business logic (train, predict, preprocess)
    /utils         # Helpers and schemas
    main.py        # API Entry point
/frontend
    /src
        /components
        /pages
    ...
```

## How to Run Locally

### 1. Backend Setup

1. Navigate to the root directory.
2. Install Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Run the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```
   The backend will be running at `http://localhost:8000`.

### 2. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The frontend will be running at `http://localhost:5173`.

## Deployment Instructions

### Backend (Render / Railway)

1. **Repository**: Push the code to GitHub.
2. **Build Command**: `pip install -r backend/requirements.txt`
3. **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` (for Render/Railway).
4. **Environment**: Ensure Python 3.9+ is selected.

### Frontend (Vercel)

1. **Repository**: Push the code to GitHub.
2. **Import Project**: Select the `frontend` directory as the root directory in Vercel.
3. **Build Command**: `npm run build`
4. **Output Directory**: `dist`
5. **Environment**:
   - `VITE_API_BASE_URL`: Set this to your deployed Backend URL (e.g. `https://my-ml-backend.onrender.com`).
   - You might need to update `frontend/src/api.ts` to use `import.meta.env.VITE_API_BASE_URL` instead of localhost if you want dynamic configuration.

## API Documentation

View the Swagger UI at `http://localhost:8000/docs` when the backend is running.
