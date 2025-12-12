import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import FileUploader from '../components/FileUploader';
import { predict } from '../api';
import { Loader2, Download } from 'lucide-react';
import { uploadCSV } from '../api';

const PredictPage: React.FC = () => {
    const location = useLocation();
    const state = location.state as any || {};
    const { modelId } = state;

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    const handlePredictionUpload = async (file: File) => {
        setLoading(true);
        setError(null);
        setResult(null);
        try {
            // 1. Upload
            const uploadRes = await uploadCSV(file);

            // 2. Predict
            const predRes = await predict(modelId, uploadRes.file_id);
            setResult(predRes);

        } catch (err: any) {
            setError(err.response?.data?.detail || "Prediction failed");
        } finally {
            setLoading(false);
        }
    };

    if (!modelId) {
        return <div className="text-center mt-10">No model selected. <a href="/" className="text-blue-600">Go Home</a></div>;
    }

    return (
        <div className="max-w-4xl mx-auto py-12 px-4">
            <h1 className="text-2xl font-bold text-gray-900 mb-6">Make Predictions</h1>

            <div className="bg-white p-8 rounded-xl shadow-md mb-8">
                <FileUploader onFileSelect={handlePredictionUpload} label="Upload Production Dataset" />
                {loading && (
                    <div className="mt-6 flex items-center justify-center text-blue-600">
                        <Loader2 className="animate-spin mr-2" />
                        <span>Running predictions...</span>
                    </div>
                )}
                {error && <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg">{error}</div>}
            </div>

            {result && (
                <div className="bg-white p-8 rounded-xl shadow-md animate-fade-in">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-xl font-bold text-gray-800">Prediction Results</h2>
                        <a
                            href={`http://localhost:8000${result.download_url}`}
                            target="_blank"
                            rel="noreferrer"
                            className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                        >
                            <Download size={18} className="mr-2" />
                            Download CSV
                        </a>
                    </div>

                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Row</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Prediction</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {result.predictions.slice(0, 10).map((pred: any, idx: number) => (
                                    <tr key={idx}>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{idx + 1}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{String(pred)}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        {result.predictions.length > 10 && (
                            <p className="text-center text-sm text-gray-500 mt-4">Showing first 10 rows...</p>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default PredictPage;
