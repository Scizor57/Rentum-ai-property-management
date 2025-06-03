from fastapi import FastAPI

# Create the simplest possible FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Simple test app working!", "status": "success"}

@app.get("/test")
def test():
    return {"test": "This is a test endpoint", "vercel": "working"}

# Export for Vercel
handler = app 