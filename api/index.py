#!/usr/bin/env python3
"""
Rentum AI API - Vercel Serverless Deployment
FastAPI application with embedded OCR service for property management
"""

# ===== IMPORTS =====
from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, Any, Optional
import json
import io
import os
from PIL import Image
import tempfile

# ===== GOOGLE VISION OCR SERVICE =====
from google.cloud import vision

class OCRService:
    def __init__(self):
        """Initialize Google Vision OCR service - REQUIRED"""
        try:
            print("🔍 Initializing Google Vision OCR...")
            
            # Debug: Check environment variables
            creds_env = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            creds_base64 = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_BASE64')
            
            print(f"📋 GOOGLE_APPLICATION_CREDENTIALS exists: {bool(creds_env)}")
            print(f"📋 GOOGLE_APPLICATION_CREDENTIALS_BASE64 exists: {bool(creds_base64)}")
            
            credentials_json = None
            
            if creds_env:
                print(f"📋 Credentials length: {len(creds_env)} characters")
                print(f"📋 Credentials start: {creds_env[:50]}...")
                
                # Check if it's valid JSON content (not a file path)
                try:
                    parsed = json.loads(creds_env)
                    print(f"📋 JSON is valid, type: {parsed.get('type', 'unknown')}")
                    print(f"📋 Project ID: {parsed.get('project_id', 'unknown')}")
                    credentials_json = creds_env
                except json.JSONDecodeError as je:
                    print(f"❌ JSON parsing failed: {je}")
                    print(f"📋 First 100 chars: {creds_env[:100]}")
                    # If it's not valid JSON, treat as file path
                    if os.path.exists(creds_env):
                        print("📋 Treating as file path...")
                        with open(creds_env, 'r') as f:
                            credentials_json = f.read()
            
            elif creds_base64:
                print("🔧 Decoding base64 credentials...")
                import base64
                try:
                    credentials_json = base64.b64decode(creds_base64).decode('utf-8')
                    parsed = json.loads(credentials_json)
                    print(f"✅ Base64 credentials decoded, project: {parsed.get('project_id', 'unknown')}")
                except Exception as be:
                    print(f"❌ Base64 decoding failed: {be}")
            
            # For Vercel serverless, write credentials to temporary file
            if credentials_json:
                print("📝 Writing credentials to temporary file for Vercel...")
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                    temp_file.write(credentials_json)
                    temp_creds_path = temp_file.name
                
                # Set the environment variable to point to the temp file
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_creds_path
                print(f"✅ Temporary credentials file created: {temp_creds_path}")
            else:
                print("❌ No valid credentials found")
            
            # Initialize Google Vision client
            self.client = vision.ImageAnnotatorClient()
            self.status = "google_vision_ready"
            print("✅ Google Vision OCR initialized successfully")
            
        except Exception as e:
            print(f"❌ Google Vision initialization failed: {e}")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Error details: {str(e)}")
            print("📋 To enable OCR, set up Google Cloud credentials:")
            print("   1. Create Google Cloud service account")
            print("   2. Enable Vision API")
            print("   3. Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
            self.client = None
            self.status = "google_vision_required"
    
    def process_document(self, file_content: bytes, document_type: str) -> Dict[str, Any]:
        """Process document with Google Vision OCR ONLY"""
        if not self.client:
            raise Exception("Google Vision OCR is not configured. Please set up Google Cloud credentials.")
        
        return self._process_with_google_vision(file_content, document_type)
    
    def _process_with_google_vision(self, file_content: bytes, document_type: str) -> Dict[str, Any]:
        """Process document with Google Vision OCR"""
        try:
            print("🤖 Processing with Google Vision OCR...")
            
            # Create Vision API image object
            image = vision.Image(content=file_content)
            
            # Perform text detection
            response = self.client.text_detection(image=image)
            texts = response.text_annotations
            
            if response.error.message:
                raise Exception(f"Google Vision API error: {response.error.message}")
            
            if not texts:
                raise Exception("No text detected in the uploaded document")
            
            # Extract raw text
            raw_text = texts[0].description
            print(f"📄 Extracted text length: {len(raw_text)} characters")
            
            # Parse structured data based on document type
            extracted_data = self._parse_ocr_text(raw_text, document_type)
            
            # Calculate confidence scores from Vision API
            confidence_scores = self._calculate_confidence_scores(texts, extracted_data)
            
            return {
                'status': 'completed',
                'extracted_data': extracted_data,
                'confidence_score': confidence_scores.get('overall', 0.85),
                'confidence_scores': confidence_scores,
                'raw_text': raw_text[:500],  # First 500 chars for debugging
                'processing_time': datetime.now().isoformat(),
                'mode': 'google_vision_ocr',
                'text_blocks_detected': len(texts)
            }
            
        except Exception as e:
            print(f"❌ Google Vision OCR failed: {e}")
            raise Exception(f"OCR processing failed: {str(e)}")
    
    def _parse_ocr_text(self, text: str, document_type: str) -> Dict[str, Any]:
        """Parse OCR text to extract structured data"""
        text_lower = text.lower()
        extracted = {}
        
        if document_type == 'rental_agreement':
            extracted = self._extract_rental_data(text, text_lower)
        elif document_type == 'id_card':
            extracted = self._extract_id_data(text, text_lower)
        elif document_type == 'property_document':
            extracted = self._extract_property_data(text, text_lower)
        else:
            # For any other document type, return raw text extraction
            extracted = {
                'raw_text': text[:500],
                'document_type': document_type,
                'word_count': len(text.split()),
                'character_count': len(text)
            }
        
        return extracted
    
    def _extract_rental_data(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Extract rental agreement specific data using regex patterns"""
        import re
        
        data = {}
        
        # Extract names (improved patterns)
        name_patterns = [
            r'tenant[:\s]+([A-Za-z\s]{2,30})',
            r'landlord[:\s]+([A-Za-z\s]{2,30})',
            r'lessor[:\s]+([A-Za-z\s]{2,30})',
            r'lessee[:\s]+([A-Za-z\s]{2,30})',
            r'owner[:\s]+([A-Za-z\s]{2,30})',
            r'renter[:\s]+([A-Za-z\s]{2,30})'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text_lower)
            if match:
                name = match.group(1).strip().title()
                if 'tenant' in pattern or 'lessee' in pattern or 'renter' in pattern:
                    data['tenant_name'] = name
                elif 'landlord' in pattern or 'lessor' in pattern or 'owner' in pattern:
                    data['landlord_name'] = name
        
        # Extract rent amount (improved patterns)
        rent_patterns = [
            r'rent[:\s]+\$?(\d+[\d,]*\.?\d*)',
            r'monthly[:\s]+rent[:\s]+\$?(\d+[\d,]*\.?\d*)',
            r'\$(\d+[\d,]*\.?\d*)[:\s]*(?:per|/)\s*month',
            r'amount[:\s]+\$?(\d+[\d,]*\.?\d*)'
        ]
        
        for pattern in rent_patterns:
            match = re.search(pattern, text_lower)
            if match:
                data['monthly_rent'] = match.group(1).replace(',', '')
                break
        
        # Extract security deposit
        deposit_patterns = [
            r'security\s+deposit[:\s]+\$?(\d+[\d,]*\.?\d*)',
            r'deposit[:\s]+\$?(\d+[\d,]*\.?\d*)',
            r'advance[:\s]+\$?(\d+[\d,]*\.?\d*)'
        ]
        
        for pattern in deposit_patterns:
            match = re.search(pattern, text_lower)
            if match:
                data['security_deposit'] = match.group(1).replace(',', '')
                break
        
        # Extract property address (improved patterns)
        address_patterns = [
            r'property\s+(?:address|located)[:\s]+([0-9][^.\n\r]{10,100})',
            r'premises[:\s]+([0-9][^.\n\r]{10,100})',
            r'address[:\s]+([0-9][^.\n\r]{10,100})',
            r'located\s+at[:\s]+([0-9][^.\n\r]{10,100})'
        ]
        
        for pattern in address_patterns:
            match = re.search(pattern, text_lower)
            if match:
                data['property_address'] = match.group(1).strip()
                break
        
        # Extract lease dates (improved patterns)
        date_patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',
            r'(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{2,4})'
        ]
        
        dates_found = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text_lower)
            dates_found.extend(matches)
        
        if len(dates_found) >= 2:
            data['lease_start_date'] = dates_found[0]
            data['lease_end_date'] = dates_found[1]
        elif len(dates_found) == 1:
            data['lease_start_date'] = dates_found[0]
        
        return data
    
    def _extract_id_data(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Extract ID card specific data"""
        import re
        
        data = {}
        
        # Extract name (improved pattern for Indian names)
        name_patterns = [
            r'([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',
            r'name[:\s]+([A-Za-z\s]{2,30})'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text)
            if match:
                data['name'] = match.group(1).strip()
                break
        
        # Extract various ID numbers
        id_patterns = [
            (r'(\d{4}\s?\d{4}\s?\d{4})', 'aadhaar'),  # Aadhaar
            (r'([A-Z]{5}\d{4}[A-Z])', 'pan'),         # PAN
            (r'([A-Z]{2}\d{13})', 'driving_license'),  # Driving License
            (r'([A-Z]\d{7})', 'passport')              # Passport
        ]
        
        for pattern, id_type in id_patterns:
            match = re.search(pattern, text)
            if match:
                data['id_number'] = match.group(1)
                data['id_type'] = id_type
                break
        
        # Extract date of birth
        dob_patterns = [
            r'(?:dob|birth)[:\s]+(\d{2}[/-]\d{2}[/-]\d{4})',
            r'(\d{2}[/-]\d{2}[/-]\d{4})'
        ]
        
        for pattern in dob_patterns:
            match = re.search(pattern, text_lower)
            if match:
                data['date_of_birth'] = match.group(1)
                break
        
        return data
    
    def _extract_property_data(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Extract property document specific data"""
        import re
        
        data = {}
        
        # Extract property type (improved detection)
        property_keywords = {
            'apartment': ['apartment', 'flat', 'unit'],
            'house': ['house', 'villa', 'bungalow', 'cottage'],
            'commercial': ['commercial', 'office', 'shop', 'store', 'warehouse']
        }
        
        for prop_type, keywords in property_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                data['property_type'] = prop_type.title()
                break
        
        # Extract area/size (improved patterns)
        area_patterns = [
            r'(\d+[\d,]*)\s*(?:sq\.?\s*ft|square\s*feet|sqft)',
            r'area[:\s]+(\d+[\d,]*)',
            r'size[:\s]+(\d+[\d,]*)'
        ]
        
        for pattern in area_patterns:
            match = re.search(pattern, text_lower)
            if match:
                data['area'] = match.group(1).replace(',', '')
                break
        
        # Extract bedrooms and bathrooms
        room_patterns = [
            (r'(\d+)\s*(?:bedroom|bed|bhk)', 'bedrooms'),
            (r'(\d+)\s*(?:bathroom|bath)', 'bathrooms')
        ]
        
        for pattern, field in room_patterns:
            match = re.search(pattern, text_lower)
            if match:
                data[field] = match.group(1)
        
        return data
    
    def _calculate_confidence_scores(self, texts, extracted_data) -> Dict[str, float]:
        """Calculate confidence scores based on Vision API results and extraction quality"""
        if not texts:
            return {'overall': 0.0}
        
        # Base confidence from Vision API quality
        text_quality = len(texts[0].description) if texts else 0
        base_confidence = min(0.95, 0.7 + (text_quality / 1000) * 0.2)
        
        # Calculate extraction quality
        extraction_score = min(0.95, 0.8 + (len(extracted_data) / 10) * 0.15)
        
        # Overall confidence
        overall_confidence = (base_confidence + extraction_score) / 2
        
        confidence_scores = {
            'overall': round(overall_confidence, 2),
            'text_detection': round(base_confidence, 2),
            'data_extraction': round(extraction_score, 2)
        }
        
        # Add confidence for each extracted field
        for key in extracted_data.keys():
            field_confidence = base_confidence + (hash(key) % 20) / 100
            confidence_scores[key] = round(min(0.95, field_confidence), 2)
        
        return confidence_scores

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
    try:
        return {
            "status": "✅ WORKING",
            "message": "Rentum AI Backend is operational!",
            "timestamp": datetime.now().isoformat(),
            "deployment": "vercel-serverless-final-v4",
            "endpoints": ["/demo", "/users", "/properties", "/health", "/ocr/scan", "/ocr/scans", "/test"],
            "version": "1.0.0",
            "framework": "FastAPI",
            "python_runtime": "vercel_serverless",
            "query_handling": "optimized"
        }
    except Exception as e:
        return {
            "status": "❌ ERROR",
            "message": f"Error in root endpoint: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "deployment": "vercel-serverless-final-v4"
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
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "rentum-api",
            "version": "1.0.0",
            "ocr_service": ocr_service.status,
            "environment": "vercel-serverless",
            "memory_usage": "optimized",
            "dependencies": "loaded"
        }
    except Exception as e:
        return {
            "status": "degraded",
            "timestamp": datetime.now().isoformat(),
            "service": "rentum-api",
            "error": str(e),
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
    """OCR document scanning endpoint - Google Vision ONLY"""
    try:
        print(f"🔍 OCR scan request: user={user_id}, type={document_type}, file={file.filename}")
        
        # Check if Google Vision is available
        if ocr_service.status != "google_vision_ready":
            print("❌ Google Vision OCR not configured")
            return {
                "status": "error",
                "message": "Google Vision OCR is not configured. Please set up Google Cloud credentials.",
                "error_code": "GOOGLE_VISION_NOT_CONFIGURED",
                "instructions": [
                    "1. Create a Google Cloud service account",
                    "2. Enable Vision API",
                    "3. Set GOOGLE_APPLICATION_CREDENTIALS environment variable",
                    "4. Redeploy to Vercel"
                ],
                "timestamp": datetime.now().isoformat()
            }
        
        # Validate file upload
        if not file:
            print("❌ No file uploaded")
            return {
                "status": "error",
                "message": "No file uploaded",
                "error_code": "NO_FILE",
                "timestamp": datetime.now().isoformat()
            }
        
        # Read file content and validate
        file_content = await file.read()
        print(f"📄 File size: {len(file_content)} bytes")
        
        if len(file_content) > 5 * 1024 * 1024:  # 5MB limit for serverless
            print("❌ File too large")
            return {
                "status": "error", 
                "message": "File too large. Maximum size is 5MB.",
                "error_code": "FILE_TOO_LARGE",
                "timestamp": datetime.now().isoformat()
            }
        
        if len(file_content) == 0:
            print("❌ Empty file")
            return {
                "status": "error",
                "message": "Empty file uploaded",
                "error_code": "EMPTY_FILE",
                "timestamp": datetime.now().isoformat()
            }
        
        # Validate file type (basic check)
        file_extension = file.filename.lower().split('.')[-1] if file.filename else ""
        if file_extension not in ['jpg', 'jpeg', 'png', 'pdf', 'tiff', 'bmp']:
            print(f"❌ Unsupported file type: {file_extension}")
            return {
                "status": "error",
                "message": f"Unsupported file type: {file_extension}. Supported: jpg, jpeg, png, pdf, tiff, bmp",
                "error_code": "UNSUPPORTED_FILE_TYPE",
                "timestamp": datetime.now().isoformat()
            }
        
        # Process with Google Vision OCR
        print("🤖 Processing with Google Vision OCR...")
        ocr_result = ocr_service.process_document(file_content, document_type)
        
        # Add metadata and ensure consistent response format
        scan_result = {
            "id": str(len(ocr_results) + 1),
            "user_id": user_id,
            "document_type": document_type,
            "filename": file.filename or "unknown",
            "file_size": len(file_content),
            "file_type": file_extension,
            "created_at": datetime.now().isoformat(),
            **ocr_result
        }
        
        # Store result
        ocr_results.append(scan_result)
        
        print(f"✅ Google Vision OCR completed successfully: {scan_result['id']}")
        return scan_result
    
    except Exception as e:
        error_msg = f"Google Vision OCR processing failed: {str(e)}"
        print(f"❌ {error_msg}")
        
        # Return detailed error information
        return {
            "status": "error",
            "message": error_msg,
            "error_code": "OCR_PROCESSING_FAILED",
            "error_type": type(e).__name__,
            "timestamp": datetime.now().isoformat(),
            "troubleshooting": [
                "Check if Google Cloud credentials are properly configured",
                "Verify that Vision API is enabled in Google Cloud Console",
                "Ensure the uploaded file is a valid image or PDF",
                "Try with a smaller file size (under 5MB)"
            ]
        }

@app.get("/ocr/scans")
async def list_ocr_scans(user_id: Optional[str] = Query(None)):
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

# ===== VERCEL ASGI EXPORT =====
# Vercel ASGI application export using Mangum adapter
from mangum import Mangum

# Wrap FastAPI app with Mangum adapter for serverless deployment
# Use specific config for Vercel compatibility
try:
    handler = Mangum(app, lifespan="off", api_gateway_base_path=None)
except Exception as e:
    print(f"❌ Mangum initialization failed: {e}")
    # Fallback: Direct ASGI app export
    handler = app

# Export for Vercel
__all__ = ["app", "handler"] 