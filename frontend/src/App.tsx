function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <header className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            AI-Powered Document Insight Extractor
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Extract structured insights from retail media documents in seconds. 
            Transform hours of manual work into instant, accurate results.
          </p>
        </header>

        {/* Main Content Card */}
        <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl p-8 md:p-12">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-indigo-100 rounded-full mb-6">
              <svg 
                className="w-10 h-10 text-indigo-600" 
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
            </div>
            <h2 className="text-3xl font-semibold text-gray-900 mb-4">
              Ready to Get Started
            </h2>
            <p className="text-gray-600 mb-8">
              Upload your documents and let AI extract key insights automatically
            </p>
          </div>

          {/* Feature Grid */}
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="text-center p-6 bg-gray-50 rounded-lg">
              <div className="text-3xl mb-3">⚡</div>
              <h3 className="font-semibold text-gray-900 mb-2">Fast Processing</h3>
              <p className="text-sm text-gray-600">
                60-80% faster than manual extraction
              </p>
            </div>
            <div className="text-center p-6 bg-gray-50 rounded-lg">
              <div className="text-3xl mb-3">🎯</div>
              <h3 className="font-semibold text-gray-900 mb-2">Accurate Results</h3>
              <p className="text-sm text-gray-600">
                AI-powered precision with fewer errors
              </p>
            </div>
            <div className="text-center p-6 bg-gray-50 rounded-lg">
              <div className="text-3xl mb-3">📄</div>
              <h3 className="font-semibold text-gray-900 mb-2">Multiple Formats</h3>
              <p className="text-sm text-gray-600">
                Supports PDF and DOCX files
              </p>
            </div>
          </div>

          {/* CTA Button */}
          <div className="text-center">
            <button className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3 rounded-lg transition-colors duration-200 shadow-md hover:shadow-lg">
              Upload Document
            </button>
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center mt-12 text-gray-500 text-sm">
          <p>Built for retail teams • Creative briefs • Ad specs • Brand guidelines</p>
        </footer>
      </div>
    </div>
  )
}

export default App
