const http = require('http');
const fs = require('fs');
const path = require('path');

const port = 8000;
const directory = '/Users/arushitandon/Desktop/UIUX analyzer/ux-analyzer';

const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json'
};

const server = http.createServer((req, res) => {
    let filePath = path.join(directory, req.url === '/' ? 'minimal_dashboard.html' : req.url);
    
    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404, {'Content-Type': 'text/html'});
            res.end(`
                <h1>404 - File Not Found</h1>
                <p>Available dashboards:</p>
                <ul>
                    <li><a href="/minimal_dashboard.html">Minimal Dashboard</a></li>
                    <li><a href="/test_dashboard.html">Test Dashboard</a></li>
                    <li><a href="/simple_dashboard.html">Simple Dashboard</a></li>
                </ul>
            `);
            return;
        }
        
        const ext = path.extname(filePath);
        const contentType = mimeTypes[ext] || 'text/plain';
        
        res.writeHead(200, {'Content-Type': contentType});
        res.end(data);
    });
});

server.listen(port, () => {
    console.log(`🚀 Dashboard server running at http://localhost:${port}`);
    console.log(`📊 Main dashboard: http://localhost:${port}/minimal_dashboard.html`);
});

server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.log(`❌ Port ${port} is already in use. Try a different port.`);
    } else {
        console.error('Server error:', err);
    }
});
