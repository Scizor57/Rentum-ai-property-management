# 🚀 Fresh Google Cloud Vision API Setup Guide

## ✅ Step 1: Create New Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Sign in with your Google account
3. Click the project dropdown at the top
4. Click **"New Project"**
5. Fill out:
   - **Project Name**: `rentum-ocr-vision` (or your choice)
   - **Project ID**: Accept auto-generated or customize  
   - **Location**: Select organization or "No organization"
6. Click **"Create"**

## ✅ Step 2: Enable Vision API

1. Go to **APIs & Services** → **Library**
2. Search for: `Cloud Vision API`
3. Click on **"Cloud Vision API"**
4. Click **"Enable"**

## ✅ Step 3: Create Service Account

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **"Create Service Account"**
3. Fill out:
   - **Service account name**: `rentum-vision-ocr`
   - **Description**: `Service account for Rentum OCR functionality`
4. Click **"Create and Continue"**
5. **Grant role**: `Cloud Vision API Service Agent`
6. Click **"Continue"** → **"Done"**

## ✅ Step 4: Generate JSON Key

1. **Click** on the service account you just created
2. Go to **"Keys"** tab
3. Click **"Add Key"** → **"Create new key"**
4. Choose **"JSON"** format
5. Click **"Create"** - downloads the JSON file automatically
6. **Save this file safely** - you'll need it for Vercel

## ✅ Step 5: Configure in Vercel

### Method 1: Copy-Paste JSON Content

1. **Open** the downloaded JSON file in a text editor
2. **Copy the entire JSON content** (everything including `{` and `}`)
3. Go to your **Vercel project dashboard**
4. Click **"Settings"** → **"Environment Variables"**
5. Click **"Add New"**:
   - **Name**: `GOOGLE_APPLICATION_CREDENTIALS`
   - **Value**: **Paste the entire JSON content here**
   - **Environments**: Select all (Production, Preview, Development)
6. Click **"Save"**

### Method 2: Base64 Encode (Alternative)

If copy-paste doesn't work:

1. **Encode the JSON file** to base64:
   ```bash
   # On Windows PowerShell:
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("path\to\your\service-account.json"))
   
   # On Mac/Linux:
   base64 -i path/to/your/service-account.json
   ```

2. In Vercel Environment Variables:
   - **Name**: `GOOGLE_APPLICATION_CREDENTIALS_BASE64`
   - **Value**: The base64 string
   - Update your backend code to decode this

## ✅ Step 6: Test the Setup

After setting up in Vercel:

1. **Redeploy** your Vercel project (or wait for auto-deployment)
2. **Run the test script**:
   ```bash
   python test_after_auth_fix.py
   ```
3. **Look for**:
   - ✅ `"ocr_service": "google_vision_ready"` = SUCCESS!
   - ❌ `"ocr_service": "google_vision_required"` = Still needs fixing

## 🔧 Troubleshooting

### If you still get "google_vision_required":

1. **Check JSON format**: Ensure the JSON is valid (no extra quotes/escaping)
2. **Verify permissions**: Service account should have `Cloud Vision API Service Agent` role
3. **Wait 2-3 minutes**: Changes can take time to propagate
4. **Check Vercel logs**: Go to Deployments → View Function Logs for errors

### Common JSON Issues:

❌ **Don't do this** (extra quotes):
```
"{"type": "service_account", ...}"
```

✅ **Do this** (direct JSON):
```
{"type": "service_account", ...}
```

## 🎯 Expected Success Result

When working correctly, you should see:

```json
{
  "status": "healthy",
  "ocr_service": "google_vision_ready",
  "service": "rentum-api"
}
```

And OCR requests will return:

```json
{
  "status": "completed",
  "mode": "google_vision_ocr",
  "extracted_data": { ... }
}
```

## 📞 Next Steps

Once you see `"google_vision_ready"`, your OCR is fully working! Test it with:

1. Upload a rental agreement document
2. Check that extracted data contains tenant names, rent amounts, etc.
3. Verify confidence scores are included

🎉 **Success!** Your demo-free, real Google Vision OCR is ready! 