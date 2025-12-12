import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import FileUploader from '../components/FileUploader';
import { uploadCSV } from '../api';
import { Loader2 } from 'lucide-react';

const UploadDataset: React.FC = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleFileSelect = async (file: File) => {
        setLoading(true);
        setError(null);
        try {
            const data = await uploadCSV(file);
            // Save state to local storage or context (simple approach: pass via navigation state)
            navigate('/select-target', {
                state: {
                    fileId: data.file_id,
                    columns: data.columns,
                    dtypes: data.dtypes,
                    filename: data.filename
                }
            });
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to upload file");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto py-12 px-4">
            <h1 className="text-3xl font-bold text-gray-900 mb-2 text-center">Random Forest ML Platform</h1>
            <p className="text-gray-500 text-center mb-10">Upload your dataset to get started</p>

            <div className="bg-white p-8 rounded-xl shadow-lg">
                <FileUploader onFileSelect={handleFileSelect} />

                {loading && (
                    <div className="mt-6 flex items-center justify-center text-blue-600">
                        <Loader2 className="animate-spin mr-2" />
                        <span>Uploading and analyzing...</span>
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
