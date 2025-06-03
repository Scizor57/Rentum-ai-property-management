from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Send a simple HTML response
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        
        # Simple HTML response
        html_response = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Rentum AI Backend</title>
        </head>
        <body>
            <h1>🎉 SUCCESS!</h1>
            <h2>Rentum AI Backend is Working!</h2>
            <p><strong>Status:</strong> ✅ Function is running</p>
            <p><strong>Path:</strong> {}</p>
            <p><strong>Method:</strong> GET</p>
            <p><strong>Location:</strong> Root backend folder</p>
            <hr>
            <p>Next step: Add FastAPI endpoints</p>
        </body>
        </html>
        """.format(self.path)
        
        self.wfile.write(html_response.encode('utf-8'))
        
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 