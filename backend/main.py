from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncpg
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import shutil
from pathlib import Path

# Import our new services
from ocr_service import ocr_service
from ai_review_service import ai_review_analyzer

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

# NEW MODELS FOR OCR AND REVIEW SYSTEM

class OCRScanCreate(BaseModel):
    user_id: str
    document_type: str  # 'rental_agreement', 'id_card', 'property_document'

class OCRScanOut(BaseModel):
    id: str
    user_id: str
    document_type: str
    original_image_url: str
    extracted_data: dict
    confidence_scores: dict
    status: str
    manual_corrections: Optional[dict]
    created_at: str

class ReviewRequestCreate(BaseModel):
    requester_id: str
    reviewer_id: Optional[str] = None
    reviewer_email: Optional[str] = None
    request_type: str  # 'tenant_review', 'landlord_review'
    property_id: Optional[str] = None
    message: Optional[str] = None

class ReviewRequestOut(BaseModel):
    id: str
    requester_id: str
    reviewer_id: Optional[str]
    reviewer_email: Optional[str]
    request_type: str
    property_id: Optional[str]
    message: Optional[str]
    status: str
    deadline: str
    created_at: str

class ReviewResponseCreate(BaseModel):
    request_id: str
    reviewer_id: Optional[str] = None
    reviewer_email: Optional[str] = None
    payment_reliability: Optional[int] = None
    property_maintenance: Optional[int] = None
    communication: Optional[int] = None
    lease_compliance: Optional[int] = None
    responsiveness: Optional[int] = None
    property_condition: Optional[int] = None
    fairness: Optional[int] = None
    privacy_respect: Optional[int] = None
    overall_rating: int
    comments: Optional[str] = None
    proof_urls: Optional[List[str]] = None

class ReviewResponseOut(BaseModel):
    id: str
    request_id: str
    reviewer_id: Optional[str]
    reviewer_email: Optional[str]
    payment_reliability: Optional[int]
    property_maintenance: Optional[int]
    communication: Optional[int]
    lease_compliance: Optional[int]
    responsiveness: Optional[int]
    property_condition: Optional[int]
    fairness: Optional[int]
    privacy_respect: Optional[int]
    overall_rating: int
    comments: Optional[str]
    proof_urls: Optional[List[str]]
    ai_overall_score: Optional[float]
    ai_risk_assessment: Optional[str]
    ai_green_flags: Optional[List[str]]
    ai_red_flags: Optional[List[str]]
    ai_analysis_summary: Optional[str]
    created_at: str

class UserProfileOut(BaseModel):
    user_id: str
    overall_ai_score: Optional[float]
    total_reviews: int
    avg_payment_reliability: Optional[float]
    avg_property_maintenance: Optional[float]
    avg_communication: Optional[float]
    avg_lease_compliance: Optional[float]
    avg_responsiveness: Optional[float]
    avg_property_condition: Optional[float]
    avg_fairness: Optional[float]
    avg_privacy_respect: Optional[float]
    green_flags_count: Optional[dict]
    red_flags_count: Optional[dict]
    last_updated: str

