from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json

# Create FastAPI application
app = FastAPI(
    title="Rentum AI API",
    description="Property Management Platform",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Demo data
DEMO_USERS = [
    {"id": "1", "name": "Alice Johnson", "email": "alice@demo.com", "role": "tenant"},
    {"id": "2", "name": "Bob Smith", "email": "bob@demo.com", "role": "landlord"},
    {"id": "3", "name": "Carol Davis", "email": "carol@demo.com", "role": "tenant"},
    {"id": "4", "name": "David Wilson", "email": "david@demo.com", "role": "landlord"}
]

DEMO_PROPERTIES = [
    {"id": "1", "address": "123 Main St", "owner_id": "2", "status": "active"},
    {"id": "2", "address": "456 Oak Ave", "owner_id": "4", "status": "active"}
]

# Routes
@app.get("/")
async def root():
    return {
        "status": "✅ WORKING",
        "message": "Rentum AI Backend is operational!",
        "timestamp": datetime.now().isoformat(),
        "deployment": "vercel-serverless",
        "endpoints": ["/demo", "/users", "/properties", "/health"]
    }

@app.get("/demo")
async def demo():
    return {
        "message": "🎭 Demo data ready for testing",
        "users": DEMO_USERS,
        "properties": DEMO_PROPERTIES,
        "total_users": len(DEMO_USERS),
        "total_properties": len(DEMO_PROPERTIES)
    }

@app.get("/users")
async def get_users():
    return {"users": DEMO_USERS}

@app.get("/properties")
async def get_properties():
    return {"properties": DEMO_PROPERTIES}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "rentum-api",
        "version": "1.0.0"
    }

@app.get("/test")
async def test():
    return {"message": "Test endpoint working!", "status": "success"}

# Vercel handler - this is the key fix!
handler = app

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 