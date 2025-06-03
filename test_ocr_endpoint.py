#!/usr/bin/env python3
"""
Test the OCR endpoint directly to see what error it returns
"""

import requests
import json

def test_ocr_endpoint():
    # The working backend URL
    backend_url = "https://rentum-ai-property-management-knip-dpyl1vmij.vercel.app"
    
    print(f"🔍 Testing Working Backend: {backend_url}")
    print("=" * 80)
    
    # Test 1: Check health endpoint 
    try:
        print("\n🏥 Testing health endpoint...")
        response = requests.get(f"{backend_url}/health")
        health_data = response.json()
        print(f"✅ Health check: {response.status_code}")
        print(f"📊 OCR Service Status: {health_data.get('ocr_service', 'UNKNOWN')}")
        print(f"📄 Full health response: {json.dumps(health_data, indent=2)}")
        
        if health_data.get('ocr_service') == 'google_vision_required':
            print("\n🔧 DIAGNOSIS: Google Vision credentials are not working!")
            print("✅ Backend is healthy but Google Cloud credentials need fixing")
        elif health_data.get('ocr_service') == 'google_vision_ready':
            print("\n🎉 Google Vision is properly configured!")
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return None
    
    # Test 2: Try OCR endpoint to get the specific error
    try:
        print("\n🤖 Testing OCR endpoint for specific error...")
        
        # Create a simple test file
        test_file_content = b"Test rental agreement\nTenant: John Doe\nLandlord: Jane Smith\nRent: $1500"
        files = {
            'file': ('test_rental.txt', test_file_content, 'text/plain')
        }
        data = {
            'user_id': '1',
            'document_type': 'rental_agreement'
        }
        
        response = requests.post(f"{backend_url}/ocr/scan", files=files, data=data)
        result = response.json()
        
        print(f"📊 OCR Response Status: {response.status_code}")
        print(f"📄 OCR Response: {json.dumps(result, indent=2)}")
        
        if result.get('error_code') == 'GOOGLE_VISION_NOT_CONFIGURED':
            print("\n🔧 DIAGNOSIS: Google Vision credentials issue confirmed!")
            print("The exact error message from backend:")
            print(f"   {result.get('message', 'No message')}")
            
            if 'instructions' in result:
                print("\nBackend provided instructions:")
                for i, instruction in enumerate(result['instructions'], 1):
                    print(f"   {i}. {instruction}")
                    
        elif result.get('status') == 'completed':
            print("\n🎉 SUCCESS: Google Vision is working!")
            print(f"Mode: {result.get('mode', 'unknown')}")
        else:
            print(f"\n❓ Unexpected response: {result}")
            
    except Exception as e:
        print(f"❌ OCR endpoint test failed: {e}")
    
    return backend_url

def check_vercel_environment():
    print("\n📋 Vercel Environment Check:")
    print("1. Go to your Vercel backend project dashboard")
    print("2. Click 'Settings' → 'Environment Variables'")
    print("3. Verify 'GOOGLE_APPLICATION_CREDENTIALS' is set")
    print("4. Click 'Deployments' → Click latest deployment → 'View Function Logs'")
    print("5. Look for any error messages during startup")

if __name__ == "__main__":
    print("🧪 OCR Endpoint Test")
    print("=" * 50)
    
    test_ocr_endpoint()
    check_vercel_environment()
    
    print("\n" + "=" * 50)
    print("💡 TIP: If you see 'GOOGLE_VISION_NOT_CONFIGURED', the issue is with your credentials format in Vercel.") 