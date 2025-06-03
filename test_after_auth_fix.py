#!/usr/bin/env python3
"""
Test after disabling Vercel authentication
"""

import requests
import json

def test_after_auth_fix():
    backend_url = "https://rentum-ai-property-management-knip-dpyl1vmij.vercel.app"
    
    print("🔓 Testing After Disabling Vercel Authentication")
    print("=" * 60)
    
    # Test 1: Health check
    try:
        print("\n🏥 Testing health endpoint...")
        response = requests.get(f"{backend_url}/health", timeout=10)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health Response: {json.dumps(health_data, indent=2)}")
            
            ocr_status = health_data.get('ocr_service', 'unknown')
            if ocr_status == 'google_vision_ready':
                print("\n🎉 Google Vision is READY!")
            elif ocr_status == 'google_vision_required':
                print("\n🔧 Google Vision credentials still need fixing")
            else:
                print(f"\n❓ OCR Status: {ocr_status}")
                
        elif response.status_code == 401:
            print("❌ Still getting 401 - authentication is still enabled!")
            return False
        else:
            print(f"❓ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: OCR endpoint 
    try:
        print("\n🤖 Testing OCR endpoint...")
        
        test_content = b"""RENTAL AGREEMENT
        
        Tenant: John Doe
        Landlord: Jane Smith  
        Property: 123 Main Street
        Monthly Rent: $1500
        Security Deposit: $3000
        """
        
        files = {'file': ('rental.txt', test_content, 'text/plain')}
        data = {'user_id': '1', 'document_type': 'rental_agreement'}
        
        response = requests.post(f"{backend_url}/ocr/scan", files=files, data=data, timeout=30)
        print(f"📊 OCR Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📋 OCR Response: {json.dumps(result, indent=2)}")
            
            if result.get('error_code') == 'GOOGLE_VISION_NOT_CONFIGURED':
                print("\n🔧 NEXT STEP: Fix Google Cloud credentials in Vercel!")
                print("The backend is working, but Google Vision needs proper credentials")
                return 'credentials_needed'
                
            elif result.get('status') == 'completed':
                print("\n🎉 SUCCESS: OCR is fully working!")
                return 'success'
                
        elif response.status_code == 401:
            print("❌ Still getting 401 - authentication not disabled yet!")
            return False
            
    except Exception as e:
        print(f"❌ OCR test failed: {e}")
    
    return 'partial'

if __name__ == "__main__":
    result = test_after_auth_fix()
    
    print("\n" + "=" * 60)
    if result == 'success':
        print("🎉 FULLY WORKING: Your OCR is ready!")
    elif result == 'credentials_needed':
        print("🔧 NEXT: Fix Google Cloud credentials format in Vercel")
    elif result == False:
        print("❌ Still blocked - disable Vercel authentication first")
    else:
        print("🔍 Check the output above for next steps") 