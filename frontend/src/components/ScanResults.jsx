// ScanResults.jsx — Result cards with server badge + detail fields

import ServerBadge, { accentColorMap } from './ServerBadge.jsx';

const KNOWN_SERVERS = {
  'nginx.org':       'Nginx',
  'github.com':      'Cloudflare',
  'cloudflare.com':  'Cloudflare',
  'example.com':     'Cloudflare',
  'google.com':      'Google Web Server',
  'youtube.com':     'Google Web Server',
};

function calcAccuracy(results) {
  let correct = 0, checked = 0;
  for (const r of results) {
    const expected = KNOWN_SERVERS[r.host];
    if (expected) {
      checked++;
      if (r.server_type === expected) correct++;
    }
  }
  return checked > 0 ? Math.round((correct / checked) * 100) : null;
}

function ResultCard({ result, animDelay }) {
  const accentColor = accentColorMap[(result.server_type || 'Unknown').toLowerCase()] || '#475569';

  return (
    <div
      className="result-card"
      style={{
        '--accent-color': accentColor,
        animationDelay: `${animDelay}ms`
      }}
      id={`result-${result.host.replace(/\./g, '-')}`}
    >
      <div className="result-card-top">
        <span className="result-host">{result.host}</span>
        <div className="result-badges">
          <ServerBadge type={result.server_type} />
          <span className="source-badge">{result.source}</span>
        </div>
      </div>

      <div className="result-card-bottom">
        <div className="result-field result-card-full">
          <span className="result-field-label">Server Header</span>
          <span className="result-field-value" style={{ color: accentColor, opacity: 0.9 }}>
            {result.server_header || '—'}
          </span>
        </div>
      </div>
    </div>
  );
}

export default function ScanResults({ results, onExport }) {
  if (results.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-icon">⬡</div>
        <h3>NO SCAN RESULTS YET</h3>
        <p>Enter one or more hostnames above<br />and press RUN SCAN to begin fingerprinting.</p>
      </div>
    );
  }

  const accuracy = calcAccuracy(results);

  return (
    <div className="results-section">
      <div className="results-header">
        <span className="results-title">// SCAN RESULTS — {results.length} host{results.length !== 1 ? 's' : ''}</span>
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          {accuracy !== null && (
            <span className="accuracy-badge">
              ◈ Accuracy: {accuracy}%
            </span>
          )}
          <button className="btn-export" onClick={onExport} id="btn-export">
            ↓ EXPORT TXT
          </button>
        </div>
      </div>

      <div className="results-list">
        {results.map((r, i) => (
          <ResultCard key={r.host} result={r} animDelay={i * 60} />
        ))}
      </div>
    </div>
  );
}
