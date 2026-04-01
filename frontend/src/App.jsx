// App.jsx — Main application component with SSE streaming

import { useState, useRef } from 'react';
import ScanInput from './components/ScanInput.jsx';
import ProgressBar from './components/ProgressBar.jsx';
import ScanResults from './components/ScanResults.jsx';

export default function App() {
  const [targetText, setTargetText] = useState('github.com\nnginx.org\ngoogle.com\ncloudflare.com');
  const [isScanning, setIsScanning] = useState(false);
  const [results, setResults] = useState([]);
  const [scanTargets, setScanTargets] = useState([]);
  const [scanningTarget, setScanningTarget] = useState(null);
  const [completedHosts, setCompletedHosts] = useState(new Set());
  const [error, setError] = useState(null);
  const abortRef = useRef(null);

  const parseTargets = (text) =>
    text.split(/[\n,]+/).map(t => t.trim()).filter(Boolean);

  const handleScan = async () => {
    const targets = parseTargets(targetText);
    if (targets.length === 0) return;

    setIsScanning(true);
    setResults([]);
    setError(null);
    setScanTargets(targets);
    setScanningTarget(null);
    setCompletedHosts(new Set());

    // Abort any existing connection
    if (abortRef.current) abortRef.current.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    try {
      const response = await fetch('/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ targets }),
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // Keep incomplete line

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));

              if (data.status === 'scanning') {
                setScanningTarget(data.target);
              } else if (data.status === 'done') {
                setResults(prev => [...prev, data]);
                setCompletedHosts(prev => new Set([...prev, data.host]));
                setScanningTarget(null);
              } else if (data.status === 'error') {
                setResults(prev => [...prev, {
                  ...data,
                  server_type: 'Unknown',
                  server_header: `Error: ${data.message}`,
                  source: 'N/A',
                }]);
                setCompletedHosts(prev => new Set([...prev, data.host]));
              }
            } catch (_) {
              // skip malformed SSE line
            }
          }
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        setError('Could not connect to backend. Make sure the Flask server is running on port 5000.');
        console.error(err);
      }
    } finally {
      setIsScanning(false);
      setScanningTarget(null);
    }
  };

  const handleClear = () => {
    if (abortRef.current) abortRef.current.abort();
    setResults([]);
    setScanTargets([]);
    setCompletedHosts(new Set());
    setError(null);
    setIsScanning(false);
    setTargetText('');
  };

  const handleExport = () => {
    const lines = ['Web Fingerprinting Results', '='.repeat(40)];
    for (const r of results) {
      lines.push('');
      lines.push(`Host:   ${r.host}`);
      lines.push(`Server: ${r.server_type}`);
      lines.push(`Header: ${r.server_header}`);
      lines.push(`Source: ${r.source}`);
      lines.push('-'.repeat(40));
    }
    const blob = new Blob([lines.join('\n')], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'fingerprint-results.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="app-container">

      {/* Header */}
      <header className="app-header">
        <div className="header-badge">
          <span className="dot" />
          WEB FINGERPRINT TOOL
        </div>
        <h1 className="app-title">Server Fingerprinting</h1>
        <p className="app-subtitle">
          Identify web server types using HTTP, HTTPS & FTP banner analysis with real-time scanning.
        </p>
      </header>

      {/* Error Banner */}
      {error && (
        <div className="error-banner">
          <span>⚠</span>
          {error}
        </div>
      )}

      {/* Scan Input */}
      <ScanInput
        value={targetText}
        onChange={setTargetText}
        onScan={handleScan}
        onClear={handleClear}
        isScanning={isScanning}
      />

      {/* Progress bar (shown while scanning) */}
      {isScanning && scanTargets.length > 0 && (
        <ProgressBar
          targets={scanTargets}
          scanningTarget={scanningTarget}
          completedHosts={completedHosts}
        />
      )}

      <div className="divider" />

      {/* Results */}
      <ScanResults
        results={results}
        onExport={handleExport}
      />

      <footer className="app-footer">
        WEB-FINGERPRINT-TOOL · PYTHON BACKEND · REACT FRONTEND
      </footer>
    </div>
  );
}
