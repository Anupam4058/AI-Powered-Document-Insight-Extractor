import type { InsightsResponse } from '../api/api';
import { downloadJSON, formatDate } from '../utils/helpers';

interface ResultsDisplayProps {
  results: InsightsResponse;
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  const handleDownloadJSON = () => {
    downloadJSON(results, `insights-${results.file_metadata.filename.replace(/\.[^/.]+$/, '')}.json`);
  };

  return (
    <div className="space-y-6">
      {/* Download Button */}
      <div className="flex justify-end">
        <button
          onClick={handleDownloadJSON}
          className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
        >
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
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
            />
          </svg>
          <span>Download Results as JSON</span>
        </button>
      </div>

      {/* Summary Card */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Summary</h2>
        <p className="text-gray-700 leading-relaxed">{results.summary}</p>
      </div>

      {/* Document Type */}
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Document Type</h2>
        <div className="flex items-center space-x-3">
          <span className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full font-semibold">
            {results.document_type.type || 'Unknown'}
          </span>
          {results.document_type.confidence && (
            <span className="text-sm text-gray-600">
              Confidence: {(results.document_type.confidence * 100).toFixed(1)}%
            </span>
          )}
        </div>
      </div>

      {/* Creative Requirements */}
      {(results.creative_requirements.dimensions.length > 0 ||
        results.creative_requirements.formats.length > 0 ||
        results.creative_requirements.colors.length > 0 ||
        results.creative_requirements.fonts.length > 0 ||
        results.creative_requirements.tone.length > 0) && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Creative Requirements</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {results.creative_requirements.dimensions.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Dimensions</h3>
                <ul className="list-disc list-inside text-gray-600 space-y-1">
                  {results.creative_requirements.dimensions.map((dim, idx) => (
                    <li key={idx}>{dim}</li>
                  ))}
                </ul>
              </div>
            )}
            {results.creative_requirements.formats.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Formats</h3>
                <ul className="list-disc list-inside text-gray-600 space-y-1">
                  {results.creative_requirements.formats.map((format, idx) => (
                    <li key={idx}>{format}</li>
                  ))}
                </ul>
              </div>
            )}
            {results.creative_requirements.colors.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Colors</h3>
                <div className="flex flex-wrap gap-2">
                  {results.creative_requirements.colors.map((color, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm"
                    >
                      {color}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {results.creative_requirements.fonts.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Fonts</h3>
                <ul className="list-disc list-inside text-gray-600 space-y-1">
                  {results.creative_requirements.fonts.map((font, idx) => (
                    <li key={idx}>{font}</li>
                  ))}
                </ul>
              </div>
            )}
            {results.creative_requirements.tone.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Tone</h3>
                <div className="flex flex-wrap gap-2">
                  {results.creative_requirements.tone.map((tone, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm"
                    >
                      {tone}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Technical Specs */}
      {Object.keys(results.technical_specs).length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Technical Specifications</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <tbody className="bg-white divide-y divide-gray-200">
                {Object.entries(results.technical_specs).map(([key, value]) => (
                  <tr key={key}>
                    <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900 capitalize">
                      {key.replace(/_/g, ' ')}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600">
                      {Array.isArray(value) ? (
                        <ul className="list-disc list-inside">
                          {value.map((item: any, idx: number) => (
                            <li key={idx}>{String(item)}</li>
                          ))}
                        </ul>
                      ) : (
                        String(value)
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Brand Guidelines */}
      {Object.keys(results.brand_guidelines).length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Brand Guidelines</h2>
          <div className="space-y-4">
            {Object.entries(results.brand_guidelines).map(([key, value]) => {
              if (Array.isArray(value) && value.length === 0) return null;
              if (!Array.isArray(value) && !value) return null;
              
              return (
                <div key={key}>
                  <h3 className="font-semibold text-gray-700 mb-2 capitalize">
                    {key.replace(/_/g, ' ')}
                  </h3>
                  {Array.isArray(value) ? (
                    <div className="flex flex-wrap gap-2">
                      {value.map((item: any, idx: number) => (
                        <span
                          key={idx}
                          className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm"
                        >
                          {String(item)}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-600">{String(value)}</p>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* KPIs */}
      {Object.keys(results.kpis).length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Key Performance Indicators</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {Object.entries(results.kpis).map(([key, value]) => (
              <div key={key} className="p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold text-gray-700 mb-1 uppercase text-sm">
                  {key.replace(/_/g, ' ')}
                </h3>
                <p className="text-2xl font-bold text-indigo-600">{String(value)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Deadlines */}
      {results.deadlines.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Deadlines</h2>
          <div className="space-y-3">
            {results.deadlines.map((deadline, idx) => (
              <div key={idx} className="flex items-start space-x-3 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <svg
                  className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
                <div className="flex-1">
                  <p className="font-semibold text-gray-900">
                    {formatDate(deadline.date)}
                  </p>
                  {(deadline.description || deadline.context) && (
                    <p className="text-sm text-gray-600 mt-1">
                      {deadline.description || deadline.context}
                    </p>
                  )}
                  {deadline.type && (
                    <span className="inline-block mt-1 px-2 py-0.5 text-xs bg-yellow-200 text-yellow-800 rounded">
                      {deadline.type}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Items */}
      {results.action_items.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Action Items</h2>
          <div className="space-y-2">
            {results.action_items.map((item, idx) => {
              const task = typeof item === 'string' ? item : item.task;
              const priority = typeof item === 'string' ? undefined : item.priority;
              
              return (
                <div key={idx} className="flex items-start space-x-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                  <div className="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-xs font-bold">{idx + 1}</span>
                  </div>
                  <div className="flex-1">
                    <p className="text-gray-900">{task}</p>
                    {priority && (
                      <span className={`inline-block mt-1 px-2 py-0.5 text-xs rounded ${
                        priority.toLowerCase() === 'high' 
                          ? 'bg-red-100 text-red-800' 
                          : priority.toLowerCase() === 'medium'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-green-100 text-green-800'
                      }`}>
                        {priority} Priority
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Warnings */}
      {results.warnings.length > 0 && (
        <div className="bg-white rounded-lg border border-red-200 p-6 shadow-sm bg-red-50">
          <h2 className="text-xl font-bold text-red-900 mb-4">⚠️ Warnings</h2>
          <div className="space-y-2">
            {results.warnings.map((warning, idx) => {
              const message = warning.message || warning.text || 'Warning';
              const severity = warning.severity || warning.type;
              
              return (
                <div key={idx} className="flex items-start space-x-3 p-3 bg-white border border-red-200 rounded-lg">
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
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                    />
                  </svg>
                  <div className="flex-1">
                    <p className="text-gray-900">{message}</p>
                    {severity && (
                      <span className="text-xs text-red-600 mt-1 block">
                        {severity.charAt(0).toUpperCase() + severity.slice(1)}
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* File Metadata */}
      <div className="bg-gray-50 rounded-lg border border-gray-200 p-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-2">File Information</h3>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div>
            <span className="text-gray-600">Filename:</span>
            <span className="ml-2 font-medium text-gray-900">{results.file_metadata.filename}</span>
          </div>
          <div>
            <span className="text-gray-600">Size:</span>
            <span className="ml-2 font-medium text-gray-900">{results.file_metadata.file_size}</span>
          </div>
          <div>
            <span className="text-gray-600">Type:</span>
            <span className="ml-2 font-medium text-gray-900">{results.file_metadata.file_type}</span>
          </div>
          <div>
            <span className="text-gray-600">Words:</span>
            <span className="ml-2 font-medium text-gray-900">{results.file_metadata.word_count.toLocaleString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

