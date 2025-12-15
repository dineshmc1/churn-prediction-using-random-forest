import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import MetricsDisplay from '../components/MetricsDisplay';
import FeatureImportanceChart from '../components/FeatureImportanceChart';
import { ArrowRight, Download } from 'lucide-react';
import { downloadModelUrl } from '../api';

const TrainingResult: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const state = location.state as any || {};
    const { modelId, metrics, featureImportance, task } = state;

    if (!modelId) {
        return <div className="text-center mt-10">No model data found. <a href="/" className="text-blue-600">Go Home</a></div>;
    }

    const handleGoPredict = () => {
        navigate('/predict', { state: { modelId } });
    };

    return (
        <div className="max-w-5xl mx-auto py-12 px-4">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Training Complete</h1>
                    <p className="text-gray-500 mt-1">Model ID: {modelId}</p>
                </div>
                <div className="text-right">
                    <span className="inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium uppercase tracking-wide">
                        {task}
                    </span>
                </div>
            </div>

            <MetricsDisplay metrics={metrics} />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2">
                    <FeatureImportanceChart data={featureImportance} />
                </div>
                <div className="lg:col-span-1">
                    <div className="bg-blue-50 p-6 rounded-xl h-full flex flex-col justify-center items-center text-center">
                        <h3 className="text-xl font-bold text-blue-900 mb-2">Ready to Predict?</h3>
                        <p className="text-blue-700 mb-6">Use your trained model to make predictions on new data.</p>
                        <button
                            onClick={handleGoPredict}
                            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-blue-700 transition flex items-center mb-4 w-full justify-center"
                        >
                            Go to Prediction <ArrowRight className="ml-2" size={18} />
                        </button>

                        <a
                            href={downloadModelUrl(modelId)}
                            className="bg-white border-2 border-blue-600 text-blue-600 px-6 py-3 rounded-lg font-bold hover:bg-blue-50 transition flex items-center w-full justify-center"
                        >
                            <Download className="mr-2" size={18} />
                            Download Pipeline
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TrainingResult;
