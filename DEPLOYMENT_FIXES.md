# 🔧 Backend Deployment Fixes & Demo Users

## ✅ **Issues Fixed:**

### **1. Backend CORS Configuration**
- ✅ **Added Vercel URLs** to CORS allow_origins
- ✅ **Wildcard support** for `*.vercel.app` domains
- ✅ **Temporary wildcard** `*` for testing (should be restricted in production)

### **2. Demo Users & Sample Data**
- ✅ **4 Demo Users** created automatically on startup
- ✅ **Sample Properties** and rental agreements
- ✅ **Works with both database and in-memory** storage
- ✅ **Conflict handling** (won't duplicate existing data)

### **3. Vercel Configuration**
- ✅ **Updated backend/vercel.json** with proper Python settings
- ✅ **Increased timeout** to 30 seconds for OCR processing
- ✅ **Better error handling** and environment configuration

---

## 👥 **Demo Users Available**

### **Tenants:**
- 👤 **Alice Johnson** - `alice.tenant@demo.com` (tenant)
- 👤 **Carol Davis** - `carol.tenant@demo.com` (tenant)

### **Landlords:**
- 🏠 **Bob Smith** - `bob.landlord@demo.com` (landlord)  
- 🏠 **David Wilson** - `david.landlord@demo.com` (landlord)

### **Sample Data Included:**
- 🏡 **2 Properties** (owned by Bob & David)
- 📄 **1 Active Rental Agreement** (Alice renting from Bob)
- 💰 **Sample rent:** $1,500/month, $3,000 deposit

---

## 🌐 **Vercel Deployment Steps**

### **Backend Deployment:**
1. **Create new Vercel project**
2. **Import:** `Scizor57/Rentum-ai-property-management`
3. **Configuration:**
   - **Framework:** Other
   - **Root Directory:** `backend`
   - **Build Command:** (leave empty)
   - **Install Command:** `pip install -r requirements.txt`

4. **Environment Variables:**
   ```
   GOOGLE_CREDENTIALS_JSON = {your Google service account JSON}
   DATABASE_URL = sqlite:///./rentum.db  (optional)
   ```

5. **Deploy!**

### **Frontend Deployment:**
1. **Create another Vercel project**
2. **Import:** Same repository
3. **Configuration:**
   - **Framework:** Create React App
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` ✅ (fixed!)
   - **Install Command:** `npm install`

4. **Environment Variables:**
   ```
   REACT_APP_API_URL = https://your-backend-url.vercel.app
   ```

5. **Deploy!**

---

## 🧪 **Testing Your Deployment**

### **1. Test Backend:**
Visit: `https://your-backend-url.vercel.app/`
- Should show: "Rentum AI backend is running!"

### **2. Test Demo Users:**
Visit: `https://your-backend-url.vercel.app/demo`
- Should show list of available demo users

### **3. Test Frontend:**
Visit: `https://your-frontend-url.vercel.app/`
- Use any demo email to login
- Try uploading a document in AI Scanner
- Check Property Details for extracted data

---

## 🔍 **Quick Demo Flow**

1. **Login** as Alice Johnson (`alice.tenant@demo.com`, role: tenant)
2. **Go to Dashboard** - see property overview
3. **Go to Property Details** - see rental agreement details
4. **Go to AI Scanner** - upload a lease document
5. **Check extraction** - view OCR results and confidence scores
6. **Try AI Reviews** - request/submit reviews

---

## 🎯 **Expected Results**

- ✅ **Frontend loads** without CORS errors
- ✅ **Demo users appear** in login dropdown
- ✅ **Property data shows** in dashboard
- ✅ **Google Vision OCR** works (with credentials)
- ✅ **All API calls succeed** between frontend/backend

---

## 🚨 **If Still Having Issues**

### **Common Problems:**
1. **CORS errors:** Check that backend URL is correctly set in frontend env vars
2. **No demo users:** Check backend logs for startup errors
3. **OCR not working:** Verify Google credentials are set in Vercel env vars
4. **Build failures:** Ensure latest commit is deployed (not old cached version)

### **Debug Steps:**
1. **Check backend logs** in Vercel dashboard
2. **Test API directly:** Visit `/demo` endpoint
3. **Verify environment variables** in Vercel settings
4. **Force redeploy** if using cached build

---

**🚀 Your Rentum AI app is now ready for professional deployment with working demo users!** 🎉 