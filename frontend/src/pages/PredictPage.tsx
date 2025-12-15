import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { predict, explain, simulate, generateReport, downloadModelUrl } from '../api';
import { Loader2, Download, BarChart2, Activity, FileText, Zap } from 'lucide-react';
import axios from 'axios';

const PredictPage: React.FC = () => {
    const location = useLocation();
    const state = location.state as any || {};
    const { modelId: initialModelId, fileId: initialFileId } = state;

    const [modelId] = useState<string | null>(initialModelId || null);
    const [fileId] = useState<string | null>(initialFileId || null);

    // Config from local storage
    const [config, setConfig] = useState<any>({});

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);

    // Data for table and simulator (Top 50 rows)
    const [tableData, setTableData] = useState<any[]>([]);

    // Explain State
    const [explainResult, setExplainResult] = useState<any>(null);
    const [explaining, setExplaining] = useState(false);

    // Simulator State
    const [selectedRow, setSelectedRow] = useState<any>(null);
    const [simulationFeatures, setSimulationFeatures] = useState<any>({});
    const [simulationResult, setSimulationResult] = useState<number | null>(null);
    const [simulating, setSimulating] = useState(false);

    useEffect(() => {
        const storedConfig = localStorage.getItem('churnConfig');
        if (storedConfig) {
            setConfig(JSON.parse(storedConfig));
        }

        // Auto-predict if both IDs are present initially
        if (initialModelId && initialFileId) {
            runPrediction(initialModelId, initialFileId);
        }
    }, []);

    const runPrediction = async (mid: string, fid: string) => {
        setLoading(true);
        setError(null);
        try {
            const res = await predict(mid, fid);
            setResult(res);

            // Fetch the CSV data to populate table and simulator
            if (res.download_url) {
                const csvUrl = `http://localhost:8000${res.download_url}`;
                const csvResp = await axios.get(csvUrl);
                const rows = csvResp.data.split('\n');
                const headers = rows[0].split(',');
                // Exclude last header which is 'prediction' usually? Or check data.

                // Parse first 20 rows
                const parsedData = rows.slice(1, 21).filter((r: string) => r.trim()).map((row: string) => {
                    const values = row.split(',');
                    const obj: any = {};
                    headers.forEach((h: string, i: number) => {
                        // simple CSV parsing, assumes no commas in values
                        obj[h.trim()] = values[i];
                    });
                    return obj;
                });
                setTableData(parsedData);
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || "Prediction failed");
        } finally {
            setLoading(false);
        }
    };

    const handleExplain = async () => {
        if (!modelId || !fileId) return;
        setExplaining(true);
        try {
            const res = await explain(modelId, fileId);
            setExplainResult(res);
        } catch (err: any) {
            alert("Explanation failed: " + err.message);
        } finally {
            setExplaining(false);
        }
    };

    const handleGenerateReport = async () => {
        if (!modelId || !fileId) return;
        try {
            const res = await generateReport(modelId, fileId,
                { high: config.highThreshold, medium: config.mediumThreshold },
                { high: config.recHigh, medium: config.recMedium }
            );
            window.open(`http://localhost:8000${res.download_url}`, '_blank');
        } catch (err: any) {
            alert("Report generation failed: " + err.message);
        }
    };

    const handleRowSelect = (row: any) => {
        setSelectedRow(row);
        // Remove prediction column if exists
        const { prediction, ...feats } = row;
        setSimulationFeatures(feats);
        setSimulationResult(null);
    };

    const handleSimulationChange = (key: string, value: string) => {
        setSimulationFeatures({
            ...simulationFeatures,
            [key]: value
        });
    };

    const runSimulation = async () => {
        if (!modelId) return;
        setSimulating(true);
        try {
            // Convert types if needed? Backend might handle string numbers if simple.
            // But better ensure they match.
            const res = await simulate(modelId, simulationFeatures);
            setSimulationResult(res.prediction);
        } catch (err: any) {
            alert("Simulation failed: " + err.message);
        } finally {
            setSimulating(false);
        }
    };

    if (!modelId) {
        return <div className="text-center mt-10">No model selected. <a href="/" className="text-blue-600">Go Home</a></div>;
    }

    return (
        <div className="max-w-7xl mx-auto py-8 px-4">
            <div className="flex justify-between items-center mb-8">
                <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
                <div className="flex space-x-4">
                    <a href={downloadModelUrl(modelId)} className="flex items-center px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 font-medium">
                        <Download className="w-4 h-4 mr-2" />
                        Download Pipeline
                    </a>
                </div>
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                {/* Left Column: Predictions Table */}
                <div className="lg:col-span-2 space-y-8">
                    <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-bold text-gray-800 flex items-center">
                                <Activity className="w-5 h-5 mr-2 text-indigo-500" />
                                Prediction Results
                            </h2>
                            {result && (
                                <a
                                    href={`http://localhost:8000${result.download_url}`}
                                    target="_blank"
                                    rel="noreferrer"
                                    className="text-sm flex items-center text-green-600 font-bold hover:underline"
                                >
                                    <Download size={16} className="mr-1" /> Download CSV
                                </a>
                            )}
                        </div>

                        {loading ? (
                            <div className="py-10 flex justify-center text-indigo-600">
                                <Loader2 className="animate-spin w-8 h-8" />
                            </div>
                        ) : tableData.length > 0 ? (
                            <div className="overflow-x-auto">
                                <div className="max-h-96 overflow-y-auto">
                                    <table className="min-w-full divide-y divide-gray-200">
                                        <thead className="bg-gray-50 sticky top-0">
                                            <tr>
                                                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
                                                {Object.keys(tableData[0]).slice(0, 5).map(h => (
                                                    <th key={h} className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{h}</th>
                                                ))}
                                                <th className="px-4 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider bg-yellow-50">Prediction</th>
                                            </tr>
                                        </thead>
                                        <tbody className="bg-white divide-y divide-gray-200">
                                            {tableData.map((row, idx) => (
                                                <tr key={idx} className={`hover:bg-indigo-50 cursor-pointer ${selectedRow === row ? 'bg-indigo-100 ring-2 ring-indigo-500' : ''}`} onClick={() => handleRowSelect(row)}>
                                                    <td className="px-4 py-2 whitespace-nowrap text-xs">
                                                        <button className="text-indigo-600 font-bold" onClick={(e) => { e.stopPropagation(); handleRowSelect(row); }}>Simulate</button>
                                                    </td>
                                                    {Object.entries(row).slice(0, 5).map(([k, v]: any) => (
                                                        <td key={k} className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{v}</td>
                                                    ))}
                                                    <td className="px-4 py-2 whitespace-nowrap text-sm font-bold text-gray-900 bg-yellow-50/50">
                                                        {row['prediction'] || row['Prediction']}
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                                <p className="text-xs text-center text-gray-400 mt-2">Showing first 20 rows. Download full CSV for more.</p>
                            </div>
                        ) : (
                            <p className="text-center py-8 text-gray-400">No predictions available yet.</p>
                        )}
                    </div>
                </div>

                {/* Right Column: Tools */}
                <div className="space-y-6">

                    {/* Simulator Card */}
                    <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100 relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-2 opacity-10">
                            <Zap className="w-24 h-24 text-yellow-500" />
                        </div>
                        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center relative z-10">
                            <Zap className="w-5 h-5 mr-2 text-yellow-500" />
                            What-if Simulator
                        </h2>

                        {selectedRow ? (
                            <div className="relative z-10">
                                <div className="space-y-3 max-h-80 overflow-y-auto pr-2 mb-4">
                                    <div className="grid grid-cols-2 gap-2 text-xs font-mono bg-gray-50 p-2 rounded">
                                        <div className="text-gray-500">Original Prob:</div>
                                        <div className="font-bold">{selectedRow['prediction'] || selectedRow['Prediction']}</div>
                                    </div>

                                    {/* Compare Result */}
                                    {simulationResult !== null && (
                                        <div className="grid grid-cols-2 gap-2 text-xs font-mono bg-indigo-50 p-2 rounded border border-indigo-200">
                                            <div className="text-indigo-600 font-bold">New Prob:</div>
                                            <div className="font-bold text-indigo-700">{typeof simulationResult === 'number' ? simulationResult.toFixed(4) : simulationResult}</div>
                                            <div className="col-span-2 text-center text-xs mt-1">
                                                {Number(simulationResult) > Number(selectedRow['prediction'] || selectedRow['Prediction']) ? 'Risk Increased 🔺' : 'Risk Decreased 🔻'}
                                            </div>
                                        </div>
                                    )}

                                    {Object.keys(simulationFeatures).map(key => (
                                        key !== 'prediction' && key !== 'Prediction' && (
                                            <div key={key}>
                                                <label className="block text-xs font-medium text-gray-700 mb-1">{key}</label>
                                                <input
                                                    type="text"
                                                    value={simulationFeatures[key]}
                                                    onChange={(e) => handleSimulationChange(key, e.target.value)}
                                                    className="w-full text-sm border-gray-300 rounded shadow-sm focus:ring-indigo-500 focus:border-indigo-500 p-1 border"
                                                />
                                            </div>
                                        )
                                    ))}
                                </div>
                                <button
                                    onClick={runSimulation}
                                    disabled={simulating}
                                    className="w-full bg-yellow-500 text-white font-bold py-2 rounded-lg hover:bg-yellow-600 transition-colors flex justify-center items-center shadow-lg"
                                >
                                    {simulating ? <Loader2 className="animate-spin" /> : "Simulate Change"}
                                </button>
                            </div>
                        ) : (
                            <div className="text-center py-10 text-gray-400 relative z-10">
                                Select a row from the table to simulate changes.
                            </div>
                        )}
                    </div>

                    {/* Report & Explain Card */}
                    <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-100">
                        <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                            <FileText className="w-5 h-5 mr-2 text-indigo-500" />
                            Insights & Reports
                        </h2>
                        <div className="space-y-4">
                            <button
                                onClick={handleExplain}
                                disabled={explaining}
                                className="w-full bg-indigo-600 text-white font-bold py-3 rounded-lg hover:bg-indigo-700 transition-colors flex items-center justify-center shadow-md"
                            >
                                {explaining ? <Loader2 className="animate-spin mr-2" /> : <BarChart2 className="w-5 h-5 mr-2" />}
                                Generate Explainability
                            </button>

                            <button
                                onClick={handleGenerateReport}
                                className="w-full bg-white text-gray-700 font-bold py-3 rounded-lg border-2 border-gray-200 hover:border-gray-300 transition-colors flex items-center justify-center"
                            >
                                <Download className="w-5 h-5 mr-2 text-red-500" />
                                Download Full Report (PDF)
                            </button>
                        </div>
                    </div>

                </div>
            </div>

            {/* Explainability Results Section (Full Width) */}
            {explainResult && (
                <div className="mt-12 bg-white p-8 rounded-xl shadow-lg border border-gray-100 animate-in fade-in slide-in-from-bottom-4 duration-700">
                    <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                        <BarChart2 className="w-6 h-6 mr-2 text-indigo-600" />
                        Model Explainability (SHAP)
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div>
                            <h3 className="text-lg font-semibold mb-4">Feature Importance (SHAP)</h3>
                            <div className="space-y-2">
                                {Object.entries(explainResult.feature_importance).map(([feat, val]: any) => (
                                    <div key={feat} className="flex items-center">
                                        <div className="w-32 text-sm text-gray-600 truncate mr-2" title={feat}>{feat}</div>
                                        <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
                                            <div
                                                className="h-full bg-indigo-500 rounded-full"
                                                style={{ width: `${Math.min(val * 100 * 5, 100)}%` }} // Scaling for visibility
                                            ></div>
                                        </div>
                                        <div className="w-16 text-right text-xs font-mono text-gray-500">{(val).toFixed(4)}</div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="flex flex-col items-center">
                            <h3 className="text-lg font-semibold mb-4">SHAP Summary Plot</h3>
                            <img
                                src={`http://localhost:8000${explainResult.summary_plot_url}`}
                                alt="SHAP Plot"
                                className="max-w-full rounded-lg shadow-sm border border-gray-200"
                            />
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PredictPage;
