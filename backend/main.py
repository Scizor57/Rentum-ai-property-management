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
def root():
    return {
        "status": "✅ WORKING",
        "message": "Rentum AI Backend is operational!",
        "timestamp": datetime.now().isoformat(),
        "deployment": "vercel-optimized",
        "endpoints": ["/demo", "/users", "/properties", "/health"]
    }

@app.get("/demo")
def demo():
    return {
        "message": "🎭 Demo data ready for testing",
        "users": DEMO_USERS,
        "properties": DEMO_PROPERTIES,
        "total_users": len(DEMO_USERS),
        "total_properties": len(DEMO_PROPERTIES)
    }

@app.get("/users")
def get_users():
    return {"users": DEMO_USERS}

@app.get("/properties")
def get_properties():
    return {"properties": DEMO_PROPERTIES}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "rentum-api",
        "version": "1.0.0"
    }

@app.get("/test")
def test():
    return {"message": "Test endpoint working!", "status": "success"}

# Vercel serverless function handler
handler = app 