@app.on_event("startup")
async def startup():
    try:
        app.state.db = await asyncpg.create_pool(DATABASE_URL)
        print("✅ Connected to database successfully!")
        
        # Test the connection
        async with app.state.db.acquire() as connection:
            result = await connection.fetchval("SELECT 1")
            print(f"✅ Database test query successful: {result}")
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("⚠️ Please check your DATABASE_URL in .env file")
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
                current_time = datetime.now()
                new_user["created_at"] = current_time.isoformat()
                await connection.execute("INSERT INTO users (id, name, email, phone, profile_photo, role, created_at) VALUES ($1, $2, $3, $4, $5, $6, $7)",
                                        new_user["id"], new_user["name"], new_user["email"], new_user["phone"], new_user["profile_photo"], new_user["role"], current_time)
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
                current_time = datetime.now()
                new_property["created_at"] = current_time.isoformat()
                await connection.execute("INSERT INTO properties (id, owner_id, address, details, status, created_at) VALUES ($1, $2, $3, $4, $5, $6)",
                                        new_property["id"], new_property["owner_id"], new_property["address"], new_property["details"], new_property["status"], current_time)
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
                current_time = datetime.now()
                new_agreement["created_at"] = current_time.isoformat()
                await connection.execute("INSERT INTO agreements (id, property_id, landlord_id, tenant_id, start_date, end_date, rent, deposit, clauses, document_url, status, created_at) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)",
                                        new_agreement["id"], new_agreement["property_id"], new_agreement["landlord_id"], new_agreement["tenant_id"], new_agreement["start_date"], new_agreement["end_date"], new_agreement["rent"], new_agreement["deposit"], new_agreement["clauses"], new_agreement["document_url"], new_agreement["status"], current_time)
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
async def upload_document(file: UploadFile = File(...), user_id: str = "", property_id: str = "", doc_type: str = ""):
    """Upload a document file"""
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = Path("uploads/documents")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Save uploaded file
        file_path = upload_dir / f"{get_next_id()}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        new_document = {
            "id": get_next_id(),
            "user_id": user_id,
            "property_id": property_id if property_id else None,
            "doc_type": doc_type,
            "url": str(file_path),
            "uploaded_at": "2024-01-01T00:00:00"
        }
        
        if app.state.db:
            try:
                async with app.state.db.acquire() as connection:
                    current_time = datetime.now()
                    new_document["uploaded_at"] = current_time.isoformat()
                    await connection.execute("INSERT INTO documents (id, user_id, property_id, doc_type, url, uploaded_at) VALUES ($1, $2, $3, $4, $5, $6)",
                                            new_document["id"], new_document["user_id"], new_document["property_id"], new_document["doc_type"], new_document["url"], current_time)
            except Exception as e:
                print(f"Database error, using in-memory: {e}")
                documents_db.append(new_document)
        else:
            documents_db.append(new_document)
        
        return new_document
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document upload failed: {str(e)}")

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
async def create_payment(user_id: str = "", property_id: str = "", amount: float = 0, payment_type: str = "", proof_file: UploadFile = File(None)):
    """Create a payment record with optional proof file"""
    try:
        proof_url = None
        if proof_file:
            # Create uploads directory if it doesn't exist
            upload_dir = Path("uploads/payments")
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            # Save uploaded file
            file_path = upload_dir / f"{get_next_id()}_{proof_file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(proof_file.file, buffer)
            proof_url = str(file_path)
        
        new_payment = {
            "id": get_next_id(),
            "user_id": user_id,
            "property_id": property_id,
            "amount": amount,
            "payment_type": payment_type,
            "proof_url": proof_url,
            "status": "pending",
            "created_at": "2024-01-01T00:00:00"
        }
        
        if app.state.db:
            try:
                async with app.state.db.acquire() as connection:
                    current_time = datetime.now()
                    new_payment["created_at"] = current_time.isoformat()
                    await connection.execute("INSERT INTO payments (id, user_id, property_id, amount, payment_type, proof_url, status, created_at) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)",
                                            new_payment["id"], new_payment["user_id"], new_payment["property_id"], new_payment["amount"], new_payment["payment_type"], new_payment["proof_url"], new_payment["status"], current_time)
            except Exception as e:
                print(f"Database error, using in-memory: {e}")
                payments_db.append(new_payment)
        else:
            payments_db.append(new_payment)
        
        return new_payment
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment creation failed: {str(e)}")

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

# NEW ENDPOINTS FOR OCR AND REVIEW SYSTEM

