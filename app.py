from backend.main import app

# This is the entry point for Vercel deployment
# It imports the FastAPI app from backend/main.py

# Export the app for Vercel
handler = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True) 