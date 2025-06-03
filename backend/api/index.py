from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set response headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Response data
        response_data = {
            "message": "Rentum AI backend is running!",
            "status": "success",
            "method": "GET",
            "path": self.path,
            "vercel": "working"
        }
        
        # Send JSON response
        self.wfile.write(json.dumps(response_data).encode())
        
    def do_POST(self):
        # Set response headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Response data
        response_data = {
            "message": "POST request received",
            "status": "success",
            "method": "POST",
            "path": self.path
        }
        
        # Send JSON response
        self.wfile.write(json.dumps(response_data).encode()) 