import React from 'react';
import clsx from 'clsx';

interface MetricsDisplayProps {
    metrics: Record<string, number>;
}

const MetricsDisplay: React.FC<MetricsDisplayProps> = ({ metrics }) => {
    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            {Object.entries(metrics).map(([key, value]) => (
                <div key={key} className="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                    <h4 className="text-xs uppercase font-bold text-gray-500 mb-1">{key}</h4>
                    <p className="text-2xl font-bold text-gray-800">{typeof value === 'number' ? value.toFixed(4) : value}</p>
                </div>
            ))}
        </div>
    );
};

export default MetricsDisplay;
