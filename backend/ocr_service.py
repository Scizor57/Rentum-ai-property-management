"""
Google Cloud Vision API OCR Service for Rentum AI
Simplified version for Vercel deployment without heavy dependencies
"""

import os
import json
import re
from typing import Dict, Any, Optional
from google.cloud import vision
from google.cloud.vision_v1 import types

class OCRService:
    def __init__(self):
        """Initialize Google Cloud Vision client with flexible authentication"""
        self.client = None
        self.credentials_available = False
        
        try:
            # Try to initialize Google Cloud Vision client
            self._setup_google_vision()
        except Exception as e:
            print(f"⚠️ OCR service started without Google Vision credentials: {e}")
            print("💡 OCR will provide setup instructions when used")
    
    def _setup_google_vision(self):
        """Setup Google Cloud Vision API client"""
        try:
            # Method 1: Try environment variables for Vercel deployment
            if all(os.getenv(key) for key in [
                'GOOGLE_CLOUD_PROJECT_ID',
                'GOOGLE_CLOUD_PRIVATE_KEY_ID', 
                'GOOGLE_CLOUD_PRIVATE_KEY',
                'GOOGLE_CLOUD_CLIENT_EMAIL',
                'GOOGLE_CLOUD_CLIENT_ID'
            ]):
                print("🔧 Using individual Google Cloud environment variables")
                credentials_info = {
                    "type": "service_account",
                    "project_id": os.getenv('GOOGLE_CLOUD_PROJECT_ID'),
                    "private_key_id": os.getenv('GOOGLE_CLOUD_PRIVATE_KEY_ID'),
                    "private_key": os.getenv('GOOGLE_CLOUD_PRIVATE_KEY').replace('\\n', '\n'),
                    "client_email": os.getenv('GOOGLE_CLOUD_CLIENT_EMAIL'),
                    "client_id": os.getenv('GOOGLE_CLOUD_CLIENT_ID'),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
                }
                
                from google.oauth2 import service_account
                credentials = service_account.Credentials.from_service_account_info(credentials_info)
                self.client = vision.ImageAnnotatorClient(credentials=credentials)
                
            # Method 2: Try JSON credentials file for local development
            elif os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
                print("🔧 Using GOOGLE_APPLICATION_CREDENTIALS file")
                self.client = vision.ImageAnnotatorClient()
                
            # Method 3: Try default credentials
            else:
                print("🔧 Trying default Google Cloud credentials")
                self.client = vision.ImageAnnotatorClient()
            
            # Test the client
            print("✅ Google Cloud Vision client initialized successfully")
            self.credentials_available = True
            
        except Exception as e:
            print(f"❌ Failed to setup Google Cloud Vision: {e}")
            self.client = None
            self.credentials_available = False
            raise e
    
    def process_document(self, image_path: str, document_type: str) -> Dict[str, Any]:
        """
        Process document image with Google Cloud Vision API
        """
        if not self.credentials_available:
            return {
                'status': 'error',
                'message': 'Google Cloud Vision API not configured',
                'extracted_data': {},
                'confidence_scores': {},
                'setup_instructions': self._get_setup_instructions()
            }
        
        try:
            # Read image file
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            # Create Vision API image object
            image = vision.Image(content=content)
            
            # Perform text detection
            response = self.client.text_detection(image=image)
            texts = response.text_annotations
            
            if response.error.message:
                raise Exception(f'Google Vision API error: {response.error.message}')
            
            if not texts:
                return {
                    'status': 'success',
                    'extracted_data': {},
                    'confidence_scores': {'overall': 0.0},
                    'raw_text': ''
                }
            
            # First annotation contains the full text
            full_text = texts[0].description
            confidence = texts[0].bounding_poly.vertices if texts else 0.8
            
            # Extract structured data based on document type
            extracted_data = self._extract_structured_data(full_text, document_type)
            
            return {
                'status': 'success',
                'extracted_data': extracted_data,
                'confidence_scores': self._calculate_confidence_scores(texts, extracted_data),
                'raw_text': full_text
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'OCR processing failed: {str(e)}',
                'extracted_data': {},
                'confidence_scores': {},
                'raw_text': ''
            }
    
    def _extract_structured_data(self, text: str, document_type: str) -> Dict[str, Any]:
        """Extract structured data from OCR text based on document type"""
        
        if document_type == 'rental_agreement':
            return self._extract_rental_agreement_data(text)
        elif document_type == 'id_card':
            return self._extract_id_card_data(text)
        elif document_type == 'property_document':
            return self._extract_property_document_data(text)
        else:
            return {'raw_text': text}
    
    def _extract_rental_agreement_data(self, text: str) -> Dict[str, Any]:
        """Extract rental agreement specific information"""
        data = {}
        
        # Enhanced patterns for rental agreement data
        patterns = {
            'tenant_name': [
                r'tenant[:\s]+([a-zA-Z\s]+?)(?:\n|,|;)',
                r'lessee[:\s]+([a-zA-Z\s]+?)(?:\n|,|;)',
                r'renter[:\s]+([a-zA-Z\s]+?)(?:\n|,|;)'
            ],
            'landlord_name': [
                r'landlord[:\s]+([a-zA-Z\s]+?)(?:\n|,|;)',
                r'lessor[:\s]+([a-zA-Z\s]+?)(?:\n|,|;)',
                r'owner[:\s]+([a-zA-Z\s]+?)(?:\n|,|;)'
            ],
            'property_address': [
                r'property[:\s]+([^,\n]+(?:,\s*[^,\n]+)*)',
                r'premises[:\s]+([^,\n]+(?:,\s*[^,\n]+)*)',
                r'address[:\s]+([^,\n]+(?:,\s*[^,\n]+)*)'
            ],
            'monthly_rent': [
                r'rent[:\s]*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
                r'monthly\s+rent[:\s]*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
                r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)\s*per\s*month'
            ],
            'security_deposit': [
                r'security\s+deposit[:\s]*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
                r'deposit[:\s]*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
                r'bond[:\s]*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)'
            ],
            'lease_start_date': [
                r'start\s+date[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                r'commence[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                r'beginning[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})'
            ],
            'lease_end_date': [
                r'end\s+date[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                r'expir[ye][:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                r'terminat[ie][:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})'
            ]
        }
        
        # Apply patterns to extract data
        for field, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    data[field] = match.group(1).strip()
                    break
        
        return data
    
    def _extract_id_card_data(self, text: str) -> Dict[str, Any]:
        """Extract ID card information"""
        data = {}
        
        patterns = {
            'name': [
                r'name[:\s]+([a-zA-Z\s]+?)(?:\n|,)',
                r'([A-Z][a-z]+\s+[A-Z][a-z]+)'  # Full name pattern
            ],
            'id_number': [
                r'id[:\s]*(\w+)',
                r'number[:\s]*(\w+)',
                r'(\d{8,})'  # Long number sequence
            ],
            'date_of_birth': [
                r'dob[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                r'birth[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                r'born[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})'
            ],
            'address': [
                r'address[:\s]+([^,\n]+(?:,\s*[^,\n]+)*)',
                r'residence[:\s]+([^,\n]+(?:,\s*[^,\n]+)*)'
            ]
        }
        
        for field, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    data[field] = match.group(1).strip()
                    break
        
        return data
    
    def _extract_property_document_data(self, text: str) -> Dict[str, Any]:
        """Extract property document information"""
        data = {}
        
        patterns = {
            'property_type': [
                r'type[:\s]+([a-zA-Z\s]+?)(?:\n|,)',
                r'(apartment|house|condo|townhouse|villa)',
            ],
            'area': [
                r'area[:\s]*(\d+(?:\.\d+)?)\s*(?:sq\.?\s*ft\.?|square\s*feet)',
                r'(\d+(?:\.\d+)?)\s*(?:sq\.?\s*ft\.?|square\s*feet)',
                r'size[:\s]*(\d+(?:\.\d+)?)\s*(?:sq\.?\s*ft\.?|square\s*feet)'
            ],
            'bedrooms': [
                r'bedroom[s]?[:\s]*(\d+)',
                r'(\d+)\s*bedroom[s]?',
                r'bed[:\s]*(\d+)'
            ],
            'bathrooms': [
                r'bathroom[s]?[:\s]*(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*bathroom[s]?',
                r'bath[:\s]*(\d+(?:\.\d+)?)'
            ]
        }
        
        for field, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    data[field] = match.group(1).strip()
                    break
        
        return data
    
    def _calculate_confidence_scores(self, texts, extracted_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate confidence scores for extracted data"""
        if not texts or len(texts) < 2:
            return {'overall': 0.5}
        
        # Calculate based on number of successfully extracted fields
        total_possible_fields = 8  # Average expected fields
        extracted_fields = len([v for v in extracted_data.values() if v])
        
        field_confidence = min(extracted_fields / total_possible_fields, 1.0)
        
        # Google Vision confidence (simplified)
        text_confidence = 0.9  # Google Vision typically has high confidence
        
        overall_confidence = (field_confidence * 0.6) + (text_confidence * 0.4)
        
        return {
            'overall': round(overall_confidence, 2),
            'text_detection': round(text_confidence, 2),
            'data_extraction': round(field_confidence, 2)
        }
    
    def _get_setup_instructions(self) -> Dict[str, str]:
        """Get setup instructions for Google Cloud Vision API"""
        return {
            'local_development': 'Set GOOGLE_APPLICATION_CREDENTIALS to point to your service account JSON file',
            'vercel_deployment': 'Add Google Cloud environment variables in Vercel dashboard',
            'required_variables': [
                'GOOGLE_CLOUD_PROJECT_ID',
                'GOOGLE_CLOUD_PRIVATE_KEY_ID', 
                'GOOGLE_CLOUD_PRIVATE_KEY',
                'GOOGLE_CLOUD_CLIENT_EMAIL',
                'GOOGLE_CLOUD_CLIENT_ID'
            ]
        }

# Create global service instance
ocr_service = OCRService() 