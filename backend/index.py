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
            "message": "Rentum AI backend is working!",
            "status": "success",
            "method": "GET",
            "path": self.path,
            "location": "root backend folder"
        }
        
        # Send JSON response
        self.wfile.write(json.dumps(response_data).encode()) 