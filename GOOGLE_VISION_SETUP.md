# 🔧 Google Vision OCR Setup Guide

This app now uses **real Google Vision OCR** instead of demo data. Follow these steps to enable OCR functionality:

## 📋 Prerequisites

1. Google Cloud account
2. Google Cloud project with billing enabled
3. Vision API enabled

## 🚀 Step-by-Step Setup

### 1. Google Cloud Console Setup

1. **Go to Google Cloud Console**: https://console.cloud.google.com
2. **Create/Select Project**: Create a new project or select an existing one
3. **Enable Vision API**: 
   - Go to APIs & Services > Library
   - Search for "Cloud Vision API"
   - Click "Enable"

### 2. Create Service Account

1. **Navigate to IAM & Admin** > Service Accounts
2. **Click "Create Service Account"**
3. **Service Account Details**:
   - Name: `rentum-ocr-service`
   - Description: `OCR service for Rentum AI`
4. **Grant Roles**:
   - Add role: `Cloud Vision API Service Agent`
5. **Click "Done"**

### 3. Generate Service Account Key

1. **Click on the created service account**
2. **Go to "Keys" tab**
3. **Click "Add Key" > "Create new key"**
4. **Select "JSON" format**
5. **Download the JSON file** (keep it secure!)

### 4. Configure Environment Variables

#### For Local Development:
```bash
# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

#### For Vercel Deployment:
1. **Go to Vercel Dashboard** > Your Project > Settings > Environment Variables
2. **Add new environment variable**:
   - **Name**: `GOOGLE_APPLICATION_CREDENTIALS`
   - **Value**: Copy the **entire contents** of your JSON file
3. **Save and redeploy**

### 5. Environment Variable Example

Your JSON file should look like this:
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "rentum-ocr-service@your-project-id.iam.gserviceaccount.com",
  "client_id": "client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/rentum-ocr-service%40your-project-id.iam.gserviceaccount.com"
}
```

## 🔍 What the OCR Can Extract

### 📄 Rental Agreements
- Tenant name
- Landlord name  
- Property address
- Monthly rent amount
- Security deposit
- Lease start/end dates

### 🆔 ID Cards (Aadhaar, PAN, Driving License)
- Full name
- ID number
- Date of birth
- ID type detection

### 🏠 Property Documents
- Property type (apartment, house, commercial)
- Area/size in sq ft
- Number of bedrooms/bathrooms

## ✅ Testing the Setup

1. **Upload a document** through the OCR scanner
2. **Check the response** - it should show:
   - `"mode": "google_vision_ocr"` (not demo_fallback)
   - Real extracted text and data
   - Confidence scores from Vision API

## ❌ Troubleshooting

### "Google Vision OCR is not configured"
- Check if environment variable is set correctly
- Verify JSON file contents are complete
- Redeploy after adding environment variables

### "Google Vision API error"
- Verify Vision API is enabled in Google Cloud
- Check service account has correct permissions
- Ensure billing is enabled on your project

### "No text detected"
- Try with a clearer image
- Ensure text is readable and well-lit
- Supported formats: JPG, PNG, PDF, TIFF, BMP

## 💰 Cost Considerations

Google Vision API pricing (as of 2024):
- First 1,000 requests/month: **FREE**
- Additional requests: ~$1.50 per 1,000 requests
- Perfect for demos and small-scale usage

## 🔐 Security Notes

- **Never commit** service account JSON files to git
- **Use environment variables** for all credentials
- **Restrict service account permissions** to only Vision API
- **Monitor usage** in Google Cloud Console

## 🎯 Ready to Deploy!

Once configured, your OCR will:
- ✅ **Actually scan uploaded documents** 
- ✅ **Extract real text and data**
- ✅ **Parse structured information**
- ✅ **Return Vision API confidence scores**
- ❌ **No more demo/fake data** 