@app.post("/ocr/scan", response_model=OCRScanOut)
async def scan_document(
    file: UploadFile = File(...), 
    user_id: str = Form(...), 
    document_type: str = Form(...)
):
    """Upload and scan a document using OCR"""
    try:
        print(f"🔍 OCR scan request - user_id: {user_id}, document_type: {document_type}, file: {file.filename}")
        
        # Validate required parameters
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        if not document_type:
            raise HTTPException(status_code=400, detail="document_type is required")
        
        # Create uploads directory if it doesn't exist
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # Save uploaded file
        file_path = upload_dir / f"{get_next_id()}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"📁 File saved to: {file_path}")
        
        # Process document with OCR
        print(f"🤖 Processing document with OCR...")
        ocr_result = ocr_service.process_document(str(file_path), document_type)
        print(f"✅ OCR processing complete: {ocr_result}")
        
        # Create OCR scan record
        new_scan = {
            "id": get_next_id(),
            "user_id": user_id,
            "document_type": document_type,
            "original_image_url": str(file_path),
            "extracted_data": ocr_result.get('extracted_data', {}),
            "confidence_scores": ocr_result.get('confidence_scores', {}),
            "status": "pending",
            "manual_corrections": None,
            "created_at": "2024-01-01T00:00:00"
        }
        
        if app.state.db:
            try:
                async with app.state.db.acquire() as connection:
                    current_time = datetime.now()
                    new_scan["created_at"] = current_time.isoformat()
                    await connection.execute("""
                        INSERT INTO ocr_scans (id, user_id, document_type, original_image_url, 
                                             extracted_data, confidence_scores, status, created_at) 
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    """, new_scan["id"], new_scan["user_id"], new_scan["document_type"], 
                    new_scan["original_image_url"], json.dumps(new_scan["extracted_data"]), 
                    json.dumps(new_scan["confidence_scores"]), new_scan["status"], current_time)
            except Exception as e:
                print(f"Database error, using in-memory: {e}")
        
        return new_scan
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")

@app.get("/ocr/scans", response_model=List[OCRScanOut])
async def list_ocr_scans(user_id: str):
    """List OCR scans for a specific user only - PRIVACY CRITICAL"""
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required for data privacy")
    
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                result = await connection.fetch("""
                    SELECT id, user_id, document_type, original_image_url, extracted_data, 
                           confidence_scores, status, manual_corrections, created_at 
                    FROM ocr_scans WHERE user_id = $1 ORDER BY created_at DESC
                """, user_id)
                
                return [{
                    "id": row["id"],
                    "user_id": row["user_id"],
                    "document_type": row["document_type"],
                    "original_image_url": row["original_image_url"],
                    "extracted_data": json.loads(row["extracted_data"]) if row["extracted_data"] else {},
                    "confidence_scores": json.loads(row["confidence_scores"]) if row["confidence_scores"] else {},
                    "status": row["status"],
                    "manual_corrections": json.loads(row["manual_corrections"]) if row["manual_corrections"] else None,
                    "created_at": str(row["created_at"])
                } for row in result]
        except Exception as e:
            print(f"Database error: {e}")
            raise HTTPException(status_code=500, detail="Database error")
    
    # Fallback to in-memory storage, but still filter by user_id for privacy
    # This should never be used in production but keeping for development
    user_scans = [scan for scan in getattr(app.state, 'ocr_scans', []) if scan.get('user_id') == user_id]
    return user_scans

@app.post("/reviews/request", response_model=ReviewRequestOut)
async def create_review_request(request: ReviewRequestCreate):
    """Create a new review request"""
    new_request = {
        **request.dict(),
        "id": get_next_id(),
        "status": "pending",
        "created_at": "2024-01-01T00:00:00"
    }
    
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                current_time = datetime.now()
                new_request["created_at"] = current_time.isoformat()
                deadline_time = current_time + timedelta(hours=48)
                new_request["deadline"] = deadline_time.isoformat()
                await connection.execute("""
                    INSERT INTO review_requests (id, requester_id, reviewer_id, reviewer_email, 
                                               request_type, property_id, message, status, deadline, created_at) 
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                """, new_request["id"], new_request["requester_id"], new_request["reviewer_id"], 
                new_request["reviewer_email"], new_request["request_type"], new_request["property_id"], 
                new_request["message"], new_request["status"], deadline_time, current_time)
        except Exception as e:
            print(f"Database error: {e}")
    
    return new_request

