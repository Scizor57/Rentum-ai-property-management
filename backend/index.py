from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set response headers properly for browser
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Response data
        response_data = {
            "message": "🎉 Rentum AI backend is working!",
            "status": "success",
            "method": "GET",
            "path": self.path,
            "location": "root backend folder",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        # Send JSON response with proper encoding
        response_json = json.dumps(response_data, indent=2)
        self.wfile.write(response_json.encode('utf-8'))
        
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 