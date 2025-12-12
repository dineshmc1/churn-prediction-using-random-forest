import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { trainModel } from '../api';
import { Loader2, ArrowRight } from 'lucide-react';
import clsx from 'clsx';

const SelectTarget: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const state = location.state as any || {};
    const { fileId, columns, dtypes, filename } = state;

    const [target, setTarget] = useState<string>('');
    const [task, setTask] = useState<string>('classification');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    if (!fileId) {
        return <div className="text-center mt-10">No file uploaded. <a href="/" className="text-blue-600">Go back</a></div>;
    }

    const handleTrain = async () => {
        if (!target) return;
        setLoading(true);
        setError(null);
        try {
            const data = await trainModel(fileId, target, task);
            navigate('/training-result', {
                state: {
                    modelId: data.model_id,
                    metrics: data.metrics,
                    featureImportance: data.feature_importance,
                    target,
                    task,
                    fileId
                }
            });
        } catch (err: any) {
            setError(err.response?.data?.detail || "Training failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto py-12 px-4">
            <h1 className="text-2xl font-bold text-gray-900 mb-6">Configure Training</h1>

            <div className="bg-white p-8 rounded-xl shadow-md space-y-8">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Dataset File</label>
                    <div className="p-3 bg-gray-50 rounded-lg text-gray-800 font-mono text-sm">{filename}</div>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Select Target Column</label>
                    <select
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        value={target}
                        onChange={(e) => setTarget(e.target.value)}
                    >
                        <option value="">-- Select Target --</option>
                        {columns.map((col: string) => (
                            <option key={col} value={col}>
                                {col} ({dtypes[col]})
                            </option>
                        ))}
                    </select>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Problem Type</label>
                    <div className="flex space-x-4">
                        <button
                            className={clsx(
                                "flex-1 py-3 px-4 rounded-lg border text-sm font-medium transition-colors",
                                task === 'classification'
                                    ? "bg-blue-50 border-blue-500 text-blue-700 ring-1 ring-blue-500"
                                    : "border-gray-300 text-gray-700 hover:bg-gray-50"
                            )}
                            onClick={() => setTask('classification')}
                        >
                            Classification
                        </button>
                        <button
                            className={clsx(
                                "flex-1 py-3 px-4 rounded-lg border text-sm font-medium transition-colors",
                                task === 'regression'
                                    ? "bg-blue-50 border-blue-500 text-blue-700 ring-1 ring-blue-500"
                                    : "border-gray-300 text-gray-700 hover:bg-gray-50"
                            )}
                            onClick={() => setTask('regression')}
                        >
                            Regression
                        </button>
                    </div>
                </div>

                {error && <div className="p-4 bg-red-50 text-red-700 rounded-lg text-sm">{error}</div>}

                <div className="pt-4">
                    <button
                        onClick={handleTrain}
                        disabled={!target || loading}
                        className="w-full py-4 bg-black text-white rounded-lg font-bold text-lg hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                    >
                        {loading ? <Loader2 className="animate-spin mr-2" /> : <ArrowRight className="mr-2" />}
                        {loading ? "Training Model..." : "Start Training"}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default SelectTarget;
