"""
Simple HTTP server to serve training status page
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8080
HANDLER = http.server.SimpleHTTPRequestHandler

os.chdir(Path(__file__).parent)

print(f"🚀 Starting HTTP server on http://localhost:{PORT}")
print(f"📄 Serving status.html")
print(f"Press Ctrl+C to stop\n")

with socketserver.TCPServer(("", PORT), HANDLER) as httpd:
    print(f"✅ Server running. Open browser to: http://localhost:{PORT}/status.html")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
