# 🚀 Vercel Deployment Guide - Rentum AI

## 📋 **Prerequisites**

1. ✅ Google Cloud Vision API setup completed
2. ✅ GitHub repository with your code
3. ✅ Vercel account ([vercel.com](https://vercel.com))

---

## 🔑 **Step 1: Get Google Cloud Credentials**

### Get Your Service Account JSON:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **IAM & Admin** → **Service Accounts**
3. Find your service account → **Keys** tab
4. Download your JSON key file
5. **Copy the entire JSON content** (you'll need this for Vercel)

---

## 🌐 **Step 2: Deploy to Vercel**

### Method A: Simple JSON Environment Variable (Recommended)

1. **Connect Repository**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click **"Add New Project"**
   - Import your GitHub repository

2. **Set Environment Variables**:
   - In project settings → **Environment Variables**
   - Add this variable:

   ```bash
   Variable Name: GOOGLE_CREDENTIALS_JSON
   Value: {paste your entire JSON here}
   ```

   **Example**:
   ```json
   {
     "type": "service_account",
     "project_id": "your-project-id",
     "private_key_id": "your-key-id",
     "private_key": "-----BEGIN PRIVATE KEY-----\nYour\nPrivate\nKey\n-----END PRIVATE KEY-----\n",
     "client_email": "your-service@your-project.iam.gserviceaccount.com",
     "client_id": "your-client-id",
     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
     "token_uri": "https://oauth2.googleapis.com/token"
   }
   ```

3. **Deploy**:
   - Click **Deploy**
   - Vercel will automatically build and deploy your app

### Method B: Individual Environment Variables (Alternative)

If you prefer to split the credentials:

```bash
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nYour\nPrivate\nKey\n-----END PRIVATE KEY-----\n
GOOGLE_CLOUD_CLIENT_EMAIL=your-service@your-project.iam.gserviceaccount.com
GOOGLE_CLOUD_CLIENT_ID=your-client-id
```

---

## 📁 **Step 3: Project Structure for Vercel**

Make sure your project structure is:

```
📦 Your Repository
├── 📁 backend/              # FastAPI backend
│   ├── main.py
│   ├── ocr_service.py
│   ├── requirements.txt
│   └── vercel.json         # (we'll create this)
├── 📁 frontend/            # React frontend  
│   ├── src/
│   ├── package.json
│   └── vercel.json         # (we'll create this)
└── 📄 README.md
```

---

## ⚙️ **Step 4: Create Vercel Configuration**

### Backend Vercel Config (`backend/vercel.json`):
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/main.py"
    }
  ],
  "env": {
    "PYTHONPATH": "/var/task"
  }
}
```

### Frontend Vercel Config (`frontend/vercel.json`):
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

---

## 🔄 **Step 5: Update API URLs**

In your React app, update the API URL for production:

### `frontend/src/App.js` (add this at the top):
```javascript
// Update API URL for production
const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-backend-url.vercel.app'  // Replace with your actual backend URL
  : 'http://localhost:8000';

// Use API_URL instead of hardcoded localhost
const response = await fetch(`${API_URL}/ocr/scan`, {
  // your fetch options
});
```

---

## 🧪 **Step 6: Test Deployment**

1. **Deploy Backend First**:
   - Create separate Vercel project for backend
   - Set `GOOGLE_CREDENTIALS_JSON` environment variable
   - Test: `https://your-backend.vercel.app/` should return success

2. **Deploy Frontend**:
   - Create separate Vercel project for frontend
   - Update API_URL to point to your backend
   - Test: Upload a document and verify OCR works

---

## 🛠️ **Troubleshooting**

### Common Issues:

1. **"Google Vision setup failed"**:
   - Check environment variable name: `GOOGLE_CREDENTIALS_JSON`
   - Ensure JSON is valid (use JSON validator)
   - Verify Google Cloud Vision API is enabled

2. **"Module not found"**:
   - Ensure `requirements.txt` includes `google-cloud-vision==3.4.5`
   - Check `vercel.json` configuration

3. **CORS Errors**:
   - Update FastAPI CORS settings to include your frontend domain
   - In `main.py`: Add your Vercel URL to `allow_origins`

### Debug Commands:
```bash
# Test locally with environment variable
export GOOGLE_CREDENTIALS_JSON='{"type":"service_account",...}'
python -c "from ocr_service import ocr_service; print('✅ OCR working!')"
```

---

## 🔒 **Security Notes**

- ✅ Credentials stored securely in Vercel environment variables
- ✅ Never commit `google-credentials.json` to Git
- ✅ Environment variables are encrypted in Vercel
- ✅ Use different service accounts for staging/production

---

## 💰 **Cost Estimation**

- **Vercel**: Free tier (sufficient for demos)
- **Google Vision**: $1.50 per 1,000 OCR requests
- **Storage**: Vercel includes file storage

---

## 🚀 **Final Deployment Commands**

```bash
# 1. Push to GitHub
git add .
git commit -m "Add Google Cloud Vision OCR"
git push origin main

# 2. Deploy on Vercel
# - Go to vercel.com/dashboard
# - Import GitHub repository
# - Add GOOGLE_CREDENTIALS_JSON environment variable
# - Deploy!
```

**Your app will be live at: `https://your-app.vercel.app`** 🎉 