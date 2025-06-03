#!/usr/bin/env python3
"""
Test backend with browser-like headers to check for CORS or user-agent issues
"""

import requests

def test_with_browser_headers():
    backend_url = "https://rentum-ai-property-management-knip-dpyl1vmij.vercel.app"
    
    # Browser-like headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    endpoints = ["/", "/health", "/demo"]
    
    for endpoint in endpoints:
        url = f"{backend_url}{endpoint}"
        print(f"\n🌐 Testing: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ Success! Data: {data}")
                except:
                    print(f"   ✅ Success! Response: {response.text[:200]}...")
            else:
                print(f"   ❌ Response: {response.text[:200]}...")
                
        except requests.exceptions.Timeout:
            print("   ⏰ Timeout - function might be cold starting")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_function_warmup():
    """Test if functions need warm-up"""
    backend_url = "https://rentum-ai-property-management-knip-dpyl1vmij.vercel.app"
    
    print("\n🔥 Testing function warm-up...")
    
    for i in range(3):
        try:
            print(f"   Attempt {i+1}...")
            response = requests.get(f"{backend_url}/", timeout=30)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Function is warm!")
                break
            elif response.status_code in [401, 403]:
                print("   ⚠️ Unauthorized - but function is responding")
                break
        except requests.exceptions.Timeout:
            print("   ⏰ Still warming up...")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Browser-like Backend Test")
    print("=" * 50)
    
    test_function_warmup()
    test_with_browser_headers()
    
    print("\n" + "=" * 50)
    print("💡 If still getting 401, check Vercel Function logs for the actual error") 