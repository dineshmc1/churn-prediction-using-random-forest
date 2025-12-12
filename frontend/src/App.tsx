import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UploadDataset from './pages/UploadDataset';
import SelectTarget from './pages/SelectTarget';
import TrainingResult from './pages/TrainingResult';
import PredictPage from './pages/PredictPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50 text-gray-800 font-sans">
        <nav className="bg-white border-b border-gray-200 shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <a href="/" className="flex-shrink-0 flex items-center">
                  <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                    AutoML Flow
                  </span>
                </a>
              </div>
            </div>
          </div>
        </nav>

        <main>
          <Routes>
            <Route path="/" element={<UploadDataset />} />
            <Route path="/select-target" element={<SelectTarget />} />
            <Route path="/training-result" element={<TrainingResult />} />
            <Route path="/predict" element={<PredictPage />} />
          </Routes>
        </main>

        <footer className="bg-white border-t border-gray-200 mt-auto">
          <div className="max-w-7xl mx-auto py-6 px-4 overflow-hidden sm:px-6 lg:px-8">
            <p className="text-center text-sm text-gray-400">
              &copy; {new Date().getFullYear()} AutoML Platform. Built with FastAPI & React.
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
