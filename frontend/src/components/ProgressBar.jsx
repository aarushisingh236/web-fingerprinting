// ProgressBar.jsx — Live scan progress tracker

export default function ProgressBar({ targets, scanningTarget, completedHosts }) {
  const total = targets.length;
  const done = completedHosts.size;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  return (
    <div className="progress-section">
      <div className="progress-header">
        <span className="progress-label">⟳ SCANNING TARGETS</span>
        <span className="progress-count">{done} / {total} complete</span>
      </div>

      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${pct}%` }} />
      </div>

      <div className="scanning-row">
        {targets.map((t, i) => {
          const isDone = completedHosts.has(t);
          const isActive = scanningTarget === t;
          return (
            <div
              key={i}
              className={`scanning-chip ${isDone ? 'done' : ''}`}
              style={{ borderColor: isActive ? 'rgba(0,212,255,0.4)' : undefined }}
            >
              {!isDone && <span className={`spinner ${!isActive ? 'pending' : ''}`} style={{ opacity: isActive ? 1 : 0.3 }} />}
              <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {t}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
