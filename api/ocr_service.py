"""
Simplified OCR Service for Vercel deployment
No external dependencies, just demo functionality
"""

import re
from typing import Dict, Any
from datetime import datetime

class OCRService:
    def __init__(self):
        """Initialize simplified OCR service"""
        self.status = "demo_mode"
    
    def process_document(self, file_content: bytes, document_type: str) -> Dict[str, Any]:
        """
        Process document - returns demo data for Vercel deployment
        """
        # For demo purposes, return realistic mock data
        return {
            'status': 'success',
            'extracted_data': self._get_demo_data(document_type),
            'confidence_scores': {
                'overall': 0.95,
                'text_detection': 0.98,
                'data_extraction': 0.92
            },
            'processing_time': datetime.now().isoformat(),
            'mode': 'demo'
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

# Create service instance
ocr_service = OCRService() 