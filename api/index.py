from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, Any

# ===== EMBEDDED OCR SERVICE =====
# No external dependencies for Vercel serverless
class OCRService:
    def __init__(self):
        """Initialize simplified OCR service for demo"""
        self.status = "demo_mode"
    
    def process_document(self, file_content: bytes, document_type: str) -> Dict[str, Any]:
        """Process document - returns demo data for Vercel deployment"""
        return {
            'status': 'success',
            'extracted_data': self._get_demo_data(document_type),
            'confidence_scores': {
                'overall': 0.95,
                'text_detection': 0.98,
                'data_extraction': 0.92
            },
            'processing_time': datetime.now().isoformat(),
            'mode': 'serverless_demo'
        }
    
    def _get_demo_data(self, document_type: str) -> Dict[str, Any]:
        """Return demo data based on document type"""
        if document_type == 'rental_agreement':
            return {
                'tenant_name': 'John Doe',
                'landlord_name': 'Jane Smith',
                'property_address': '123 Demo Street, Demo City, DC 12345',
                'monthly_rent': '1500',
                'security_deposit': '3000',
                'lease_start_date': '01/01/2024',
                'lease_end_date': '12/31/2024'
            }
        elif document_type == 'id_card':
            return {
                'name': 'Demo User',
                'id_number': 'ID123456789',
                'date_of_birth': '01/01/1990',
                'address': '456 Demo Avenue, Demo City, DC 12345'
            }
        elif document_type == 'property_document':
            return {
                'property_type': 'Apartment',
                'area': '1200',
                'bedrooms': '2',
                'bathrooms': '1'
            }
        else:
            return {
                'document_type': document_type,
                'text': 'Demo document content extracted successfully'
            }

# ===== GLOBAL INSTANCES =====
# Initialize service instance BEFORE FastAPI app
ocr_service = OCRService()

# ===== DEMO DATA =====
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

# Storage for OCR results (in-memory for demo)
ocr_results = []

# ===== FASTAPI APPLICATION =====
# NO LIFESPAN - Not supported in Vercel serverless
app = FastAPI(
    title="Rentum AI API",
    description="Property Management Platform with OCR",
    version="1.0.0",
)

# ===== CORS MIDDLEWARE =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== API ROUTES =====

@app.get("/")
async def root():
    return {
        "status": "✅ WORKING",
        "message": "Rentum AI Backend is operational!",
        "timestamp": datetime.now().isoformat(),
        "deployment": "vercel-serverless-fixed-v2",
        "endpoints": ["/demo", "/users", "/properties", "/health", "/ocr/scan", "/test"],
        "version": "1.0.0",
        "framework": "FastAPI"
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
        "ocr_service": ocr_service.status,
        "environment": "vercel-serverless"
    }

@app.get("/test")
async def test():
    return {
        "message": "Test endpoint working!",
        "status": "success",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/ocr/scan")
async def scan_document(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    document_type: str = Form(...)
):
    """OCR document scanning endpoint"""
    try:
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
            "timestamp": datetime.now().isoformat(),
            **ocr_result
        }
        
        # Store result
        ocr_results.append(scan_result)
        
        return scan_result
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"OCR processing failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@app.get("/ocr/scans")
async def list_ocr_scans(user_id: str = None):
    """List OCR scan results"""
    if user_id:
        return {
            "scans": [scan for scan in ocr_results if scan["user_id"] == user_id],
            "total": len([scan for scan in ocr_results if scan["user_id"] == user_id])
        }
    return {
        "scans": ocr_results,
        "total": len(ocr_results)
    }

# ===== VERCEL HANDLER EXPORTS =====
# Correct ASGI exports for Vercel Python runtime with FastAPI
app_asgi = app
handler = app 