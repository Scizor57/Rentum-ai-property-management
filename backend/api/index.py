import sys
import os

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# Vercel expects a function called 'app' or a function to handle requests
# This exports our FastAPI app for Vercel
def handler(request, response):
    return app

# Export the app for Vercel
application = app 