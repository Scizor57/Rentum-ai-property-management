from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
import json

# Initialize FastAPI app
app = FastAPI(
    title="Rentum AI Backend",
    description="Property Management Platform with AI-powered OCR and Review System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
        "*"  # For demo purposes
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo
users_db = [
    {
        "id": "1",
        "name": "Alice Johnson",
        "email": "alice.tenant@demo.com",
        "phone": "+1-555-0101",
        "role": "tenant",
        "created_at": "2024-01-01T00:00:00"
    },
    {
        "id": "2",
        "name": "Bob Smith",
        "email": "bob.landlord@demo.com",
        "phone": "+1-555-0102",
        "role": "landlord",
        "created_at": "2024-01-01T00:00:00"
    },
    {
        "id": "3",
        "name": "Carol Davis",
        "email": "carol.tenant@demo.com",
        "phone": "+1-555-0103",
        "role": "tenant",
        "created_at": "2024-01-01T00:00:00"
    },
    {
        "id": "4",
        "name": "David Wilson",
        "email": "david.landlord@demo.com",
        "phone": "+1-555-0104",
        "role": "landlord",
        "created_at": "2024-01-01T00:00:00"
    }
]

properties_db = [
    {
        "id": "1",
        "owner_id": "2",
        "address": "123 Main St, Downtown City",
        "details": {"bedrooms": 2, "bathrooms": 1, "area": "1200 sq ft"},
        "status": "active",
        "created_at": "2024-01-01T00:00:00"
    },
    {
        "id": "2",
        "owner_id": "4",
        "address": "456 Oak Ave, Riverside District",
        "details": {"bedrooms": 3, "bathrooms": 2, "area": "1800 sq ft"},
        "status": "active",
        "created_at": "2024-01-01T00:00:00"
    }
]

agreements_db = [
    {
        "id": "1",
        "property_id": "1",
        "landlord_id": "2",
        "tenant_id": "1",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "rent": 1500.0,
        "deposit": 3000.0,
        "status": "active",
        "created_at": "2024-01-01T00:00:00"
    }
]

ocr_scans_db = []
review_requests_db = []
review_responses_db = []

# Pydantic models
class UserOut(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str]
    role: str
    created_at: str

class PropertyOut(BaseModel):
    id: str
    owner_id: str
    address: str
    details: Optional[dict]
    status: str
    created_at: str

class AgreementOut(BaseModel):
    id: str
    property_id: str
    landlord_id: str
    tenant_id: str
    start_date: str
    end_date: str
    rent: float
    deposit: float
    status: str
    created_at: str

class OCRScanOut(BaseModel):
    id: str
    user_id: str
    document_type: str
    extracted_data: dict
    confidence_scores: dict
    status: str
    created_at: str

# API Endpoints
@app.get("/")
async def read_root():
    return {
        "message": "🎉 Rentum AI Backend is running successfully!",
        "status": "operational",
        "version": "1.0.0",
        "environment": "production",
        "deployment": "vercel",
        "features": [
            "✅ User Management",
            "✅ Property Management", 
            "✅ Rental Agreements",
            "✅ OCR Document Scanning",
            "✅ AI Review System",
            "✅ Demo Data Available"
        ]
    }

@app.get("/demo")
async def get_demo_info():
    return {
        "message": "🎭 Demo users and data available for testing",
        "total_users": len(users_db),
        "total_properties": len(properties_db),
        "total_agreements": len(agreements_db),
        "users": users_db,
        "properties": properties_db,
        "agreements": agreements_db,
        "instructions": [
            "Use any email from users list to test login",
            "Upload documents for OCR testing",
            "Create review requests between users",
            "All data is stored in memory for demo"
        ],
        "api_endpoints": [
            "GET /users - List all users",
            "GET /properties - List all properties", 
            "GET /agreements - List all agreements",
            "POST /ocr/scan - Upload document for OCR",
            "GET /health - Health check"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "running",
        "database": "in-memory",
        "services": {
            "api": "✅ operational",
            "ocr": "✅ ready", 
            "ai_review": "✅ ready",
            "cors": "✅ enabled"
        }
    }

@app.get("/users", response_model=List[UserOut])
async def list_users():
    return users_db

@app.get("/properties", response_model=List[PropertyOut]) 
async def list_properties():
    return properties_db

@app.get("/agreements", response_model=List[AgreementOut])
async def list_agreements():
    return agreements_db

@app.post("/ocr/scan", response_model=OCRScanOut)
async def scan_document(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    document_type: str = Form(...)
):
    """Demo OCR endpoint - simulates document scanning"""
    
    # Simulate OCR processing
    new_scan = {
        "id": str(len(ocr_scans_db) + 1),
        "user_id": user_id,
        "document_type": document_type,
        "extracted_data": {
            "tenant_name": "John Doe",
            "landlord_name": "Jane Smith", 
            "property_address": "123 Demo Street",
            "monthly_rent": "1500",
            "security_deposit": "3000",
            "lease_start_date": "01/01/2024",
            "lease_end_date": "12/31/2024"
        },
        "confidence_scores": {
            "overall": 0.95,
            "text_detection": 0.98,
            "data_extraction": 0.92
        },
        "status": "completed",
        "created_at": datetime.now().isoformat()
    }
    
    ocr_scans_db.append(new_scan)
    return new_scan

@app.get("/ocr/scans")
async def list_ocr_scans(user_id: str = None):
    """List OCR scans, optionally filtered by user"""
    if user_id:
        return [scan for scan in ocr_scans_db if scan["user_id"] == user_id]
    return ocr_scans_db

@app.post("/reviews/request")
async def create_review_request(
    requester_id: str = Form(...),
    reviewer_email: str = Form(...),
    request_type: str = Form(...),
    property_id: str = Form(None)
):
    """Create a new review request"""
    new_request = {
        "id": str(len(review_requests_db) + 1),
        "requester_id": requester_id,
        "reviewer_email": reviewer_email,
        "request_type": request_type,
        "property_id": property_id,
        "status": "pending",
        "deadline": "2024-12-31T23:59:59",
        "created_at": datetime.now().isoformat()
    }
    
    review_requests_db.append(new_request)
    return new_request

@app.get("/reviews/requests")
async def list_review_requests(user_id: str = None):
    """List review requests"""
    if user_id:
        return [req for req in review_requests_db if req["requester_id"] == user_id]
    return review_requests_db

@app.post("/reviews/response")
async def submit_review_response(
    request_id: str = Form(...),
    overall_rating: int = Form(...),
    comments: str = Form(""),
    payment_reliability: int = Form(None),
    communication: int = Form(None),
    property_maintenance: int = Form(None)
):
    """Submit a review response with AI analysis"""
    
    # Simulate AI analysis
    new_response = {
        "id": str(len(review_responses_db) + 1),
        "request_id": request_id,
        "overall_rating": overall_rating,
        "comments": comments,
        "payment_reliability": payment_reliability,
        "communication": communication,
        "property_maintenance": property_maintenance,
        "ai_overall_score": min(overall_rating * 0.85 + 0.15, 5.0),
        "ai_risk_assessment": "low" if overall_rating >= 4 else "medium" if overall_rating >= 3 else "high",
        "ai_green_flags": ["Reliable payments", "Good communication"] if overall_rating >= 4 else [],
        "ai_red_flags": ["Late payments", "Poor maintenance"] if overall_rating < 3 else [],
        "ai_analysis_summary": f"Based on {overall_rating}/5 rating, this appears to be a {'positive' if overall_rating >= 4 else 'mixed' if overall_rating >= 3 else 'concerning'} review.",
        "created_at": datetime.now().isoformat()
    }
    
    review_responses_db.append(new_response)
    return new_response

@app.get("/stats")
async def get_stats():
    """Get platform statistics"""
    return {
        "total_users": len(users_db),
        "total_properties": len(properties_db), 
        "total_agreements": len(agreements_db),
        "total_ocr_scans": len(ocr_scans_db),
        "total_review_requests": len(review_requests_db),
        "total_review_responses": len(review_responses_db),
        "user_breakdown": {
            "tenants": len([u for u in users_db if u["role"] == "tenant"]),
            "landlords": len([u for u in users_db if u["role"] == "landlord"])
        },
        "system_status": "operational"
    }

# For Vercel deployment
handler = app 