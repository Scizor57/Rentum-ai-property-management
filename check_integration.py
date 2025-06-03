#!/usr/bin/env python3
"""
Rentum AI - Supabase Integration Status Checker
This script checks the current status of your Supabase integration.
"""

import requests
import json
import sys
from datetime import datetime

def check_backend_status():
    """Check if backend is running and connected to database"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "running": True,
                "database_connected": data.get("database") == "connected",
                "db_time": data.get("db_time"),
                "message": data.get("message")
            }
        else:
            return {"running": False, "error": f"HTTP {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"running": False, "error": str(e)}

def check_frontend_status():
    """Check if frontend is accessible"""
    try:
        response = requests.get("http://localhost:3000/", timeout=5)
        return {"running": response.status_code == 200}
    except requests.exceptions.RequestException:
        return {"running": False}

def check_api_endpoints():
    """Test key API endpoints"""
    endpoints = ["/users", "/properties", "/agreements", "/documents", "/payments"]
    results = {}
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            results[endpoint] = {
                "status": response.status_code,
                "working": response.status_code == 200,
                "data_count": len(response.json()) if response.status_code == 200 else 0
            }
        except requests.exceptions.RequestException as e:
            results[endpoint] = {"working": False, "error": str(e)}
    
    return results

def print_status_report():
    """Print comprehensive status report"""
    print("🏠 RENTUM AI - SUPABASE INTEGRATION STATUS")
    print("=" * 50)
    print(f"📅 Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Backend Status
    print("🔧 BACKEND STATUS")
    backend = check_backend_status()
    if backend["running"]:
        print("✅ Backend Server: RUNNING")
        if backend["database_connected"]:
            print("✅ Database: CONNECTED")
            print(f"🕒 DB Time: {backend['db_time']}")
        else:
            print("❌ Database: NOT CONNECTED (using in-memory storage)")
    else:
        print("❌ Backend Server: NOT RUNNING")
        print(f"   Error: {backend.get('error', 'Unknown error')}")
    print()
    
    # Frontend Status
    print("🎨 FRONTEND STATUS")
    frontend = check_frontend_status()
    if frontend["running"]:
        print("✅ Frontend Server: RUNNING")
        print("🌐 Access: http://localhost:3000")
    else:
        print("❌ Frontend Server: NOT RUNNING")
    print()
    
    # API Endpoints
    if backend["running"]:
        print("🔗 API ENDPOINTS STATUS")
        endpoints = check_api_endpoints()
        for endpoint, status in endpoints.items():
            if status["working"]:
                print(f"✅ {endpoint}: Working ({status['data_count']} records)")
            else:
                print(f"❌ {endpoint}: Failed")
        print()
    
    # Integration Summary
    print("📊 INTEGRATION SUMMARY")
    if backend["running"] and backend["database_connected"]:
        print("🎉 Status: FULLY INTEGRATED WITH SUPABASE")
        print("✅ Ready for production deployment")
    elif backend["running"]:
        print("⚠️  Status: PARTIALLY INTEGRATED")
        print("💡 Backend running with in-memory storage")
        print("📝 Action needed: Configure Supabase connection string")
    else:
        print("❌ Status: NOT RUNNING")
        print("📝 Action needed: Start backend server")
    
    print()
    print("📖 For setup instructions, see: SUPABASE_SETUP.md")
    print("🚀 For deployment guide, see: README.md")

if __name__ == "__main__":
    print_status_report() 