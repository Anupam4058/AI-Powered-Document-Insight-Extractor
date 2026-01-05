import { useState, useEffect } from 'react';
import FileUploader from '../components/FileUploader';
import ProcessingIndicator from '../components/ProcessingIndicator';
import ResultsDisplay from '../components/ResultsDisplay';
import { extractInsights, checkHealth, ApiError } from '../api/api';
import type { InsightsResponse } from '../api/api';

type ProcessingState = 'idle' | 'processing' | 'success' | 'error';

export default function MainPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [processingState, setProcessingState] = useState<ProcessingState>('idle');
  const [results, setResults] = useState<InsightsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [estimatedTime, setEstimatedTime] = useState<number>(30);
  const [apiConnected, setApiConnected] = useState<boolean | null>(null);
  const [showConnectionError, setShowConnectionError] = useState<boolean>(false);

  // Check API health on component mount
  useEffect(() => {
    let isMounted = true;
    
    const checkApiConnection = async () => {
      try {
        await checkHealth();
        if (isMounted) {
          setApiConnected((prev) => {
            if (prev === false) {
              // Was disconnected, now connected - no popup needed
            }
            return true;
          });
          setShowConnectionError(false);
        }
      } catch (err) {
        if (isMounted) {
          setApiConnected((prev) => {
            // Only show popup if connection was lost (was true, now false)
            if (prev === true) {
              setShowConnectionError(true);
              setTimeout(() => {
                setShowConnectionError(false);
              }, 2000);
            }
            return false;
          });
          console.warn('Backend API is not available:', err);
        }
      }
    };

    checkApiConnection();
    // Check every 30 seconds
    const interval = setInterval(checkApiConnection, 30000);
    
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setProcessingState('idle');
    setResults(null);
    setError(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    // Check API connection before upload
    if (apiConnected === false) {
      setError('Cannot connect to the backend server. Please ensure the backend is running.');
      setProcessingState('error');
      return;
    }

    setProcessingState('processing');
    setError(null);
    setResults(null);

    // Estimate processing time based on file size (rough estimate: 1MB = 5 seconds)
    const estimatedSeconds = Math.max(10, Math.min(60, (selectedFile.size / (1024 * 1024)) * 5));
    setEstimatedTime(Math.round(estimatedSeconds));

    try {
      const insights = await extractInsights(selectedFile);
      setResults(insights);
      setProcessingState('success');
      setApiConnected(true); // Mark as connected on success
    } catch (err) {
      let errorMessage = 'An unexpected error occurred';
      
      if (err instanceof ApiError) {
        errorMessage = err.message;
        // Update connection status based on error type
        if (err.isNetworkError) {
          setApiConnected(false);
        }
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
      setProcessingState('error');
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setProcessingState('idle');
    setResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            AI-Powered Document Insight Extractor
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto">
            Extract structured insights from retail media documents in seconds.
          </p>
        </header>

        {/* Connection Error Popup */}
        {showConnectionError && (
          <div 
            className="fixed top-4 left-1/2 z-50"
            style={{ 
              transform: 'translateX(-50%)',
              animation: 'fadeInOut 2s ease-in-out'
            }}
          >
            <div className="bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg flex items-center space-x-2">
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span className="font-medium">Backend connection lost</span>
            </div>
          </div>
        )}
        
        <style>{`
          @keyframes fadeInOut {
            0% { opacity: 0; transform: translate(-50%, -10px); }
            15% { opacity: 1; transform: translate(-50%, 0); }
            85% { opacity: 1; transform: translate(-50%, 0); }
            100% { opacity: 0; transform: translate(-50%, -10px); }
          }
        `}</style>

        {/* Main Content */}
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-6">
            {/* Left Side: Upload Section */}
            <div className="bg-white rounded-2xl shadow-xl p-6 md:p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Upload Document</h2>
              
              <FileUploader
                onFileSelect={handleFileSelect}
                disabled={processingState === 'processing'}
              />

              {/* Upload Button */}
              {selectedFile && processingState === 'idle' && (
                <div className="mt-6">
                  <button
                    onClick={handleUpload}
                    className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors duration-200 shadow-md hover:shadow-lg"
                  >
                    Extract Insights
                  </button>
                </div>
              )}

              {/* Processing Indicator */}
              {processingState === 'processing' && (
                <div className="mt-6">
                  <ProcessingIndicator estimatedTime={estimatedTime} />
                </div>
              )}

              {/* Error Message */}
              {error && (
                <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <div className="flex items-start space-x-3">
                    <svg
                      className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    <div className="flex-1">
                      <h3 className="font-semibold text-red-900 mb-1">Error</h3>
                      <p className="text-sm text-red-700">{error}</p>
                    </div>
                  </div>
                  <button
                    onClick={handleReset}
                    className="mt-4 text-sm text-red-600 hover:text-red-800 underline"
                  >
                    Try again
                  </button>
                </div>
              )}

              {/* Reset Button (after success) */}
              {processingState === 'success' && (
                <div className="mt-6">
                  <button
                    onClick={handleReset}
                    className="w-full bg-gray-600 hover:bg-gray-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors duration-200"
                  >
                    Upload New Document
                  </button>
                </div>
              )}
            </div>

            {/* Right Side: Results Display */}
            <div className="bg-white rounded-2xl shadow-xl p-6 md:p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Extracted Insights</h2>
              
              {processingState === 'idle' && !results && (
                <div className="text-center py-12 text-gray-500">
                  <svg
                    className="w-16 h-16 mx-auto mb-4 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  <p>Upload a document to see extracted insights</p>
                </div>
              )}

              {processingState === 'processing' && (
                <div className="text-center py-12 text-gray-500">
                  <p>Processing your document...</p>
                </div>
              )}

              {results && (
                <div className="max-h-[calc(100vh-300px)] overflow-y-auto">
                  <ResultsDisplay results={results} />
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center mt-12 text-gray-500 text-sm">
          <p>Built for retail teams • Creative briefs • Ad specs • Brand guidelines</p>
        </footer>
      </div>
    </div>
  );
}

