# 🔄 Rentum AI - Data Flow & Architecture

## 📊 **Where Data Comes From & Where It Goes**

### 🔍 **Data Sources (Input)**

#### 1. **User Registration Forms**
- **From**: React frontend forms (`/register`, `/login`)
- **To**: PostgreSQL database (`users` table)
- **What**: Name, email, phone, role (tenant/landlord/company)

#### 2. **Document Uploads (AI OCR)**
- **From**: File upload in AI Scanner component
- **To**: Backend `/ocr/scan` → **Google Cloud Vision API** → `ocr_scans` table
- **What**: Lease agreements, ID cards, property documents
- **AI Processing**: **Google Cloud Vision** extracts text with 95-99% accuracy, AI analyzes structure

#### 3. **Review Submissions**
- **From**: AIReviews component forms
- **To**: `review_requests` & `review_responses` tables + AI analysis
- **What**: 1-5 ratings, comments, proof files → AI generates scores & flags

#### 4. **Form Data (Payments, Issues, Chat, Documents)**
- **From**: Component forms in React app
- **To**: PostgreSQL tables (`payments`, `issues`, `chat_messages`, `documents`)
- **What**: Payment records, maintenance issues, messages, document uploads

---

## 🗄️ **Data Storage (Database)**

### **Database Choice**: PostgreSQL (via DATABASE_URL)
```
postgresql://postgres:password@localhost:5432/rentum_db
```

### **Fallback**: In-memory storage (if DB fails)
```javascript
// Backend falls back to arrays:
users_db = []
payments_db = []
documents_db = []
// etc...
```

### **Main Tables**:
1. **`users`** - User accounts & profiles
2. **`ocr_scans`** - **Google Vision** AI-extracted document data
3. **`review_requests`** - Review requests between users
4. **`review_responses`** - Reviews with AI analysis
5. **`user_profiles`** - Aggregated AI scores
6. **`payments`** - Payment tracking
7. **`issues`** - Property maintenance issues
8. **`chat_messages`** - User communications
9. **`documents`** - File uploads

---

## 🚀 **Data Flow Diagram**

```
📱 FRONTEND (React)
    ↓ User Input
🌐 API CALLS (HTTP/JSON)
    ↓ FastAPI Routes
🤖 GOOGLE CLOUD VISION API
    ↓ OCR + Analysis
🗄️ POSTGRESQL DATABASE
    ↓ Query Results
📊 FILTERED DATA
    ↓ Role-based
📱 FRONTEND DISPLAY
```

---

## 🔄 **Detailed Data Journey**

### **1. OCR Document Processing**
```
1. User uploads lease document (PropertyDetails component)
2. File sent to `/ocr/scan` endpoint
3. Google Cloud Vision API extracts:
   - Property address
   - Rent amount & deposit
   - Tenant/landlord names
   - Lease start/end dates
   - Terms & conditions
4. Confidence scores calculated (95-99% accuracy)
5. Data stored in `ocr_scans` table
6. Displayed in Property Details component
```

### **2. AI Review System**
```
1. User requests review via AIReviews component
2. Review request stored in `review_requests` table
3. Reviewer submits ratings (1-5 scale)
4. AI analyzes review → generates:
   - Overall score (0-10)
   - Risk assessment (low/medium/high)
   - Green flags (positive behaviors)
   - Red flags (concerning patterns)
5. Results stored in `review_responses` table
6. User profiles updated with aggregated scores
```

### **3. Property Data Pipeline**
```
1. Google Vision extracts property info from lease documents
2. Data processed by AI for accuracy
3. Property details stored with confidence scores
4. Dashboard aggregates property summaries
5. PropertyDetails component displays extracted info
```

---

## 📂 **File Storage**

### **Uploaded Files**: `/backend/uploads/`
- **Documents**: `uploads/documents/`
- **OCR Images**: `uploads/ocr_scans/`
- **Payment Proofs**: `uploads/payment_proofs/`

### **File Naming**: `{ID}_{original_filename}`

---

## 🔐 **Data Security & Privacy**

### **Role-Based Access**:
- **Tenants**: See only their data
- **Landlords**: See their properties + tenant data
- **Company**: See all data for managed properties

### **Data Filtering**:
```javascript
// Backend filters data by user role
if (currentUser.role === 'tenant') {
  // Show only user's own data
} else if (currentUser.role === 'landlord') {
  // Show properties they own + related data
}
```

### **Google Cloud Security**:
- Service account authentication
- Credentials stored securely (not in Git)
- API keys with restricted permissions

---

## 🌐 **API Endpoints**

### **Core Data Endpoints**:
- `GET/POST /users` - User management
- `GET/POST /ocr/scan` - **Google Vision** AI document processing
- `GET/POST /reviews/*` - Review system
- `GET/POST /payments` - Payment tracking
- `GET/POST /issues` - Issue management
- `GET/POST /chat` - Messaging
- `GET/POST /documents` - File uploads

### **Data Response Format**:
```json
{
  "users": [...],
  "ocr_scans": [...],
  "review_responses": [...],
  "payments": [...],
  "issues": [...],
  "chat": [...],
  "documents": [...]
}
```

---

## 🎯 **Current Data Flow Status**

✅ **Working**: 
- User registration/login
- **Google Cloud Vision** OCR document processing
- AI review analysis
- Property details extraction
- Dashboard data aggregation
- Role-based data filtering

✅ **Data Sources**: React forms → FastAPI → PostgreSQL
✅ **Data Display**: Database → API → React components
✅ **AI Processing**: **Google Vision** → Text extraction → Structured data
✅ **File Storage**: Local uploads directory

---

## 🆚 **Google Vision vs Tesseract**

| Feature | Tesseract (OLD) | Google Vision (NEW) |
|---------|-----------------|---------------------|
| **Accuracy** | 70-80% | **95-99%** |
| **Languages** | Manual setup | **Auto-detect** |
| **Speed** | Fast | **Very fast** |
| **Setup** | Complex install | **API key only** |
| **Cost** | Free | **$1.50/1000 requests** |
| **Maintenance** | High | **Low** |

---

**🔍 Data flows from user inputs → Google Vision AI → secure database → filtered display** 📊 