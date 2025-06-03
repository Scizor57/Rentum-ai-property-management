# 🔑 Google Cloud Vision API Setup

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Note your **Project ID**

## Step 2: Enable Vision API

1. Go to **APIs & Services** → **Library**
2. Search for "Cloud Vision API"
3. Click **Enable**

## Step 3: Create Service Account

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **Create Service Account**
3. Name: `rentum-ai-ocr`
4. Role: **Cloud Vision AI Service Agent**
5. Click **Create and Continue**
6. Click **Done**

## Step 4: Generate Credentials

1. Click on your service account
2. Go to **Keys** tab
3. Click **Add Key** → **Create New Key**
4. Choose **JSON** format
5. Download the file
6. Rename it to `google-credentials.json`
7. Place it in your backend folder

## Step 5: Set Environment Variable

### Option A: Place file in backend folder
```bash
# Just put google-credentials.json in the backend/ directory
# The app will find it automatically
```

### Option B: Set environment variable
```bash
# Windows PowerShell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\google-credentials.json"

# Windows Command Prompt  
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\google-credentials.json

# Linux/Mac
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/google-credentials.json"
```

## Step 6: Test Setup

```python
from google.cloud import vision
client = vision.ImageAnnotatorClient()
print("✅ Google Cloud Vision setup successful!")
```

## 🚨 Important Security Notes

- **Never commit `google-credentials.json` to Git**
- Add it to `.gitignore`
- For production, use Google Cloud IAM roles instead of service account keys

## 💰 Pricing

- Free tier: 1,000 requests/month
- After free tier: $1.50 per 1,000 requests
- Much more accurate than Tesseract OCR

## 🆚 Google Vision vs Tesseract

| Feature | Tesseract | Google Vision |
|---------|-----------|---------------|
| Accuracy | 70-80% | 95-99% |
| Languages | Manual setup | Auto-detect |
| Speed | Fast | Very fast |
| Cost | Free | $1.50/1000 requests |
| Setup | Complex install | API key only | 