# 🚀 Supabase Integration Guide for Rentum AI

## ✅ Current Status
Your Rentum AI application is **already partially integrated** with Supabase! The backend code includes:
- ✅ Database connection pooling with AsyncPG
- ✅ Graceful fallback to in-memory storage
- ✅ Complete database schema ready for deployment
- ✅ All CRUD operations for all features

## 🎯 Quick Setup (5 minutes)

### Step 1: Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and sign up/login
2. Click **"New Project"**
3. Choose organization and enter:
   - **Name**: `rentum-ai`
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Choose closest to your location
4. Click **"Create new project"** (takes 2-3 minutes)

### Step 2: Set Up Database Schema
1. In Supabase dashboard → **SQL Editor**
2. Copy the entire content from `backend/schema.sql`
3. Paste and click **"Run"**
4. Verify tables in **Table Editor** (should see 9 tables with sample data)

### Step 3: Get Connection String
1. Supabase dashboard → **Settings** → **Database**
2. Copy the **Connection pooling** string:
   ```
   postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres
   ```
3. Replace `[password]` with your actual database password

### Step 4: Update Environment Variables
1. Copy `backend/env_template.txt` to `backend/.env`
2. Update the `DATABASE_URL` with your Supabase connection string:
   ```env
   DATABASE_URL=postgresql://postgres.abcdefghijklmnop:your_password@aws-0-us-west-1.pooler.supabase.com:5432/postgres
   ```

### Step 5: Test Integration
1. Restart backend: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
2. Test: `curl http://localhost:8000/`
3. Look for: `"database":"connected"` and `"db_time"` in response

## 🏗️ Database Schema Overview

Your database includes these tables:
- **users** - User profiles (landlords, tenants, companies)
- **properties** - Property listings and details
- **agreements** - Rental agreements and contracts
- **documents** - Document vault (Aadhaar, PAN, etc.)
- **payments** - Payment tracking and history
- **recommendations** - User reviews and ratings
- **issues** - Property issue tracking
- **notifications** - SMS/email/push notifications
- **chat_messages** - In-app messaging system

## 🔧 Backend Features Already Implemented

### Database Operations
- ✅ Connection pooling with graceful fallback
- ✅ Automatic retry on connection failure
- ✅ Real-time database status reporting
- ✅ Sample data for testing

### API Endpoints
- ✅ `/users` - User management
- ✅ `/properties` - Property management
- ✅ `/agreements` - Rental agreements
- ✅ `/documents` - Document vault
- ✅ `/payments` - Payment tracking
- ✅ `/recommendations` - Reviews system
- ✅ `/issues` - Issue management
- ✅ `/notifications` - Notification system
- ✅ `/chat` - Messaging system

### Security & Performance
- ✅ CORS middleware configured
- ✅ Input validation with Pydantic
- ✅ Database indexes for performance
- ✅ Foreign key constraints
- ✅ Error handling and logging

## 🎨 Frontend Features

### Modern UI
- ✅ Sky blue gradient design
- ✅ Responsive card-based layout
- ✅ Tabbed navigation for all features
- ✅ Dark/light mode toggle
- ✅ Smooth animations and hover effects

### Functionality
- ✅ Real-time data fetching from backend
- ✅ Form validation and submission
- ✅ Dynamic status indicators
- ✅ Comprehensive feature coverage

## 🚀 Production Deployment

### Backend Deployment Options
1. **Railway** (Recommended)
   - Connect GitHub repo
   - Set `DATABASE_URL` environment variable
   - Auto-deploy on push

2. **Heroku**
   - `heroku create rentum-ai-backend`
   - `heroku config:set DATABASE_URL=your_supabase_url`
   - `git push heroku main`

3. **Vercel**
   - Connect GitHub repo
   - Add environment variables
   - Deploy with one click

### Frontend Deployment Options
1. **Vercel** (Recommended)
   - Connect GitHub repo
   - Update API_BASE to production URL
   - Auto-deploy on push

2. **Netlify**
   - Drag and drop build folder
   - Configure redirects for SPA

## 🔒 Security Considerations

### For Production
1. **Enable Row Level Security (RLS)** in Supabase
2. **Rotate database passwords** regularly
3. **Use environment variables** for all secrets
4. **Enable HTTPS** for all endpoints
5. **Implement JWT authentication**

### Sample RLS Policies
```sql
-- Users can only see their own data
CREATE POLICY "Users can view own data" ON users
FOR SELECT USING (auth.uid()::text = id);

-- Landlords can manage their properties
CREATE POLICY "Landlords manage properties" ON properties
FOR ALL USING (auth.uid()::text = owner_id);
```

## 🐛 Troubleshooting

### Common Issues
1. **"Failed to fetch"** → Check CORS settings and backend URL
2. **"Connection refused"** → Verify Supabase connection string
3. **"Table does not exist"** → Re-run schema.sql in Supabase
4. **"Module not found"** → Activate virtual environment and install dependencies

### Debug Commands
```bash
# Test backend connection
curl http://localhost:8000/

# Check database status
curl http://localhost:8000/ | grep database

# View backend logs
uvicorn main:app --reload --log-level debug
```

## 📊 Sample Data Included

The schema includes test data:
- 3 users (landlord, tenant, company)
- 3 properties (Mumbai, Delhi, Bangalore)
- Relationships and sample transactions

## 🎉 Next Steps

1. **Complete Supabase setup** using steps above
2. **Test all features** in the frontend
3. **Customize sample data** as needed
4. **Deploy to production** when ready
5. **Enable authentication** for security

---

**Your Rentum AI application is ready for Supabase integration!** 🚀 