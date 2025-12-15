import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const uploadCSV = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/upload-csv', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const trainModel = async (fileId: string, target: string, task: string) => {
    const response = await api.post('/train-model', {
        file_id: fileId,
        target,
        task,
    });
    return response.data;
};

export const predict = async (modelId: string, fileId: string) => {
    const response = await api.post('/predict', {
        model_id: modelId,
        file_id: fileId,
    });
    return response.data;
};

export const uploadModel = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/upload-model', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const downloadModelUrl = (modelId: string) => {
    return `${API_BASE_URL}/download-model/${modelId}`;
};

export const explain = async (modelId: string, fileId: string) => {
    const response = await api.post('/explain', {
        model_id: modelId,
        file_id: fileId,
    });
    return response.data;
};

export const simulate = async (modelId: string, features: any) => {
    const response = await api.post('/simulate', {
        model_id: modelId,
        features: features,
    });
    return response.data;
};

export const generateReport = async (modelId: string, fileId: string, thresholds: any, recommendations: any) => {
    const response = await api.post('/generate-report', {
        model_id: modelId,
        file_id: fileId,
        thresholds: thresholds,
        recommendations: recommendations,
    });
    return response.data;
};

export default api;
