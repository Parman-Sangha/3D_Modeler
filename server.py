#!/usr/bin/env python3
"""
Simple HTTP server to serve the 3D viewer
Run: python3 server.py
Then open http://localhost:8000/viewer.html
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    os.chdir(Path(__file__).parent)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}/viewer.html"
        print("=" * 60)
        print("🚀 3D Modeler Pro - Web Viewer")
        print("=" * 60)
        print(f"\n📡 Server running at: {url}")
        print(f"\n📁 Serving files from: {os.getcwd()}")
        print("\n💡 Tips:")
        print("   - Load a JSON file using the file picker")
        print("   - Or place 'demo_scene.json' in this directory")
        print("   - Use mouse to rotate, zoom, and pan")
        print("\n🛑 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Try to open browser automatically
        try:
            webbrowser.open(url)
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")

if __name__ == "__main__":
    main()