@app.get("/reviews/requests", response_model=List[ReviewRequestOut])
async def list_review_requests(user_id: Optional[str] = None):
    """List review requests"""
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                if user_id:
                    result = await connection.fetch("""
                        SELECT id, requester_id, reviewer_id, reviewer_email, request_type, 
                               property_id, message, status, deadline, created_at 
                        FROM review_requests 
                        WHERE requester_id = $1 OR reviewer_id = $1 
                        ORDER BY created_at DESC
                    """, user_id)
                else:
                    result = await connection.fetch("""
                        SELECT id, requester_id, reviewer_id, reviewer_email, request_type, 
                               property_id, message, status, deadline, created_at 
                        FROM review_requests ORDER BY created_at DESC
                    """)
                
                return [{
                    "id": row["id"],
                    "requester_id": row["requester_id"],
                    "reviewer_id": row["reviewer_id"],
                    "reviewer_email": row["reviewer_email"],
                    "request_type": row["request_type"],
                    "property_id": row["property_id"],
                    "message": row["message"],
                    "status": row["status"],
                    "deadline": str(row["deadline"]),
                    "created_at": str(row["created_at"])
                } for row in result]
        except Exception as e:
            print(f"Database error: {e}")
    
    return []

@app.post("/reviews/response", response_model=ReviewResponseOut)
async def create_review_response(response: ReviewResponseCreate):
    """Submit a review response with AI analysis"""
    # Perform AI analysis on the review
    ai_analysis = ai_review_analyzer.analyze_review_response(response.dict())
    
    new_response = {
        **response.dict(),
        "id": get_next_id(),
        "ai_overall_score": ai_analysis.get('ai_overall_score'),
        "ai_risk_assessment": ai_analysis.get('ai_risk_assessment'),
        "ai_green_flags": ai_analysis.get('ai_green_flags'),
        "ai_red_flags": ai_analysis.get('ai_red_flags'),
        "ai_analysis_summary": ai_analysis.get('ai_analysis_summary'),
        "created_at": "2024-01-01T00:00:00"
    }
    
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                current_time = datetime.now()
                new_response["created_at"] = current_time.isoformat()
                await connection.execute("""
                    INSERT INTO review_responses (id, request_id, reviewer_id, reviewer_email,
                                                payment_reliability, property_maintenance, communication,
                                                lease_compliance, responsiveness, property_condition,
                                                fairness, privacy_respect, overall_rating, comments,
                                                proof_urls, ai_overall_score, ai_risk_assessment,
                                                ai_green_flags, ai_red_flags, ai_analysis_summary, created_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21)
                """, new_response["id"], new_response["request_id"], new_response["reviewer_id"],
                new_response["reviewer_email"], new_response["payment_reliability"], 
                new_response["property_maintenance"], new_response["communication"],
                new_response["lease_compliance"], new_response["responsiveness"],
                new_response["property_condition"], new_response["fairness"],
                new_response["privacy_respect"], new_response["overall_rating"],
                new_response["comments"], json.dumps(new_response["proof_urls"]),
                new_response["ai_overall_score"], new_response["ai_risk_assessment"],
                json.dumps(new_response["ai_green_flags"]), json.dumps(new_response["ai_red_flags"]),
                new_response["ai_analysis_summary"], current_time)
                
                # Update request status to completed
                await connection.execute("""
                    UPDATE review_requests SET status = 'completed' WHERE id = $1
                """, new_response["request_id"])
                
        except Exception as e:
            print(f"Database error: {e}")
    
    return new_response

