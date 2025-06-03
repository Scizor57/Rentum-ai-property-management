#!/usr/bin/env python3
"""
Simple test for OCR endpoint to get specific Google Vision error
"""

import requests
import json

def test_ocr_only():
    backend_url = "https://rentum-ai-property-management-knip-dpyl1vmij.vercel.app"
    
    print(f"🤖 Testing OCR endpoint: {backend_url}/ocr/scan")
    print("=" * 60)
    
    # Create test file content
    test_content = b"""RENTAL AGREEMENT
    
    Tenant: John Doe
    Landlord: Jane Smith
    Property Address: 123 Main Street, City, State
    Monthly Rent: $1500
    Security Deposit: $3000
    Lease Start Date: 01/01/2024
    Lease End Date: 12/31/2024
    """
    
    # Prepare the request
    files = {
        'file': ('rental_agreement.txt', test_content, 'text/plain')
    }
    data = {
        'user_id': '1',
        'document_type': 'rental_agreement'
    }
    
    try:
        print("📤 Sending OCR request...")
        response = requests.post(f"{backend_url}/ocr/scan", files=files, data=data, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        try:
            result = response.json()
            print(f"📋 Response JSON:")
            print(json.dumps(result, indent=2))
            
            # Analyze the response
            if result.get('error_code') == 'GOOGLE_VISION_NOT_CONFIGURED':
                print("\n🔧 CONFIRMED: Google Vision is not configured!")
                print("💡 This means your GOOGLE_APPLICATION_CREDENTIALS needs fixing")
                
            elif result.get('status') == 'completed':
                print("\n🎉 SUCCESS: OCR is working!")
                print(f"🤖 Processing mode: {result.get('mode', 'unknown')}")
                
            elif 'error' in result.get('status', '').lower():
                print(f"\n❌ OCR Error: {result.get('message', 'Unknown error')}")
                
        except json.JSONDecodeError:
            print(f"📄 Raw Response Text: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - function might be cold starting")
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("🧪 Simple OCR Test")
    print("=" * 40)
    test_ocr_only()
    print("\n" + "=" * 40)
    print("💡 Next: Fix Google Cloud credentials if you see 'GOOGLE_VISION_NOT_CONFIGURED'") 