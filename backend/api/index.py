import sys
import os

# Add the parent directory to the path so we can import from backend
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

print(f"🔧 Backend directory: {backend_dir}")
print(f"🔧 Python path: {sys.path[:3]}")

try:
    # Import the FastAPI app
    print("📦 Importing main app...")
    from main import app
    print("✅ Successfully imported FastAPI app")
    
    # Test the app
    print(f"✅ App type: {type(app)}")
    print(f"✅ App routes: {len(app.routes)}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    # Create a basic FastAPI app as fallback
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(title="Rentum AI Backend", description="Property Management Platform")
    
    # Add CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def root():
        return {
            "message": "Rentum AI backend is running (fallback mode)", 
            "error": f"Import error: {str(e)}",
            "backend_dir": backend_dir
        }
        
    @app.get("/demo")
    async def demo():
        return {
            "message": "Demo endpoint (fallback mode)",
            "users": [
                {"name": "Alice Johnson", "email": "alice.tenant@demo.com", "role": "tenant"},
                {"name": "Bob Smith", "email": "bob.landlord@demo.com", "role": "landlord"}
            ]
        }
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def error():
        return {"message": "Error loading app", "error": str(e)}

# Export for Vercel
print(f"🚀 Exporting app: {app}")

# Vercel looks for these variable names
application = app
handler = app 