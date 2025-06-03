from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase database URL format: postgresql://postgres:[password]@[host]:5432/postgres
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/rentum_db")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for testing (fallback if DB fails)
users_db = []
properties_db = []
agreements_db = []
documents_db = []
payments_db = []
recommendations_db = []
issues_db = []
notifications_db = []
chat_db = []

# Counter for generating IDs
id_counter = 1

def get_next_id():
    global id_counter
    current_id = str(id_counter)
    id_counter += 1
    return current_id

class UserCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    profile_photo: Optional[str] = None
    role: str

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str]
    profile_photo: Optional[str]
    role: str
    created_at: str

class PropertyCreate(BaseModel):
    owner_id: str
    address: str
    details: Optional[dict] = None
    status: Optional[str] = 'active'

class PropertyOut(BaseModel):
    id: str
    owner_id: str
    address: str
    details: Optional[dict]
    status: str
    created_at: str

class AgreementCreate(BaseModel):
    property_id: str
    landlord_id: str
    tenant_id: str
    start_date: str
    end_date: str
    rent: float
    deposit: float
    clauses: Optional[dict] = None
    document_url: Optional[str] = None

class AgreementOut(BaseModel):
    id: str
    property_id: str
    landlord_id: str
    tenant_id: str
    start_date: str
    end_date: str
    rent: float
    deposit: float
    clauses: Optional[dict]
    document_url: Optional[str]
    status: str
    created_at: str

class DocumentCreate(BaseModel):
    user_id: str
    property_id: Optional[str] = None
    doc_type: str
    url: str

class DocumentOut(BaseModel):
    id: str
    user_id: str
    property_id: Optional[str]
    doc_type: str
    url: str
    uploaded_at: str

class PaymentCreate(BaseModel):
    user_id: str
    property_id: str
    amount: float
    payment_type: str  # e.g., rent, deposit, wallet_topup
    proof_url: Optional[str] = None

class PaymentOut(BaseModel):
    id: str
    user_id: str
    property_id: str
    amount: float
    payment_type: str
    proof_url: Optional[str]
    status: str
    created_at: str

class RecommendationCreate(BaseModel):
    from_user_id: str
    to_user_id: str
    text: str
    property_id: Optional[str] = None

class RecommendationOut(BaseModel):
    id: str
    from_user_id: str
    to_user_id: str
    text: str
    property_id: Optional[str]
    ai_rating: Optional[float]
    created_at: str

class IssueCreate(BaseModel):
    property_id: str
    raised_by: str
    details: str

class IssueOut(BaseModel):
    id: str
    property_id: str
    raised_by: str
    details: str
    status: str
    created_at: str

class NotificationCreate(BaseModel):
    recipient_id: str
    notif_type: str
    method: str  # SMS/email/push
    content: str

class NotificationOut(BaseModel):
    id: str
    recipient_id: str
    notif_type: str
    method: str
    content: str
    status: str
    created_at: str

class ChatMessageCreate(BaseModel):
    from_user_id: str
    to_user_id: str
    message: str
    property_id: Optional[str] = None

class ChatMessageOut(BaseModel):
    id: str
    from_user_id: str
    to_user_id: str
    message: str
    property_id: Optional[str]
    created_at: str

