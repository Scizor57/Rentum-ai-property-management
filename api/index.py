from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from .ocr_service import ocr_service

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

# Storage for OCR results
ocr_results = []

# Routes
@app.get("/")
async def root():
    return {
        "status": "✅ WORKING",
        "message": "Rentum AI Backend is operational!",
        "timestamp": datetime.now().isoformat(),
        "deployment": "vercel-api-folder",
        "endpoints": ["/demo", "/users", "/properties", "/health", "/ocr/scan"]
    }

@app.get("/demo")
async def demo():
    return {
        "message": "🎭 Demo data ready for testing",
        "users": DEMO_USERS,
        "properties": DEMO_PROPERTIES,
        "total_users": len(DEMO_USERS),
        "total_properties": len(DEMO_PROPERTIES),
        "ocr_service": "✅ Available",
        "ocr_results": len(ocr_results)
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
        "version": "1.0.0",
        "ocr_service": ocr_service.status
    }

@app.get("/test")
async def test():
    return {"message": "Test endpoint working!", "status": "success"}

@app.post("/ocr/scan")
async def scan_document(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    document_type: str = Form(...)
):
    """OCR document scanning endpoint"""
    
    # Read file content
    file_content = await file.read()
    
    # Process with OCR service
    ocr_result = ocr_service.process_document(file_content, document_type)
    
    # Add metadata
    scan_result = {
        "id": str(len(ocr_results) + 1),
        "user_id": user_id,
        "document_type": document_type,
        "filename": file.filename,
        "file_size": len(file_content),
        **ocr_result
    }
    
    # Store result
    ocr_results.append(scan_result)
    
    return scan_result

@app.get("/ocr/scans")
async def list_ocr_scans(user_id: str = None):
    """List OCR scan results"""
    if user_id:
        return [scan for scan in ocr_results if scan["user_id"] == user_id]
    return ocr_results

# Vercel handler - standard pattern for api folder
handler = app 