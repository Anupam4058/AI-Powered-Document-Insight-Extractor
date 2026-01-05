import { useState } from 'react';
import type { InsightsResponse } from '../api/api';
import { downloadJSON } from '../utils/helpers';

interface ResultsDisplayProps {
  results: InsightsResponse;
}

interface CollapsibleSectionProps {
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
  onCopy?: () => void;
}

function CollapsibleSection({ title, children, defaultOpen = true, onCopy }: CollapsibleSectionProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-900">{title}</h2>
        <div className="flex items-center space-x-2">
          {onCopy && (
            <button
              onClick={onCopy}
              className="px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
              title="Copy section to clipboard"
            >
              Copy
            </button>
          )}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="p-1.5 hover:bg-gray-100 rounded-lg transition-colors"
            aria-label={isOpen ? 'Collapse section' : 'Expand section'}
          >
            <svg
              className={`w-5 h-5 text-gray-600 transition-transform ${isOpen ? 'rotate-180' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        </div>
      </div>
      {isOpen && <div>{children}</div>}
    </div>
  );
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  const handleDownloadJSON = () => {
    downloadJSON(results, `insights-${results.file_metadata.filename.replace(/\.[^/.]+$/, '')}.json`);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      // You could add a toast notification here
    });
  };

  const formatFileSize = (size: string | number): string => {
    const bytes = typeof size === 'string' ? parseInt(size, 10) : size;
    if (isNaN(bytes)) return size.toString();
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const copySummary = () => {
    const text = [
      `Campaign: ${results.summary.goal}`,
      `Dates: ${results.summary.dates}`,
      `Channels: ${results.summary.channels}`,
      `Success: ${results.summary.success}`,
      `Must include: ${results.summary.must_include}`,
      `Avoid: ${results.summary.avoid}`,
    ].filter(Boolean).join('\n');
    copyToClipboard(text);
  };

  const copyCreativeRequirements = () => {
    const text = [
      'Must-have elements:',
      ...results.creative_requirements.must_have.map(item => `  • ${item}`),
      '',
      'Optional elements:',
      ...results.creative_requirements.optional.map(item => `  • ${item}`),
    ].filter(Boolean).join('\n');
    copyToClipboard(text);
  };

  const copyTechnicalSpecs = () => {
    const text = results.technical_specs.map(spec => 
      `${spec.placement}\n  Size: ${spec.size}\n  Formats: ${spec.file_formats.join(', ')}\n  Min font size: ${spec.min_font_size}\n  Notes: ${spec.notes.join('; ')}`
    ).join('\n\n');
    copyToClipboard(text);
  };

  const copyGuidelines = () => {
    const text = [
      'Copy Rules:',
      ...results.guidelines.copy_rules.map(r => `  • ${r}`),
      '',
      'Design Rules:',
      ...results.guidelines.design_rules.map(r => `  • ${r}`),
      '',
      'Accessibility Rules:',
      ...results.guidelines.accessibility_rules.map(r => `  • ${r}`),
      '',
      'Legal Rules:',
      ...results.guidelines.legal_rules.map(r => `  • ${r}`),
    ].filter(Boolean).join('\n');
    copyToClipboard(text);
  };

  const copyActionItems = () => {
    const text = results.action_items.map((item, idx) => `${idx + 1}. ${item}`).join('\n');
    copyToClipboard(text);
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

      {/* Summary */}
      <CollapsibleSection title="Summary" onCopy={copySummary}>
        <div className="space-y-3">
          {results.summary.goal && (
            <div>
              <span className="font-semibold text-gray-800">Campaign: </span>
              <span className="text-gray-700">{results.summary.goal}</span>
            </div>
          )}
          
          {results.summary.dates && (
            <div>
              <span className="font-semibold text-gray-800">Dates: </span>
              <span className="text-gray-700">{results.summary.dates}</span>
            </div>
          )}

          {results.summary.channels && (
            <div>
              <span className="font-semibold text-gray-800">Channels: </span>
              <span className="text-gray-700">{results.summary.channels}</span>
            </div>
          )}

          {results.summary.success && (
            <div>
              <span className="font-semibold text-gray-800">Success: </span>
              <span className="text-gray-700">{results.summary.success}</span>
            </div>
          )}

          {results.summary.must_include && (
            <div>
              <span className="font-semibold text-gray-800">Must include: </span>
              <span className="text-gray-700">{results.summary.must_include}</span>
            </div>
          )}

          {results.summary.avoid && (
            <div>
              <span className="font-semibold text-gray-800">Avoid: </span>
              <span className="text-gray-700">{results.summary.avoid}</span>
            </div>
          )}
        </div>
      </CollapsibleSection>

      {/* Document Type */}
      <CollapsibleSection title="Document Type" defaultOpen={true}>
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <span className="px-4 py-2 bg-indigo-100 text-indigo-800 rounded-lg font-semibold text-lg">
              {results.document_type.type || 'Unknown'}
            </span>
          </div>
          {results.document_type.description && (
            <p className="text-gray-600 leading-relaxed">
              {results.document_type.description}
            </p>
          )}
        </div>
      </CollapsibleSection>

      {/* Creative Requirements */}
      {(results.creative_requirements.must_have.length > 0 || results.creative_requirements.optional.length > 0) && (
        <CollapsibleSection title="Creative Requirements" onCopy={copyCreativeRequirements}>
          <div className="space-y-6">
            {results.creative_requirements.must_have.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-800 mb-3">Must-have elements</h3>
                <ul className="list-disc list-inside text-gray-700 space-y-2">
                  {results.creative_requirements.must_have.map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>
            )}

            {results.creative_requirements.optional.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-800 mb-3">Optional elements</h3>
                <ul className="list-disc list-inside text-gray-700 space-y-2">
                  {results.creative_requirements.optional.map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </CollapsibleSection>
      )}

      {/* Technical Specifications */}
      {results.technical_specs.length > 0 && (
        <CollapsibleSection title="Technical Specifications" onCopy={copyTechnicalSpecs}>
          <div className="space-y-4">
            {results.technical_specs.map((spec, idx) => (
              <div key={idx} className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                <h3 className="font-semibold text-gray-900 mb-3">{spec.placement}</h3>
                <div className="grid md:grid-cols-2 gap-3 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Size:</span>
                    <span className="ml-2 text-gray-600">{spec.size}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">File formats:</span>
                    <span className="ml-2 text-gray-600">{spec.file_formats.join(', ')}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Min font size:</span>
                    <span className="ml-2 text-gray-600">{spec.min_font_size}</span>
                  </div>
                  {spec.notes.length > 0 && (
                    <div className="md:col-span-2">
                      <span className="font-medium text-gray-700">Notes:</span>
                      <ul className="list-disc list-inside ml-2 text-gray-600 mt-1">
                        {spec.notes.map((note, noteIdx) => (
                          <li key={noteIdx}>{note}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </CollapsibleSection>
      )}

      {/* Guidelines & Risks */}
      {(results.guidelines.copy_rules.length > 0 ||
        results.guidelines.design_rules.length > 0 ||
        results.guidelines.accessibility_rules.length > 0 ||
        results.guidelines.legal_rules.length > 0) && (
        <CollapsibleSection title="Guidelines & Risks" onCopy={copyGuidelines}>
          <div className="space-y-5">
            {results.guidelines.copy_rules.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">Copy Rules</h3>
                <ul className="list-disc list-inside text-gray-700 space-y-1">
                  {results.guidelines.copy_rules.map((rule, idx) => (
                    <li key={idx}>{rule}</li>
                  ))}
                </ul>
              </div>
            )}

            {results.guidelines.design_rules.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">Design Rules</h3>
                <ul className="list-disc list-inside text-gray-700 space-y-1">
                  {results.guidelines.design_rules.map((rule, idx) => (
                    <li key={idx}>{rule}</li>
                  ))}
                </ul>
              </div>
            )}

            {results.guidelines.accessibility_rules.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">Accessibility Rules</h3>
                <ul className="list-disc list-inside text-gray-700 space-y-1">
                  {results.guidelines.accessibility_rules.map((rule, idx) => (
                    <li key={idx}>{rule}</li>
                  ))}
                </ul>
              </div>
            )}

            {results.guidelines.legal_rules.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">Legal Rules</h3>
                <ul className="list-disc list-inside text-gray-700 space-y-1">
                  {results.guidelines.legal_rules.map((rule, idx) => (
                    <li key={idx}>{rule}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </CollapsibleSection>
      )}

      {/* Action Items */}
      {results.action_items.length > 0 && (
        <CollapsibleSection title="Action Items" onCopy={copyActionItems}>
          <ol className="list-decimal list-inside text-gray-700 space-y-2">
            {results.action_items.map((item, idx) => (
              <li key={idx} className="pl-2">{item}</li>
            ))}
          </ol>
        </CollapsibleSection>
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
            <span className="ml-2 font-medium text-gray-900">{formatFileSize(results.file_metadata.file_size)}</span>
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
