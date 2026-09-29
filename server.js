const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const PORT = Number(process.env.PORT || 3000);
const HOST = '0.0.0.0';
const PUBLIC_DIR = path.join(__dirname, 'public');

const contentTypes = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.ico': 'image/x-icon',
  '.txt': 'text/plain; charset=utf-8',
};

function securityHeaders() {
  return {
    'Content-Security-Policy': "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'none'; frame-ancestors 'none'; upgrade-insecure-requests",
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=()',
    'Cross-Origin-Opener-Policy': 'same-origin',
  };
}

function sendFile(res, filePath, status = 200) {
  const extension = path.extname(filePath).toLowerCase();
  const headers = {
    ...securityHeaders(),
    'Content-Type': contentTypes[extension] || 'application/octet-stream',
    'Cache-Control': extension === '.html' ? 'no-cache' : 'public, max-age=604800, immutable',
  };
  const stream = fs.createReadStream(filePath);
  stream.on('error', () => {
    if (!res.headersSent) res.writeHead(500, { ...securityHeaders(), 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Internal server error');
  });
  res.writeHead(status, headers);
  stream.pipe(res);
}

const server = http.createServer((req, res) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.writeHead(405, { ...securityHeaders(), Allow: 'GET, HEAD', 'Content-Type': 'text/plain; charset=utf-8' });
    return res.end('Method not allowed');
  }

  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  if (url.pathname === '/health') {
    res.writeHead(200, { ...securityHeaders(), 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
    return res.end(JSON.stringify({ status: 'ok' }));
  }

  let requestedPath;
  try {
    requestedPath = decodeURIComponent(url.pathname);
  } catch {
    res.writeHead(400, { ...securityHeaders(), 'Content-Type': 'text/plain; charset=utf-8' });
    return res.end('Bad request');
  }

  const relativePath = requestedPath === '/' ? 'index.html' : requestedPath.replace(/^\/+/, '');
  const filePath = path.resolve(PUBLIC_DIR, relativePath);
  if (!filePath.startsWith(`${PUBLIC_DIR}${path.sep}`)) {
    res.writeHead(403, { ...securityHeaders(), 'Content-Type': 'text/plain; charset=utf-8' });
    return res.end('Forbidden');
  }

  fs.stat(filePath, (error, stats) => {
    if (!error && stats.isFile()) {
      if (req.method === 'HEAD') {
        res.writeHead(200, { ...securityHeaders(), 'Content-Type': contentTypes[path.extname(filePath).toLowerCase()] || 'application/octet-stream' });
        return res.end();
      }
      return sendFile(res, filePath);
    }
    const notFound = path.join(PUBLIC_DIR, '404.html');
    return sendFile(res, notFound, 404);
  });
});

server.listen(PORT, HOST, () => {
  console.log(`Portfolio listening on http://${HOST}:${PORT}`);
});

function shutdown() {
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(1), 5000).unref();
}
process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
