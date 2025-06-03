#!/usr/bin/env python3
"""
Test Vercel fixes for routing and Google Vision credentials
"""

import requests
import json
import time

def test_vercel_fixes():
    backend_url = "https://rentum-ai-property-management-knip-dpyl1vmij.vercel.app"
    
    print("🔧 Testing Vercel Fixes")
    print("=" * 60)
    
    # Wait for potential redeployment
    print("⏳ Waiting 30 seconds for Vercel to redeploy...")
    time.sleep(30)
    
    # Test 1: Basic endpoint routing
    print("\n🌐 Test 1: Check if routing is fixed...")
    try:
        response = requests.get(f"{backend_url}/", timeout=15)
        print(f"📊 Root Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint working!")
            print(f"🏷️ Deployment: {data.get('deployment', 'unknown')}")
            print(f"🐍 Framework: {data.get('framework', 'unknown')}")
        elif response.status_code == 404:
            print("❌ Still getting 404 - routing not fixed yet")
            return False
        else:
            print(f"❓ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False
    
    # Test 2: Health endpoint with detailed debugging
    print("\n🏥 Test 2: Health endpoint with Google Vision debugging...")
    try:
        response = requests.get(f"{backend_url}/health", timeout=15)
        print(f"📊 Health Status: {response.status_code}")
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health Response:")
            print(json.dumps(health_data, indent=2))
            
            ocr_status = health_data.get('ocr_service', 'unknown')
            if ocr_status == 'google_vision_ready':
                print("\n🎉 SUCCESS: Google Vision is ready!")
                return 'ready'
            elif ocr_status == 'google_vision_required':
                print("\n🔧 Google Vision still needs credentials")
                return 'needs_creds'
            else:
                print(f"\n❓ OCR Status: {ocr_status}")
                return 'unknown'
                
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 3: Check Vercel function logs for debugging info
    print("\n📋 Test 3: Check OCR endpoint for detailed debugging...")
    try:
        test_content = b"Test rental agreement"
        files = {'file': ('test.txt', test_content, 'text/plain')}
        data = {'user_id': '1', 'document_type': 'rental_agreement'}
        
        response = requests.post(f"{backend_url}/ocr/scan", files=files, data=data, timeout=30)
        print(f"📊 OCR Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📋 OCR Response:")
            print(json.dumps(result, indent=2))
            
            if result.get('status') == 'completed':
                print("\n🎉 FULL SUCCESS: OCR is working!")
                return 'working'
            elif result.get('error_code') == 'GOOGLE_VISION_NOT_CONFIGURED':
                print("\n🔧 Need to check Vercel logs for credential debugging info")
                return 'check_logs'
                
        elif response.status_code == 404:
            print("❌ Still getting 404 - function routing not working")
            return False
            
    except Exception as e:
        print(f"❌ OCR test failed: {e}")
    
    return 'partial'

def show_next_steps(result):
    print("\n" + "=" * 60)
    
    if result == 'working':
        print("🎉 EVERYTHING IS WORKING!")
        print("✅ Vercel routing: Fixed")
        print("✅ Google Vision: Ready")
        print("✅ OCR endpoint: Functional")
        
    elif result == 'ready':
        print("🎯 VERCEL ROUTING FIXED!")
        print("✅ Backend is accessible")
        print("✅ Google Vision credentials are working")
        print("💡 Test the OCR functionality in your frontend")
        
    elif result == 'needs_creds':
        print("🔧 ROUTING FIXED, CREDENTIALS NEEDED")
        print("✅ Vercel function is working")
        print("❌ Google Vision credentials still need fixing")
        print("\n📋 Next steps:")
        print("1. Go to Vercel project → Settings → Environment Variables")
        print("2. Check if GOOGLE_APPLICATION_CREDENTIALS is properly set")
        print("3. Go to Deployments → View Function Logs to see debugging info")
        
    elif result == 'check_logs':
        print("🔍 CHECK VERCEL LOGS FOR DEBUGGING INFO")
        print("✅ Backend is responding")
        print("❌ Google Vision credentials need investigation")
        print("\n📋 How to check logs:")
        print("1. Go to Vercel dashboard → Your project")
        print("2. Click 'Deployments' tab")
        print("3. Click latest deployment → 'View Function Logs'")
        print("4. Look for credential debugging messages starting with 📋")
        
    elif result == False:
        print("❌ STILL HAVING ISSUES")
        print("The routing fix may not have deployed yet")
        print("\n📋 Try:")
        print("1. Wait 5 more minutes for Vercel to redeploy")
        print("2. Manually trigger redeployment in Vercel dashboard")
        print("3. Run this test again")
        
    else:
        print("❓ PARTIAL SUCCESS")
        print("Some things are working, check the output above")

if __name__ == "__main__":
    result = test_vercel_fixes()
    show_next_steps(result) 