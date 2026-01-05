interface ProcessingIndicatorProps {
  message?: string;
  estimatedTime?: number; // in seconds
}

export default function ProcessingIndicator({ 
  message = 'Processing document...',
  estimatedTime 
}: ProcessingIndicatorProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 bg-white rounded-lg border-2 border-indigo-200">
      {/* Spinner */}
      <div className="relative w-16 h-16 mb-4">
        <div className="absolute inset-0 border-4 border-indigo-200 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-indigo-600 rounded-full border-t-transparent animate-spin"></div>
      </div>

      {/* Status Message */}
      <p className="text-lg font-semibold text-gray-900 mb-2">{message}</p>
      
      {/* Estimated Time */}
      {estimatedTime && (
        <p className="text-sm text-gray-500">
          Estimated time: {estimatedTime} seconds
        </p>
      )}

      {/* Processing Steps */}
      <div className="mt-6 space-y-2 text-sm text-gray-600">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-indigo-600 rounded-full animate-pulse"></div>
          <span>Extracting text from document...</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-indigo-600 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
          <span>Analyzing content with AI...</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-gray-300 rounded-full"></div>
          <span className="text-gray-400">Structuring insights...</span>
        </div>
      </div>
    </div>
  );
}

