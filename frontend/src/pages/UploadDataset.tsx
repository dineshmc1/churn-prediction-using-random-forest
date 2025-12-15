import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import FileUploader from '../components/FileUploader';
import { uploadCSV, uploadModel } from '../api';
import { Loader2, Settings, Play, Upload, FileText } from 'lucide-react';

interface Config {
    highThreshold: number;
    mediumThreshold: number;
    recHigh: string;
    recMedium: string;
    recLow: string;
}

const UploadDataset: React.FC = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [mode, setMode] = useState<'train' | 'predict'>('train');

    // Config State
    const [config, setConfig] = useState<Config>({
        highThreshold: 0.75,
        mediumThreshold: 0.5,
        recHigh: "Immediate intervention required. Call customer.",
        recMedium: "Send promotional offer via email.",
        recLow: "Monitor usage patterns."
    });

    // Prediction Mode State
    const [uploadedModelId, setUploadedModelId] = useState<string | null>(null);
    const [predictionFileId, setPredictionFileId] = useState<string | null>(null);

    // Save config to local storage on change
    useEffect(() => {
        localStorage.setItem('churnConfig', JSON.stringify(config));
    }, [config]);

    const handleCSVUpload = async (file: File) => {
        setLoading(true);
        setError(null);
        try {
            const data = await uploadCSV(file);

            if (mode === 'train') {
                navigate('/select-target', {
                    state: {
                        fileId: data.file_id,
                        columns: data.columns,
                        dtypes: data.dtypes,
                        filename: data.filename
                    }
                });
            } else {
                setPredictionFileId(data.file_id);
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to upload file");
        } finally {
            setLoading(false);
        }
    };

    const handleModelUpload = async (file: File) => {
        setLoading(true);
        setError(null);
        try {
            const data = await uploadModel(file);
            setUploadedModelId(data.model_id);
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to upload model");
        } finally {
            setLoading(false);
        }
    };

    const startPrediction = () => {
        if (uploadedModelId && predictionFileId) {
            navigate('/predict', {
                state: {
                    modelId: uploadedModelId,
                    fileId: predictionFileId, // The file to predict on
                    // We assume columns match the model. Error handling in backend provided.
                }
            });
        }
    };

    return (
        <div className="max-w-4xl mx-auto py-12 px-4">
            <h1 className="text-4xl font-extrabold text-gray-900 mb-2 text-center bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                AutoML & Churn Analytics
            </h1>
            <p className="text-gray-500 text-center mb-10 text-lg">
                Train robust models or simulate scenarios with explainability
            </p>

            {/* Global Configuration Panel */}
            <div className="bg-white p-6 rounded-xl shadow-md mb-8 border border-gray-100">
                <div className="flex items-center mb-4">
                    <Settings className="w-5 h-5 text-gray-400 mr-2" />
                    <h2 className="text-lg font-semibold text-gray-800">Risk Thresholds & Recommendations</h2>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">High Risk Threshold ({config.highThreshold})</label>
                        <input
                            type="range" min="0" max="1" step="0.01"
                            value={config.highThreshold}
                            onChange={(e) => setConfig({ ...config, highThreshold: parseFloat(e.target.value) })}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                        />
                        <label className="block text-sm font-medium text-gray-700 mt-4 mb-1">Medium Risk Threshold ({config.mediumThreshold})</label>
                        <input
                            type="range" min="0" max="1" step="0.01"
                            value={config.mediumThreshold}
                            onChange={(e) => setConfig({ ...config, mediumThreshold: parseFloat(e.target.value) })}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                        />
                    </div>

                    <div className="space-y-3">
                        <input
                            type="text" placeholder="Recommendation for High Risk"
                            value={config.recHigh}
                            onChange={(e) => setConfig({ ...config, recHigh: e.target.value })}
                            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                        />
                        <input
                            type="text" placeholder="Recommendation for Medium Risk"
                            value={config.recMedium}
                            onChange={(e) => setConfig({ ...config, recMedium: e.target.value })}
                            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                        />
                        <input
                            type="text" placeholder="Recommendation for Low Risk"
                            value={config.recLow}
                            onChange={(e) => setConfig({ ...config, recLow: e.target.value })}
                            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                        />
                    </div>
                </div>
            </div>

            {/* Mode Selection */}
            <div className="flex justify-center space-x-4 mb-8">
                <button
                    onClick={() => setMode('train')}
                    className={`px-6 py-2 rounded-full font-medium transition-colors ${mode === 'train' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-600 hover:bg-gray-300'}`}
                >
                    Train New Model
                </button>
                <button
                    onClick={() => setMode('predict')}
                    className={`px-6 py-2 rounded-full font-medium transition-colors ${mode === 'predict' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-600 hover:bg-gray-300'}`}
                >
                    Load Pipeline & Predict
                </button>
            </div>

            <div className="bg-white p-8 rounded-xl shadow-lg border border-gray-100">
                {mode === 'train' ? (
                    <div>
                        <h3 className="text-xl font-bold mb-4 flex items-center">
                            <Upload className="w-5 h-5 mr-2 text-indigo-500" />
                            Upload Training Dataset
                        </h3>
                        <FileUploader onFileSelect={handleCSVUpload} />
                    </div>
                ) : (
                    <div className="space-y-8">
                        <div>
                            <h3 className="text-xl font-bold mb-4 flex items-center">
                                <Settings className="w-5 h-5 mr-2 text-indigo-500" />
                                1. Upload Saved Pipeline (.pkl)
                            </h3>
                            {uploadedModelId ? (
                                <div className="p-4 bg-green-50 text-green-700 rounded-lg flex items-center">
                                    <FileText className="w-5 h-5 mr-2" />
                                    Model Loaded! (ID: {uploadedModelId})
                                </div>
                            ) : (
                                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 hover:border-indigo-500 transition-colors cursor-pointer relative bg-gray-50/50">
                                    <input
                                        type="file"
                                        accept=".pkl"
                                        onChange={(e) => e.target.files && handleModelUpload(e.target.files[0])}
                                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                                    />
                                    <div className="text-center">
                                        <Upload className="mx-auto h-12 w-12 text-gray-400 mb-3" />
                                        <p className="text-sm font-medium text-gray-700">Click to upload .pkl file</p>
                                    </div>
                                </div>
                            )}
                        </div>

                        {uploadedModelId && (
                            <div className="animate-in fade-in slide-in-from-bottom duration-500">
                                <h3 className="text-xl font-bold mb-4 flex items-center">
                                    <FileText className="w-5 h-5 mr-2 text-indigo-500" />
                                    2. Upload New Data for Prediction (CSV)
                                </h3>
                                <FileUploader onFileSelect={handleCSVUpload} />
                            </div>
                        )}

                        {predictionFileId && uploadedModelId && (
                            <div className="flex justify-center mt-6">
                                <button
                                    onClick={startPrediction}
                                    className="bg-green-600 text-white px-8 py-3 rounded-lg hover:bg-green-700 transition-colors flex items-center text-lg font-semibold shadow-md"
                                >
                                    <Play className="w-5 h-5 mr-2" />
                                    Run Analytics
                                </button>
                            </div>
                        )}
                    </div>
                )}

                {loading && (
                    <div className="mt-6 flex items-center justify-center text-blue-600">
                        <Loader2 className="animate-spin mr-2" />
                        <span>Processing...</span>
                    </div>
                )}

                {error && (
                    <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg">
                        {error}
                    </div>
                )}
            </div>
        </div>
    );
};

export default UploadDataset;
