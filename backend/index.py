from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(title="Rentum AI Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Demo data
users_db = [
    {"id": "1", "name": "Alice Johnson", "email": "alice.tenant@demo.com", "role": "tenant"},
    {"id": "2", "name": "Bob Smith", "email": "bob.landlord@demo.com", "role": "landlord"},
    {"id": "3", "name": "Carol Davis", "email": "carol.tenant@demo.com", "role": "tenant"},
    {"id": "4", "name": "David Wilson", "email": "david.landlord@demo.com", "role": "landlord"}
]

properties_db = [
    {"id": "1", "owner_id": "2", "address": "123 Main St, Downtown City", "status": "active"},
    {"id": "2", "owner_id": "4", "address": "456 Oak Ave, Riverside District", "status": "active"}
]

@app.get("/")
async def root():
    return {
        "message": "🎉 Rentum AI Backend is WORKING!",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "deployment": "vercel",
        "version": "1.0.0"
    }

@app.get("/api")
async def api_root():
    return {"message": "API is working!", "status": "success"}

@app.get("/demo")
async def demo():
    return {
        "message": "Demo data available",
        "users": users_db,
        "properties": properties_db,
        "total_users": len(users_db),
        "total_properties": len(properties_db)
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/users")
async def get_users():
    return users_db

@app.get("/properties")
async def get_properties():
    return properties_db

# Export for Vercel
handler = app 