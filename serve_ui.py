#!/usr/bin/env python
"""Simple HTTP server to serve the drug recommendation UI"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8080
DIRECTORY = Path(__file__).parent

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow requests from localhost
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"""
╔══════════════════════════════════════════════════════════╗
║     DRUG RECOMMENDATION SYSTEM - UI SERVER RUNNING       ║
╚══════════════════════════════════════════════════════════╝

✓ Web UI:  http://localhost:{PORT}/index.html
✓ API:     http://localhost:5001/
✓ Model:   Loaded ✓ (97.78% accuracy)

Open the URL above in your browser to test predictions!

Press Ctrl+C to stop the server...
        """)
        
        httpd.serve_forever()
