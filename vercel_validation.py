#!/usr/bin/env python3
"""
Comprehensive Vercel deployment validation script
Checks all critical aspects for successful deployment
"""

import json
import os
import sys
from pathlib import Path

def check_file_structure():
    """Check required file structure"""
    print("🔍 Checking file structure...")
    
    required_files = [
        "api/index.py",
        "vercel.json", 
        "requirements.txt",
        "runtime.txt"
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print(f"❌ Missing files: {missing}")
        return False
    
    print("✅ All required files present")
    return True

def check_vercel_json():
    """Validate vercel.json configuration"""
    print("🔍 Checking vercel.json...")
    
    try:
        with open("vercel.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        # Check required fields
        if "version" not in config or config["version"] != 2:
            print("❌ vercel.json must have version: 2")
            return False
            
        if "builds" not in config:
            print("❌ vercel.json missing builds section")
            return False
            
        build = config["builds"][0]
        if build["src"] != "api/index.py" or build["use"] != "@vercel/python":
            print("❌ Incorrect build configuration")
            return False
            
        if "routes" not in config:
            print("❌ vercel.json missing routes section")
            return False
            
        print("✅ vercel.json configuration valid")
        return True
        
    except Exception as e:
        print(f"❌ vercel.json error: {e}")
        return False

def check_requirements():
    """Check requirements.txt"""
    print("🔍 Checking requirements.txt...")
    
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        required_deps = ["fastapi", "python-multipart"]
        
        for dep in required_deps:
            if dep not in content:
                print(f"❌ Missing dependency: {dep}")
                return False
        
        print("✅ requirements.txt valid")
        return True
        
    except Exception as e:
        print(f"❌ requirements.txt error: {e}")
        return False

def check_api_structure():
    """Check API structure and imports"""
    print("🔍 Checking API structure...")
    
    try:
        # Import the app
        from api.index import app
        
        # Check it's FastAPI
        if app.__class__.__name__ != "FastAPI":
            print(f"❌ Expected FastAPI app, got {type(app)}")
            return False
        
        # Check routes - all user-defined endpoints
        routes = [route.path for route in app.routes]
        required_routes = ["/", "/demo", "/users", "/properties", "/health", "/test", "/ocr/scan", "/ocr/scans"]
        
        missing_routes = [route for route in required_routes if route not in routes]
        if missing_routes:
            print(f"❌ Missing routes: {missing_routes}")
            return False
        
        print(f"✅ API structure valid ({len(routes)} routes)")
        return True
        
    except Exception as e:
        print(f"❌ API structure error: {e}")
        return False

def check_serverless_compatibility():
    """Check serverless-specific requirements"""
    print("🔍 Checking serverless compatibility...")
    
    try:
        # Check no lifespan events
        with open("api/index.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        if "lifespan=" in content:
            print("❌ Lifespan events not supported in Vercel serverless")
            return False
        
        # Check proper error handling
        if "except Exception" not in content:
            print("❌ Missing proper error handling")
            return False
        
        # Check ASGI app export
        if "app = FastAPI(" not in content:
            print("❌ Missing proper FastAPI app declaration")
            return False
        
        print("✅ Serverless compatibility checks passed")
        return True
        
    except Exception as e:
        print(f"❌ Serverless compatibility error: {e}")
        return False

def main():
    """Run all validation checks"""
    print("🚀 Starting Vercel deployment validation...\n")
    
    checks = [
        ("File Structure", check_file_structure),
        ("Vercel Configuration", check_vercel_json),
        ("Requirements", check_requirements),
        ("API Structure", check_api_structure),
        ("Serverless Compatibility", check_serverless_compatibility)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        if check_func():
            passed += 1
        print("-" * 50)
    
    print(f"\n🎯 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED! Ready for Vercel deployment!")
        return True
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 