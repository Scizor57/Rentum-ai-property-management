#!/usr/bin/env python3
"""
Simple test to verify API structure for Vercel deployment
"""

def test_api_structure():
    """Test that the API can be imported and has the right structure"""
    try:
        # Import the API - only need 'app' for ASGI applications
        from api.index import app
        
        print("✅ Successfully imported FastAPI app")
        print(f"✅ App type: {type(app)}")
        
        # Check if app has routes
        routes = [route.path for route in app.routes]
        print(f"✅ Found {len(routes)} routes: {routes}")
        
        # Test that required routes exist - all user-defined endpoints
        required_routes = ["/", "/demo", "/users", "/properties", "/health", "/test", "/ocr/scan", "/ocr/scans"]
        missing_routes = [route for route in required_routes if route not in routes]
        
        if missing_routes:
            print(f"❌ Missing routes: {missing_routes}")
            return False
        else:
            print("✅ All required routes present")
            return True
            
    except Exception as e:
        print(f"❌ Error importing API: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing API structure for Vercel deployment...")
    success = test_api_structure()
    print(f"\n{'✅ API structure test PASSED' if success else '❌ API structure test FAILED'}") 