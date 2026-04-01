// ServerBadge.jsx — Color-coded badge for server type

const SERVER_MAP = {
  'nginx':              { label: 'Nginx',              cls: 'badge-nginx',      icon: '⬡' },
  'apache':             { label: 'Apache',             cls: 'badge-apache',     icon: '🪶' },
  'cloudflare':         { label: 'Cloudflare',         cls: 'badge-cloudflare', icon: '☁' },
  'google web server':  { label: 'GWS',                cls: 'badge-google',     icon: '◈' },
  'microsoft iis':      { label: 'IIS',                cls: 'badge-iis',        icon: '⊞' },
  'ftp server':         { label: 'FTP',                cls: 'badge-ftp',        icon: '⊙' },
};

// Map the card accent color per server
export const accentColorMap = {
  'nginx':              '#00ff88',
  'apache':             '#f97316',
  'cloudflare':         '#f59e0b',
  'google web server':  '#60a5fa',
  'microsoft iis':      '#818cf8',
  'ftp server':         '#f472b6',
  'unknown':            '#475569',
};

export default function ServerBadge({ type }) {
  const key = (type || 'Unknown').toLowerCase();
  const info = SERVER_MAP[key] || { label: type || 'Unknown', cls: 'badge-unknown', icon: '?' };

  return (
    <span className={`server-badge ${info.cls}`}>
      <span>{info.icon}</span>
      {info.label}
    </span>
  );
}
