from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set response headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Demo users data
        demo_users = [
            {"name": "Alice Johnson", "email": "alice.tenant@demo.com", "role": "tenant"},
            {"name": "Bob Smith", "email": "bob.landlord@demo.com", "role": "landlord"},
            {"name": "Carol Davis", "email": "carol.tenant@demo.com", "role": "tenant"},
            {"name": "David Wilson", "email": "david.landlord@demo.com", "role": "landlord"}
        ]
        
        response_data = {
            "message": "Demo users available for testing",
            "users": demo_users,
            "instructions": "Use any email above to login",
            "features": [
                "🔍 Upload documents for AI OCR scanning",
                "🤖 AI-powered review system", 
                "🏠 Property management",
                "💳 Payment tracking",
                "📊 Dashboard with insights"
            ]
        }
        
        # Send JSON response
        self.wfile.write(json.dumps(response_data).encode()) 