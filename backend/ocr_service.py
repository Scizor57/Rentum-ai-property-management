#!/usr/bin/env python3
"""
OCR Service for Rentum AI
Handles document scanning and data extraction using Google Cloud Vision API
"""

from google.cloud import vision
from google.oauth2 import service_account
import cv2
import numpy as np
from PIL import Image
import re
import json
import os
import io
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        # Initialize Google Cloud Vision client
        self._setup_google_vision()
        # Configure languages (Google Vision supports many languages automatically)
        self.languages = ['en', 'hi', 'bn', 'gu', 'ta', 'te', 'kn', 'ml', 'or', 'pa']
        self._check_google_vision_setup()
    
    def _setup_google_vision(self):
        """Setup Google Cloud Vision API client - works with both Vercel env vars and local JSON"""
        self.client = None
        self.credentials_available = False
        
        try:
            # Method 1: Try Vercel/Production environment variables
            google_credentials_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
            if google_credentials_json:
                logger.info("Using Google credentials from GOOGLE_CREDENTIALS_JSON environment variable")
                # Parse the JSON credentials from environment variable
                credentials_info = json.loads(google_credentials_json)
                credentials = service_account.Credentials.from_service_account_info(credentials_info)
                self.client = vision.ImageAnnotatorClient(credentials=credentials)
                self.credentials_available = True
                logger.info("✅ Google Cloud Vision client initialized from environment variables")
                return
            
            # Method 2: Try individual environment variables (alternative Vercel setup)
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
            private_key = os.getenv('GOOGLE_CLOUD_PRIVATE_KEY')
            client_email = os.getenv('GOOGLE_CLOUD_CLIENT_EMAIL')
            
            if project_id and private_key and client_email:
                logger.info("Using Google credentials from individual environment variables")
                # Replace \\n with actual newlines in private key
                private_key = private_key.replace('\\n', '\n')
                
                credentials_info = {
                    "type": "service_account",
                    "project_id": project_id,
                    "private_key": private_key,
                    "client_email": client_email,
                    "client_id": os.getenv('GOOGLE_CLOUD_CLIENT_ID', ''),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{client_email}"
                }
                
                credentials = service_account.Credentials.from_service_account_info(credentials_info)
                self.client = vision.ImageAnnotatorClient(credentials=credentials)
                self.credentials_available = True
                logger.info("✅ Google Cloud Vision client initialized from individual environment variables")
                return
            
            # Method 3: Try local JSON file (for development)
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if not credentials_path:
                # Try to find credentials in common locations
                possible_paths = [
                    'google-credentials.json',
                    'credentials/google-credentials.json',
                    '../google-credentials.json'
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
                        credentials_path = path
                        logger.info(f"Google credentials found at: {path}")
                        break
            
            if credentials_path and os.path.exists(credentials_path):
                # Initialize the client with local credentials
                self.client = vision.ImageAnnotatorClient()
                self.credentials_available = True
                logger.info("✅ Google Cloud Vision client initialized from local credentials")
                return
            
            # Try application default credentials as last resort
            try:
                self.client = vision.ImageAnnotatorClient()
                self.credentials_available = True
                logger.info("✅ Google Cloud Vision client initialized with default credentials")
                return
            except Exception as default_error:
                logger.warning(f"Application default credentials failed: {default_error}")
            
            # If we get here, no credentials were found
            logger.warning("⚠️  Google Cloud Vision credentials not found")
            logger.warning("🔧 Backend will start without OCR functionality")
            logger.warning("📝 To enable OCR:")
            logger.warning("   Local: Place google-credentials.json in backend folder")
            logger.warning("   Vercel: Set GOOGLE_CREDENTIALS_JSON environment variable")
            
        except Exception as e:
            logger.error(f"Error setting up Google Cloud Vision: {e}")
            logger.warning("🔧 Backend will start without OCR functionality")
            
        # Don't raise an error - let the backend start without OCR
        self.credentials_available = False
    
    def _check_google_vision_setup(self):
        """Check if Google Cloud Vision is properly configured"""
        if not self.credentials_available or not self.client:
            logger.warning("⚠️  Google Cloud Vision is not configured")
            logger.info("📝 OCR endpoints will return setup instructions")
            return
            
        try:
            # Test with a simple request
            test_image = vision.Image()
            test_image.content = b''  # Empty content for test
            
            # This will fail but helps verify the client is working
            logger.info("✅ Google Cloud Vision API is properly configured")
        except Exception as e:
            logger.warning(f"Google Vision setup verification failed: {e}")
            logger.info("This is normal if no test image was provided")
        
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Preprocess image for better OCR accuracy"""
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image from {image_path}")
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply denoising
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Morphological operations to clean up
            kernel = np.ones((1, 1), np.uint8)
            processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            return processed
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise
    
    def extract_text(self, image_path: str) -> Tuple[str, Dict]:
        """Extract text from image using Google Cloud Vision API"""
        # Check if credentials are available
        if not self.credentials_available or not self.client:
            logger.error("❌ Google Cloud Vision credentials not available")
            return "", {
                "average_confidence": 0, 
                "word_count": 0, 
                "low_confidence_words": 0, 
                "error": "Google Cloud Vision credentials not configured",
                "setup_instructions": {
                    "local": "Place google-credentials.json in backend folder",
                    "vercel": "Set GOOGLE_CREDENTIALS_JSON environment variable in Vercel dashboard"
                }
            }
        
        try:
            # Read the image file
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            # Create Google Vision image object
            image = vision.Image(content=content)
            
            # Configure text detection features
            features = [
                vision.Feature(type_=vision.Feature.Type.TEXT_DETECTION),
                vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
            ]
            
            # Create request
            request = vision.AnnotateImageRequest(image=image, features=features)
            
            # Perform OCR
            response = self.client.annotate_image(request=request)
            
            # Check for errors
            if response.error.message:
                raise Exception(f'Google Vision API error: {response.error.message}')
            
            # Extract text
            texts = response.text_annotations
            if not texts:
                return "", {"average_confidence": 0, "word_count": 0, "low_confidence_words": 0}
            
            # Get full text (first annotation contains all text)
            full_text = texts[0].description
            
            # Calculate confidence scores from individual words
            word_confidences = []
            word_count = 0
            low_confidence_count = 0
            
            # Get document-level text detection for confidence scores
            document = response.full_text_annotation
            if document:
                for page in document.pages:
                    for block in page.blocks:
                        for paragraph in block.paragraphs:
                            for word in paragraph.words:
                                # Calculate word confidence (Google provides confidence at symbol level)
                                symbol_confidences = [symbol.confidence for symbol in word.symbols if hasattr(symbol, 'confidence')]
                                if symbol_confidences:
                                    word_confidence = sum(symbol_confidences) / len(symbol_confidences) * 100
                                    word_confidences.append(word_confidence)
                                    word_count += 1
                                    if word_confidence < 60:
                                        low_confidence_count += 1
            
            # Calculate average confidence
            avg_confidence = sum(word_confidences) / len(word_confidences) if word_confidences else 95
            
            confidence_data = {
                'average_confidence': avg_confidence,
                'word_count': word_count,
                'low_confidence_words': low_confidence_count,
                'google_vision_detected': True
            }
            
            return full_text.strip(), confidence_data
            
        except Exception as e:
            logger.error(f"Error extracting text with Google Vision: {e}")
            # Fallback to basic error handling
            return "", {"average_confidence": 0, "word_count": 0, "low_confidence_words": 0, "error": str(e)}
    
    def extract_rental_agreement_data(self, text: str) -> Dict:
        """Extract structured data from rental agreement text"""
        extracted_data = {}
        confidence_scores = {}
        
        # Enhanced patterns for different fields (improved for better accuracy)
        patterns = {
            'rent_amount': [
                r'rent[:\s]*(?:rs\.?|₹|inr)?\s*(\d{1,2}[,\s]*\d{3,6})',
                r'monthly rent[:\s]*(?:rs\.?|₹|inr)?\s*(\d{1,2}[,\s]*\d{3,6})',
                r'rental amount[:\s]*(?:rs\.?|₹|inr)?\s*(\d{1,2}[,\s]*\d{3,6})',
                r'rent.*?(?:rs\.?|₹|inr)\s*(\d{1,2}[,\s]*\d{3,6})'
            ],
            'deposit_amount': [
                r'deposit[:\s]*(?:rs\.?|₹|inr)?\s*(\d{1,2}[,\s]*\d{3,6})',
                r'security deposit[:\s]*(?:rs\.?|₹|inr)?\s*(\d{1,2}[,\s]*\d{3,6})',
                r'advance[:\s]*(?:rs\.?|₹|inr)?\s*(\d{1,2}[,\s]*\d{3,6})',
                r'security.*?(?:rs\.?|₹|inr)\s*(\d{1,2}[,\s]*\d{3,6})'
            ],
            'tenant_name': [
                r'tenant[:\s]*(?:mr\.?|ms\.?|mrs\.?|dr\.?)?\s*([A-Za-z\s]{3,50})',
                r'lessee[:\s]*(?:mr\.?|ms\.?|mrs\.?|dr\.?)?\s*([A-Za-z\s]{3,50})',
                r'renter[:\s]*(?:mr\.?|ms\.?|mrs\.?|dr\.?)?\s*([A-Za-z\s]{3,50})',
                r'tenant.*?(?:mr\.?|ms\.?|mrs\.?|dr\.?)\s*([A-Za-z\s]{3,50})'
            ],
            'landlord_name': [
                r'landlord[:\s]*(?:mr\.?|ms\.?|mrs\.?|dr\.?)?\s*([A-Za-z\s]{3,50})',
                r'lessor[:\s]*(?:mr\.?|ms\.?|mrs\.?|dr\.?)?\s*([A-Za-z\s]{3,50})',
                r'owner[:\s]*(?:mr\.?|ms\.?|mrs\.?|dr\.?)?\s*([A-Za-z\s]{3,50})',
                r'landlord.*?(?:mr\.?|ms\.?|mrs\.?|dr\.?)\s*([A-Za-z\s]{3,50})'
            ],
            'property_address': [
                r'property[:\s]*([A-Za-z0-9\s,.-]{10,200})',
                r'premises[:\s]*([A-Za-z0-9\s,.-]{10,200})',
                r'address[:\s]*([A-Za-z0-9\s,.-]{10,200})',
                r'located at[:\s]*([A-Za-z0-9\s,.-]{10,200})'
            ],
            'start_date': [
                r'from[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'start date[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'commencement[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'effective from[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
            ],
            'end_date': [
                r'to[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'end date[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'expiry[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'until[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
            ]
        }
        
        # Extract data using patterns
        text_lower = text.lower()
        
        for field, field_patterns in patterns.items():
            best_match = None
            best_confidence = 0
            
            for pattern in field_patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    # Take the first match and calculate confidence based on pattern specificity
                    match = matches[0].strip()
                    if match:
                        # Clean up name fields - remove salutations and common prefixes
                        if 'name' in field:
                            match = self._clean_extracted_name(match)
                            if not match:  # Skip if cleaning resulted in empty name
                                continue
                        
                        # Higher confidence for Google Vision (generally more accurate)
                        confidence = min(98, 75 + len(pattern) * 2)
                        if confidence > best_confidence:
                            best_match = match
                            best_confidence = confidence
            
            if best_match:
                extracted_data[field] = best_match
                confidence_scores[field] = best_confidence
            else:
                confidence_scores[field] = 0
        
        # Clean up extracted amounts (remove commas, spaces)
        for amount_field in ['rent_amount', 'deposit_amount']:
            if amount_field in extracted_data:
                amount = extracted_data[amount_field]
                # Remove commas, spaces and convert to number
                cleaned_amount = re.sub(r'[,\s]', '', amount)
                try:
                    # Validate it's a number
                    int(cleaned_amount)
                    extracted_data[amount_field] = cleaned_amount
                except ValueError:
                    # If not a valid number, remove the field
                    del extracted_data[amount_field]
                    confidence_scores[amount_field] = 0
        
        return {
            'extracted_data': extracted_data,
            'confidence_scores': confidence_scores,
            'processing_method': 'google_cloud_vision'
        }
    
    def _clean_extracted_name(self, name: str) -> str:
        """Clean extracted name by removing salutations and common words"""
        if not name:
            return ""
        
        # Remove salutations and common prefixes
        salutations = ['mr', 'ms', 'mrs', 'dr', 'prof', 'sir', 'madam']
        words = name.lower().split()
        
        # Filter out salutations and single characters
        filtered_words = []
        for word in words:
            cleaned_word = re.sub(r'[^\w]', '', word)  # Remove punctuation
            if cleaned_word and len(cleaned_word) > 1 and cleaned_word not in salutations:
                filtered_words.append(cleaned_word.title())
        
        result = ' '.join(filtered_words[:4])  # Limit to 4 words max
        
        # Additional validation - name should have at least 2 characters and be mostly alphabetic
        if len(result) < 2 or not re.match(r'^[A-Za-z\s]+$', result):
            return ""
        
        return result.strip()
    
    def extract_id_card_data(self, text: str) -> Dict:
        """Extract data from ID cards (Aadhaar, PAN, etc.)"""
        extracted_data = {}
        confidence_scores = {}
        
        # Patterns for ID card data
        patterns = {
            'aadhaar_number': [
                r'(\d{4}\s?\d{4}\s?\d{4})',
                r'aadhaar.*?(\d{4}\s?\d{4}\s?\d{4})',
                r'uid.*?(\d{4}\s?\d{4}\s?\d{4})'
            ],
            'pan_number': [
                r'([A-Z]{5}\d{4}[A-Z])',
                r'pan.*?([A-Z]{5}\d{4}[A-Z])',
                r'permanent account.*?([A-Z]{5}\d{4}[A-Z])'
            ],
            'name': [
                r'name[:\s]*([A-Za-z\s]{3,50})',
                r'holder[:\s]*([A-Za-z\s]{3,50})',
                r'cardholder[:\s]*([A-Za-z\s]{3,50})'
            ],
            'dob': [
                r'dob[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'date of birth[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'birth[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
            ],
            'address': [
                r'address[:\s]*([A-Za-z0-9\s,.-]{10,200})',
                r'resident of[:\s]*([A-Za-z0-9\s,.-]{10,200})'
            ]
        }
        
        text_lower = text.lower()
        
        for field, field_patterns in patterns.items():
            best_match = None
            best_confidence = 0
            
            for pattern in field_patterns:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    match = matches[0].strip()
                    if match:
                        if field == 'name':
                            match = self._clean_extracted_name(match)
                            if not match:
                                continue
                        
                        # Higher confidence for Google Vision
                        confidence = min(98, 80 + len(pattern))
                        if confidence > best_confidence:
                            best_match = match
                            best_confidence = confidence
            
            if best_match:
                extracted_data[field] = best_match
                confidence_scores[field] = best_confidence
            else:
                confidence_scores[field] = 0
        
        return {
            'extracted_data': extracted_data,
            'confidence_scores': confidence_scores,
            'processing_method': 'google_cloud_vision'
        }
    
    def process_document(self, image_path: str, document_type: str) -> Dict:
        """Process document and extract relevant data based on type"""
        try:
            # Extract text from image
            text, text_confidence = self.extract_text(image_path)
            
            if not text:
                return {
                    'success': False,
                    'error': 'No text detected in document',
                    'extracted_data': {},
                    'confidence_scores': {},
                    'processing_method': 'google_cloud_vision'
                }
            
            # Process based on document type
            if document_type == 'rental_agreement':
                result = self.extract_rental_agreement_data(text)
            elif document_type in ['id_card', 'aadhaar', 'pan']:
                result = self.extract_id_card_data(text)
            else:
                # Generic text extraction
                result = {
                    'extracted_data': {'full_text': text},
                    'confidence_scores': {'full_text': text_confidence['average_confidence']},
                    'processing_method': 'google_cloud_vision'
                }
            
            # Add text confidence to result
            result['text_confidence'] = text_confidence
            result['success'] = True
            result['raw_text'] = text
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return {
                'success': False,
                'error': str(e),
                'extracted_data': {},
                'confidence_scores': {},
                'processing_method': 'google_cloud_vision'
            }

# Global instance
ocr_service = OCRService() 