# 🚀 Vercel Deployment Guide for Rentum AI

## Quick Overview
Rentum AI is deployed as two separate Vercel projects:
- **Frontend**: React app (`/frontend` folder)  
- **Backend**: FastAPI app (`/backend` folder)

## 📋 Prerequisites Setup

### 1. Get Your Supabase Database URL
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project (or create new one)
3. Go to **Settings** → **Database**  
4. Copy the **Connection string** (URI format)
5. It looks like: `postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres`

### 2. Get Your Google Cloud Vision API Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create/select project
3. Enable **Vision API**
4. Go to **IAM & Admin** → **Service Accounts**
5. Create service account with Vision API permissions
6. Download JSON key file
7. Copy these values from the JSON:
   - `project_id`
   - `private_key_id`
   - `private_key` (full key including `-----BEGIN PRIVATE KEY-----`)
   - `client_email`
   - `client_id`

## 🔧 Vercel Environment Variables Setup

### Backend Environment Variables
Go to **Vercel Dashboard** → **Your Backend Project** → **Settings** → **Environment Variables**

Add these variables:

| Variable Name | Value | Example |
|---------------|-------|---------|
| `DATABASE_URL` | Your Supabase connection string | `postgresql://postgres:your_password@db.abc123.supabase.co:5432/postgres` |
| `GOOGLE_CLOUD_PROJECT_ID` | Your Google Cloud project ID | `rentum-ai-123456` |
| `GOOGLE_CLOUD_PRIVATE_KEY_ID` | Private key ID from JSON | `a1b2c3d4e5f6...` |
| `GOOGLE_CLOUD_PRIVATE_KEY` | Full private key (with \n) | `-----BEGIN PRIVATE KEY-----\nMII...` |
| `GOOGLE_CLOUD_CLIENT_EMAIL` | Service account email | `vision-api@rentum-ai.iam.gserviceaccount.com` |
| `GOOGLE_CLOUD_CLIENT_ID` | Client ID from JSON | `123456789012345678901` |

### Frontend Environment Variables
Go to **Vercel Dashboard** → **Your Frontend Project** → **Settings** → **Environment Variables**

Add these variables:

| Variable Name | Value | Example |
|---------------|-------|---------|
| `REACT_APP_API_URL` | Your backend Vercel URL | `https://rentum-backend.vercel.app` |

## 🎯 Deployment Steps

### Step 1: Deploy Backend
1. **Create new Vercel project** for backend
2. **Connect to GitHub** repository  
3. **Set Root Directory** to `backend`
4. **Set Build Command** to `pip install -r requirements.txt`
5. **Add all environment variables** (see table above)
6. **Deploy**

### Step 2: Deploy Frontend  
1. **Create new Vercel project** for frontend
2. **Connect to same GitHub** repository
3. **Set Root Directory** to `frontend`
4. **Add environment variables** (see table above)
5. **Deploy**

### Step 3: Update CORS
After both are deployed, update backend CORS in `main.py`:
```python
allow_origins=[
    "https://your-frontend.vercel.app",  # Add your actual frontend URL
    "https://*.vercel.app",
    "*"  # Remove this in production
]
```

## 🔍 Testing Your Deployment

### Test Backend
Visit: `https://your-backend.vercel.app/`
Should see: `{"message": "Rentum AI backend is running!", "database": "connected"}`

Visit: `https://your-backend.vercel.app/demo`
Should see demo users list

### Test Frontend
Visit: `https://your-frontend.vercel.app/`
Should load the Rentum AI app

### Test Full Integration
1. Upload a document through frontend
2. Check if OCR processing works
3. Verify database connections

## 🐛 Troubleshooting

### Backend Issues

**"404: NOT_FOUND"**
- Check that Root Directory is set to `backend`
- Verify `vercel.json` is in backend folder

**Database Connection Failed**
- Verify DATABASE_URL in environment variables
- Check Supabase project is active (not paused)
- Test connection string format

**OCR Not Working**
- Check all Google Cloud environment variables are set
- Verify private key format (should include `\n` characters)
- Test Google Cloud Vision API is enabled

### Frontend Issues

**API Calls Failing**
- Check REACT_APP_API_URL points to backend
- Verify CORS settings in backend
- Check browser network tab for errors

## 📱 Environment Variables Summary

### For Local Development (.env file):
```bash
# Backend .env
DATABASE_URL=postgresql://postgres:your_password@db.your_project.supabase.co:5432/postgres
GOOGLE_APPLICATION_CREDENTIALS=./google-cloud-credentials.json

# Frontend .env  
REACT_APP_API_URL=http://localhost:8000
```

### For Vercel (Dashboard Settings):
- **Backend**: DATABASE_URL + 5 Google Cloud variables
- **Frontend**: REACT_APP_API_URL

## 🎉 Success!
Once deployed, your Rentum AI app will be live with:
- ✅ Supabase database connected
- ✅ Google Cloud Vision OCR working  
- ✅ Full AI review system operational
- ✅ Professional deployment setup

Your app URLs:
- **Frontend**: `https://your-frontend.vercel.app`
- **Backend**: `https://your-backend.vercel.app`

Need help? The backend provides detailed error messages and setup instructions at startup! 