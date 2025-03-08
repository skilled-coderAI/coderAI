import { useState } from 'react';
import coderAIService from '../services/coderAIService';
import ReactMarkdown from 'react-markdown';

const CodeAnalysis = () => {
  const [code, setCode] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!code.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const result = await coderAIService.analyzeCode(code);
      setAnalysis(result);
    } catch (err) {
      setError('Failed to analyze code. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4 text-white">Code Analysis</h2>
      <div className="mb-4">
        <textarea
          className="w-full h-48 p-3 bg-gray-800 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Paste your code here..."
        />
      </div>
      <button
        onClick={handleAnalyze}
        disabled={loading}
        className={`px-4 py-2 rounded-lg ${loading ? 'bg-gray-600' : 'bg-blue-600 hover:bg-blue-700'} text-white font-medium transition-colors`}
      >
        {loading ? 'Analyzing...' : 'Analyze Code'}
      </button>

      {error && (
        <div className="mt-4 p-3 bg-red-500 bg-opacity-20 border border-red-500 rounded-lg text-red-500">
          {error}
        </div>
      )}

      {analysis && (
        <div className="mt-6 p-4 bg-gray-800 rounded-lg">
          <h3 className="text-xl font-semibold mb-3 text-white">Analysis Results</h3>
          <div className="prose prose-invert">
            <ReactMarkdown>{analysis.result}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
};

export default CodeAnalysis;