@app.get("/reviews/responses", response_model=List[ReviewResponseOut])
async def list_review_responses(request_id: Optional[str] = None, user_id: Optional[str] = None):
    """List review responses"""
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                if request_id:
                    result = await connection.fetch("""
                        SELECT * FROM review_responses WHERE request_id = $1 ORDER BY created_at DESC
                    """, request_id)
                elif user_id:
                    result = await connection.fetch("""
                        SELECT rr.* FROM review_responses rr
                        JOIN review_requests req ON rr.request_id = req.id
                        WHERE req.requester_id = $1 ORDER BY rr.created_at DESC
                    """, user_id)
                else:
                    result = await connection.fetch("""
                        SELECT * FROM review_responses ORDER BY created_at DESC
                    """)
                
                return [{
                    "id": row["id"],
                    "request_id": row["request_id"],
                    "reviewer_id": row["reviewer_id"],
                    "reviewer_email": row["reviewer_email"],
                    "payment_reliability": row["payment_reliability"],
                    "property_maintenance": row["property_maintenance"],
                    "communication": row["communication"],
                    "lease_compliance": row["lease_compliance"],
                    "responsiveness": row["responsiveness"],
                    "property_condition": row["property_condition"],
                    "fairness": row["fairness"],
                    "privacy_respect": row["privacy_respect"],
                    "overall_rating": row["overall_rating"],
                    "comments": row["comments"],
                    "proof_urls": json.loads(row["proof_urls"]) if row["proof_urls"] else None,
                    "ai_overall_score": row["ai_overall_score"],
                    "ai_risk_assessment": row["ai_risk_assessment"],
                    "ai_green_flags": json.loads(row["ai_green_flags"]) if row["ai_green_flags"] else None,
                    "ai_red_flags": json.loads(row["ai_red_flags"]) if row["ai_red_flags"] else None,
                    "ai_analysis_summary": row["ai_analysis_summary"],
                    "created_at": str(row["created_at"])
                } for row in result]
        except Exception as e:
            print(f"Database error: {e}")
    
    return []

@app.get("/users/{user_id}/profile", response_model=UserProfileOut)
async def get_user_profile(user_id: str):
    """Get user profile with aggregated AI scores and review data"""
    if app.state.db:
        try:
            async with app.state.db.acquire() as connection:
                # Get existing profile
                profile = await connection.fetchrow("""
                    SELECT * FROM user_profiles WHERE user_id = $1
                """, user_id)
                
                if profile:
                    return {
                        "user_id": profile["user_id"],
                        "overall_ai_score": profile["overall_ai_score"],
                        "total_reviews": profile["total_reviews"],
                        "avg_payment_reliability": profile["avg_payment_reliability"],
                        "avg_property_maintenance": profile["avg_property_maintenance"],
                        "avg_communication": profile["avg_communication"],
                        "avg_lease_compliance": profile["avg_lease_compliance"],
                        "avg_responsiveness": profile["avg_responsiveness"],
                        "avg_property_condition": profile["avg_property_condition"],
                        "avg_fairness": profile["avg_fairness"],
                        "avg_privacy_respect": profile["avg_privacy_respect"],
                        "green_flags_count": json.loads(profile["green_flags_count"]) if profile["green_flags_count"] else {},
                        "red_flags_count": json.loads(profile["red_flags_count"]) if profile["red_flags_count"] else {},
                        "last_updated": str(profile["last_updated"])
                    }
        except Exception as e:
            print(f"Database error: {e}")
    
    # Return default profile if not found
    return {
        "user_id": user_id,
        "overall_ai_score": 0.0,
        "total_reviews": 0,
        "avg_payment_reliability": None,
        "avg_property_maintenance": None,
        "avg_communication": None,
        "avg_lease_compliance": None,
        "avg_responsiveness": None,
        "avg_property_condition": None,
        "avg_fairness": None,
        "avg_privacy_respect": None,
        "green_flags_count": {},
        "red_flags_count": {},
        "last_updated": str(datetime.now())
    } 