@app.on_event("startup")
async def startup():
    try:
        app.state.db = await asyncpg.create_pool(DATABASE_URL)
        print("✅ Connected to Supabase database successfully!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("🔄 Falling back to in-memory storage...")
        app.state.db = None

@app.on_event("shutdown")
async def shutdown():
    if app.state.db:
        await app.state.db.close()

@app.get("/")
async def read_root():
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetchval("SELECT NOW()")
                return {"message": "Rentum AI backend is running!", "db_time": str(result), "database": "connected"}
        except Exception as e:
            return {"message": "Rentum AI backend is running!", "database": "error", "error": str(e)}
    else:
        return {"message": "Rentum AI backend is running!", "database": "in-memory"}

@app.post("/users", response_model=UserOut)
async def create_user(user: UserCreate):
    new_user = {
        "id": get_next_id(),
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "profile_photo": user.profile_photo,
        "role": user.role,
        "created_at": "2024-01-01T00:00:00"
    }
    
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetchval("SELECT NOW()")
                new_user["created_at"] = str(result)
                await connection.execute("INSERT INTO users (id, name, email, phone, profile_photo, role, created_at) VALUES ($1, $2, $3, $4, $5, $6, $7)",
                                        new_user["id"], new_user["name"], new_user["email"], new_user["phone"], new_user["profile_photo"], new_user["role"], new_user["created_at"])
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            users_db.append(new_user)
    else:
        users_db.append(new_user)
    
    return new_user

@app.get("/users", response_model=List[UserOut])
async def list_users():
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetch("SELECT id, name, email, phone, profile_photo, role, created_at FROM users")
                return [{"id": row["id"], "name": row["name"], "email": row["email"], "phone": row["phone"], "profile_photo": row["profile_photo"], "role": row["role"], "created_at": str(row["created_at"])} for row in result]
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            return users_db
    else:
        return users_db

@app.post("/properties", response_model=PropertyOut)
async def create_property(property: PropertyCreate):
    new_property = {
        "id": get_next_id(),
        "owner_id": property.owner_id,
        "address": property.address,
        "details": property.details,
        "status": property.status,
        "created_at": "2024-01-01T00:00:00"
    }
    
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetchval("SELECT NOW()")
                new_property["created_at"] = str(result)
                await connection.execute("INSERT INTO properties (id, owner_id, address, details, status, created_at) VALUES ($1, $2, $3, $4, $5, $6)",
                                        new_property["id"], new_property["owner_id"], new_property["address"], new_property["details"], new_property["status"], new_property["created_at"])
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            properties_db.append(new_property)
    else:
        properties_db.append(new_property)
    
    return new_property

@app.get("/properties", response_model=List[PropertyOut])
async def list_properties():
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetch("SELECT id, owner_id, address, details, status, created_at FROM properties")
                return [{"id": row["id"], "owner_id": row["owner_id"], "address": row["address"], "details": dict(row["details"]) if row["details"] else None, "status": row["status"], "created_at": str(row["created_at"])} for row in result]
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            return properties_db
    else:
        return properties_db

@app.post("/auth/otp")
async def request_otp(email_or_phone: str):
    # Stub: send OTP
    return {"message": "OTP sent (stub)"}

@app.post("/auth/verify-otp")
async def verify_otp(email_or_phone: str, otp: str):
    # Stub: verify OTP
    return {"message": "OTP verified (stub)", "token": "fake-jwt-token"}

@app.post("/auth/google-login")
async def google_login(google_token: str):
    # Stub: Google OAuth login with OTP approval
    return {"message": "Google login successful (stub)", "token": "fake-jwt-token", "user_id": "google-user-123"}

@app.post("/ocr/scan-document")
async def scan_document(file_url: str, doc_type: str):
    # Stub: AI/OCR document scanning
    extracted_data = {
        "property_address": "123 Sample Street, Mumbai",
        "rent_amount": 25000,
        "deposit_amount": 50000,
        "tenant_name": "John Doe",
        "landlord_name": "Jane Smith",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "confidence_score": 0.95
    }
    return {"message": "Document scanned successfully", "extracted_data": extracted_data, "requires_review": True}

@app.post("/ocr/manual-review")
async def manual_review(scan_id: str, verified_data: dict, approved: bool):
    # Stub: Manual review after OCR
    if approved:
        return {"message": "Data approved and saved", "scan_id": scan_id, "status": "approved"}
    else:
        return {"message": "Data rejected, requires re-scan", "scan_id": scan_id, "status": "rejected"}

@app.post("/upload/document")
async def upload_document_file(file_data: str, file_name: str, user_id: str):
    # Stub: File upload to cloud storage
    file_url = f"https://storage.example.com/documents/{user_id}/{file_name}"
    return {"message": "File uploaded successfully", "file_url": file_url, "file_id": get_next_id()}

@app.post("/agreements", response_model=AgreementOut)
async def create_agreement(agreement: AgreementCreate):
    new_agreement = {
        **agreement.dict(),
        "id": get_next_id(),
        "status": "pending",
        "created_at": "2024-01-01T00:00:00"
    }
    
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetchval("SELECT NOW()")
                new_agreement["created_at"] = str(result)
                await connection.execute("INSERT INTO agreements (id, property_id, landlord_id, tenant_id, start_date, end_date, rent, deposit, clauses, document_url, status, created_at) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)",
                                        new_agreement["id"], new_agreement["property_id"], new_agreement["landlord_id"], new_agreement["tenant_id"], new_agreement["start_date"], new_agreement["end_date"], new_agreement["rent"], new_agreement["deposit"], new_agreement["clauses"], new_agreement["document_url"], new_agreement["status"], new_agreement["created_at"])
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            agreements_db.append(new_agreement)
    else:
        agreements_db.append(new_agreement)
    
    return new_agreement

@app.get("/agreements", response_model=List[AgreementOut])
async def list_agreements():
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetch("SELECT id, property_id, landlord_id, tenant_id, start_date, end_date, rent, deposit, clauses, document_url, status, created_at FROM agreements")
                return [{"id": row["id"], "property_id": row["property_id"], "landlord_id": row["landlord_id"], "tenant_id": row["tenant_id"], "start_date": row["start_date"], "end_date": row["end_date"], "rent": float(row["rent"]), "deposit": float(row["deposit"]), "clauses": dict(row["clauses"]) if row["clauses"] else None, "document_url": row["document_url"], "status": row["status"], "created_at": str(row["created_at"])} for row in result]
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            return agreements_db
    else:
        return agreements_db

@app.post("/documents", response_model=DocumentOut)
async def upload_document(document: DocumentCreate):
    new_document = {
        **document.dict(),
        "id": get_next_id(),
        "uploaded_at": "2024-01-01T00:00:00"
    }
    
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetchval("SELECT NOW()")
                new_document["uploaded_at"] = str(result)
                await connection.execute("INSERT INTO documents (id, user_id, property_id, doc_type, url, uploaded_at) VALUES ($1, $2, $3, $4, $5, $6)",
                                        new_document["id"], new_document["user_id"], new_document["property_id"], new_document["doc_type"], new_document["url"], new_document["uploaded_at"])
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            documents_db.append(new_document)
    else:
        documents_db.append(new_document)
    
    return new_document

@app.get("/documents", response_model=List[DocumentOut])
async def list_documents():
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetch("SELECT id, user_id, property_id, doc_type, url, uploaded_at FROM documents")
                return [{"id": row["id"], "user_id": row["user_id"], "property_id": row["property_id"], "doc_type": row["doc_type"], "url": row["url"], "uploaded_at": str(row["uploaded_at"])} for row in result]
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            return documents_db
    else:
        return documents_db

@app.post("/payments", response_model=PaymentOut)
async def create_payment(payment: PaymentCreate):
    new_payment = {
        **payment.dict(),
        "id": get_next_id(),
        "status": "pending",
        "created_at": "2024-01-01T00:00:00"
    }
    
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetchval("SELECT NOW()")
                new_payment["created_at"] = str(result)
                await connection.execute("INSERT INTO payments (id, user_id, property_id, amount, payment_type, proof_url, status, created_at) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)",
                                        new_payment["id"], new_payment["user_id"], new_payment["property_id"], new_payment["amount"], new_payment["payment_type"], new_payment["proof_url"], new_payment["status"], new_payment["created_at"])
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            payments_db.append(new_payment)
    else:
        payments_db.append(new_payment)
    
    return new_payment

@app.get("/payments", response_model=List[PaymentOut])
async def list_payments():
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetch("SELECT id, user_id, property_id, amount, payment_type, proof_url, status, created_at FROM payments")
                return [{"id": row["id"], "user_id": row["user_id"], "property_id": row["property_id"], "amount": row["amount"], "payment_type": row["payment_type"], "proof_url": row["proof_url"], "status": row["status"], "created_at": str(row["created_at"])} for row in result]
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            return payments_db
    else:
        return payments_db

@app.post("/recommendations", response_model=RecommendationOut)
async def create_recommendation(rec: RecommendationCreate):
    new_recommendation = {
        **rec.dict(),
        "id": get_next_id(),
        "ai_rating": 4.5,
        "created_at": "2024-01-01T00:00:00"
    }
    
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetchval("SELECT NOW()")
                new_recommendation["created_at"] = str(result)
                await connection.execute("INSERT INTO recommendations (id, from_user_id, to_user_id, text, property_id, ai_rating, created_at) VALUES ($1, $2, $3, $4, $5, $6, $7)",
                                        new_recommendation["id"], new_recommendation["from_user_id"], new_recommendation["to_user_id"], new_recommendation["text"], new_recommendation["property_id"], new_recommendation["ai_rating"], new_recommendation["created_at"])
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            recommendations_db.append(new_recommendation)
    else:
        recommendations_db.append(new_recommendation)
    
    return new_recommendation

@app.get("/recommendations", response_model=List[RecommendationOut])
async def list_recommendations():
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetch("SELECT id, from_user_id, to_user_id, text, property_id, ai_rating, created_at FROM recommendations")
                return [{"id": row["id"], "from_user_id": row["from_user_id"], "to_user_id": row["to_user_id"], "text": row["text"], "property_id": row["property_id"], "ai_rating": row["ai_rating"], "created_at": str(row["created_at"])} for row in result]
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            return recommendations_db
    else:
        return recommendations_db

@app.post("/issues", response_model=IssueOut)
async def create_issue(issue: IssueCreate):
    new_issue = {
        **issue.dict(),
        "id": get_next_id(),
        "status": "open",
        "created_at": "2024-01-01T00:00:00"
    }
    
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetchval("SELECT NOW()")
                new_issue["created_at"] = str(result)
                await connection.execute("INSERT INTO issues (id, property_id, raised_by, details, status, created_at) VALUES ($1, $2, $3, $4, $5, $6)",
                                        new_issue["id"], new_issue["property_id"], new_issue["raised_by"], new_issue["details"], new_issue["status"], new_issue["created_at"])
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            issues_db.append(new_issue)
    else:
        issues_db.append(new_issue)
    
    return new_issue

@app.get("/issues", response_model=List[IssueOut])
async def list_issues():
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetch("SELECT id, property_id, raised_by, details, status, created_at FROM issues")
                return [{"id": row["id"], "property_id": row["property_id"], "raised_by": row["raised_by"], "details": row["details"], "status": row["status"], "created_at": str(row["created_at"])} for row in result]
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            return issues_db
    else:
        return issues_db

@app.post("/notifications", response_model=NotificationOut)
async def create_notification(notif: NotificationCreate):
    new_notification = {
        **notif.dict(),
        "id": get_next_id(),
        "status": "sent",
        "created_at": "2024-01-01T00:00:00"
    }
    
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetchval("SELECT NOW()")
                new_notification["created_at"] = str(result)
                await connection.execute("INSERT INTO notifications (id, recipient_id, notif_type, method, content, status, created_at) VALUES ($1, $2, $3, $4, $5, $6, $7)",
                                        new_notification["id"], new_notification["recipient_id"], new_notification["notif_type"], new_notification["method"], new_notification["content"], new_notification["status"], new_notification["created_at"])
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            notifications_db.append(new_notification)
    else:
        notifications_db.append(new_notification)
    
    return new_notification

@app.get("/notifications", response_model=List[NotificationOut])
async def list_notifications():
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetch("SELECT id, recipient_id, notif_type, method, content, status, created_at FROM notifications")
                return [{"id": row["id"], "recipient_id": row["recipient_id"], "notif_type": row["notif_type"], "method": row["method"], "content": row["content"], "status": row["status"], "created_at": str(row["created_at"])} for row in result]
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            return notifications_db
    else:
        return notifications_db

@app.post("/chat", response_model=ChatMessageOut)
async def send_message(msg: ChatMessageCreate):
    new_message = {
        **msg.dict(),
        "id": get_next_id(),
        "created_at": "2024-01-01T00:00:00"
    }
    
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetchval("SELECT NOW()")
                new_message["created_at"] = str(result)
                await connection.execute("INSERT INTO chat_messages (id, from_user_id, to_user_id, message, property_id, created_at) VALUES ($1, $2, $3, $4, $5, $6)",
                                        new_message["id"], new_message["from_user_id"], new_message["to_user_id"], new_message["message"], new_message["property_id"], new_message["created_at"])
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            chat_db.append(new_message)
    else:
        chat_db.append(new_message)
    
    return new_message

@app.get("/chat", response_model=List[ChatMessageOut])
async def list_messages():
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetch("SELECT id, from_user_id, to_user_id, message, property_id, created_at FROM chat_messages")
                return [{"id": row["id"], "from_user_id": row["from_user_id"], "to_user_id": row["to_user_id"], "message": row["message"], "property_id": row["property_id"], "created_at": str(row["created_at"])} for row in result]
        except Exception as e:
            print(f"Database error, using in-memory: {e}")
            return chat_db
    else:
        return chat_db

@app.post("/dual-approval")
async def dual_approval(action_id: str, user_id: str):
    # Stub: mark approval
    return {"message": "Approval recorded (stub)"}
