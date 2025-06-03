# 🏠 Rentum AI - Property Management with Google Cloud Vision OCR

## 🚀 SIMPLE STARTUP (2 Commands Only!)

### Terminal 1 - Backend
```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Terminal 2 - Frontend  
```bash
cd frontend
npm start
```

## 🎯 Demo Ready!

1. **Open**: http://localhost:3000
2. **Register**: Create account (tenant/landlord)
3. **Upload**: Go to "AI Scanner" → Upload lease document
4. **View**: Go to "Property Details" → See extracted info!

## 📁 Project Structure
```
📦 Rentum AI
├── 📁 backend/          # FastAPI + Google Vision API
├── 📁 frontend/         # React App
└── 📄 README.md         # This file
```

## 🔍 What It Does

- **Google Cloud Vision OCR**: Upload lease agreements with 95-99% accuracy
- **Auto Property Details**: AI extracts address, rent, dates, etc.
- **Dashboard**: Quick property overview with navigation
- **Modern UI**: Clean interface with dark mode

## 🔑 Setup Google Cloud Vision

### For Local Development:
1. **Get Google Cloud Account**: [console.cloud.google.com](https://console.cloud.google.com)
2. **Enable Vision API**: Search "Cloud Vision API" → Enable
3. **Create Service Account**: IAM → Service Accounts → Create
4. **Download Credentials**: Generate JSON key → Save as `google-credentials.json` in `backend/` folder
5. **Ready!**: The app will auto-detect your credentials

### For Vercel Deployment:
1. **Get your JSON credentials** (same as above)
2. **Copy the entire JSON content**
3. **In Vercel dashboard** → Environment Variables
4. **Add**: `GOOGLE_CREDENTIALS_JSON` = `{your JSON content}`
5. **Deploy!**: Vercel will handle the rest

**See `backend/google_setup.md` for detailed local setup**
**See `VERCEL_SETUP.md` for detailed deployment guide**

## 🌐 **Vercel Deployment**

This app is ready for Vercel deployment with:
- ✅ **Vercel config files** included (`vercel.json`)
- ✅ **Environment variable support** for Google credentials
- ✅ **Separate backend/frontend** deployment
- ✅ **Production-ready** configurations

**Quick Deploy**: Follow `VERCEL_SETUP.md` for step-by-step deployment

---
*Simple. Clean. Demo Ready. Powered by Google AI. Deploy to Vercel!* ✨ 