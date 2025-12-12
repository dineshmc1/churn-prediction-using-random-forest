import React, { useRef, useState } from 'react';
import { Upload } from 'lucide-react';
import clsx from 'clsx';

interface FileUploaderProps {
    onFileSelect: (file: File) => void;
    label?: string;
}

const FileUploader: React.FC<FileUploaderProps> = ({ onFileSelect, label = "Upload CSV Dataset" }) => {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [fileName, setFileName] = useState<string | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setFileName(file.name);
            onFileSelect(file);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        const file = e.dataTransfer.files?.[0];
        if (file) {
            setFileName(file.name);
            onFileSelect(file);
        }
    };

    return (
        <div
            className="border-2 border-dashed border-gray-300 rounded-lg p-10 text-center hover:bg-gray-50 transition-colors cursor-pointer"
            onClick={() => fileInputRef.current?.click()}
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
        >
            <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                accept=".csv"
                onChange={handleFileChange}
            />
            <div className="flex flex-col items-center justify-center space-y-3">
                <div className="p-3 bg-blue-100 rounded-full text-blue-600">
                    <Upload size={32} />
                </div>
                <h3 className="text-lg font-semibold text-gray-700">{label}</h3>
                <p className="text-sm text-gray-500">
                    {fileName ? `Selected: ${fileName}` : "Drag & drop file here or click to browse"}
                </p>
            </div>
        </div>
    );
};

export default FileUploader;
