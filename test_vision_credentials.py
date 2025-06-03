#!/usr/bin/env python3
"""
Test script to verify Google Vision credentials locally to help debug the issue.
Run this locally to test your credentials before deploying
"""

import os
import json
from google.cloud import vision

def test_google_vision_credentials():
    print("🔍 Testing Google Vision Credentials...")
    
    # Check if credentials are set
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if creds_path:
        print(f"✅ GOOGLE_APPLICATION_CREDENTIALS found: {creds_path}")
        
        # Try to read the credentials file
        try:
            with open(creds_path, 'r') as f:
                creds_data = json.load(f)
            
            print("✅ Credentials file is valid JSON")
            print(f"📋 Project ID: {creds_data.get('project_id', 'MISSING')}")
            print(f"📋 Client Email: {creds_data.get('client_email', 'MISSING')}")
            print(f"📋 Service Account Type: {creds_data.get('type', 'MISSING')}")
            
            # Check required fields
            required_fields = ['type', 'project_id', 'private_key', 'client_email']
            missing_fields = [field for field in required_fields if not creds_data.get(field)]
            
            if missing_fields:
                print(f"❌ Missing required fields: {missing_fields}")
                return False
            else:
                print("✅ All required credential fields present")
                
        except FileNotFoundError:
            print(f"❌ Credentials file not found: {creds_path}")
            return False
        except json.JSONDecodeError:
            print("❌ Credentials file is not valid JSON")
            return False
    else:
        print("❌ GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
        return False
    
    # Test Vision API connection
    try:
        print("\n🤖 Testing Vision API connection...")
        client = vision.ImageAnnotatorClient()
        print("✅ Vision client created successfully")
        
        # Test with a simple image (create a small test image)
        # Create a simple white image to test
        test_image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDAT\x08\x1dc\xf8\x0f\x00\x00\x01\x00\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        
        image = vision.Image(content=test_image_content)
        response = client.text_detection(image=image)
        
        if response.error.message:
            print(f"❌ Vision API error: {response.error.message}")
            return False
        else:
            print("✅ Vision API connection successful!")
            print(f"📊 Response received (no text expected in test image)")
            return True
            
    except Exception as e:
        print(f"❌ Vision API connection failed: {e}")
        print("\n🔧 Common solutions:")
        print("   1. Enable Vision API in Google Cloud Console")
        print("   2. Check service account has 'Cloud Vision API' role")
        print("   3. Ensure billing is enabled on your Google Cloud project")
        print("   4. Verify service account key is not expired")
        return False

def check_google_cloud_project():
    """Check Google Cloud project settings"""
    print("\n📋 Google Cloud Project Checklist:")
    print("   1. Go to: https://console.cloud.google.com/apis/library/vision.googleapis.com")
    print("   2. Verify 'Cloud Vision API' is ENABLED")
    print("   3. Go to: https://console.cloud.google.com/billing")
    print("   4. Verify billing is ENABLED for your project")
    print("   5. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts")
    print("   6. Verify your service account has 'Cloud Vision API Service Agent' role")

if __name__ == "__main__":
    print("🧪 Google Vision Credentials Test")
    print("=" * 50)
    
    success = test_google_vision_credentials()
    check_google_cloud_project()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SUCCESS: Google Vision is properly configured!")
        print("   Your credentials should work in production.")
    else:
        print("❌ FAILED: Google Vision needs configuration")
        print("   Fix the issues above before deploying.") 