#!/usr/bin/env python3
"""
Unity WebGL Server with Gzip compression support
Serves .gz files with proper Content-Encoding header for Unity WebGL
"""

import http.server
import socketserver
import sys
import os

PORT = 3001

class UnityWebGLHandler(http.server.SimpleHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    
    def guess_type(self, path):
        """Set correct MIME type based on file extension"""
        # Handle .gz files - get MIME type of uncompressed version
        if path.endswith('.gz'):
            path = path[:-3]
        elif path.endswith('.br'):
            path = path[:-3]
        
        # Set Unity WebGL MIME types
        if path.endswith('.wasm'):
            return 'application/wasm'
        elif path.endswith('.data'):
            return 'application/octet-stream'
        elif path.endswith('.js'):
            return 'application/javascript'
        
        return super().guess_type(path)
    
    def end_headers(self):
        """Add custom headers"""
        # CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        
        # Compression headers for .gz files
        if self.path.endswith('.gz'):
            self.send_header('Content-Encoding', 'gzip')
        elif self.path.endswith('.br'):
            self.send_header('Content-Encoding', 'br')
        
        # Other headers
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom logging"""
        if args[1] == '200':
            # Only show successful requests
            print(f"✓ {args[0]}")
        else:
            # Show errors
            print(f"✗ {args[0]} - Status: {args[1]}")

if __name__ == '__main__':
    # Allow quick restart
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("0.0.0.0", PORT), UnityWebGLHandler) as httpd:
        print(f"🚀 Unity WebGL Server (with Gzip support)")
        print(f"   Local:   http://localhost:{PORT}")
        print(f"   Network: http://192.168.1.6:{PORT}")
        print(f"\n📱 iPhone URL: http://192.168.1.6:{PORT}")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped")
            sys.exit(0)
