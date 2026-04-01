// ScanInput.jsx — Target input form

export default function ScanInput({ value, onChange, onScan, onClear, isScanning }) {
  const handleKeyDown = (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
      onScan();
    }
  };

  return (
    <div className="scan-panel">
      <div className="scan-panel-label">TARGET HOSTS</div>

      <textarea
        className="targets-textarea"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={`github.com\nnginx.org\ngoogle.com\ncloudflare.com`}
        disabled={isScanning}
        spellCheck={false}
      />

      <div className="scan-actions">
        <button
          className="btn-scan"
          onClick={onScan}
          disabled={isScanning || !value.trim()}
          id="btn-start-scan"
        >
          {isScanning ? (
            <>
              <span className="spinner" style={{ width: 14, height: 14, borderWidth: 2 }} />
              SCANNING...
            </>
          ) : (
            <>
              <span>⟳</span>
              RUN SCAN
            </>
          )}
        </button>

        <button
          className="btn-clear"
          onClick={onClear}
          disabled={isScanning}
          id="btn-clear"
        >
          CLEAR
        </button>

        <span className="scan-hint">Ctrl+Enter to scan</span>
      </div>
    </div>
  );
}
