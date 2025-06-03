-- Enhanced Rentum AI Database Schema with OCR and Review System

-- Existing tables (keeping current structure)
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    profile_photo TEXT,
    role TEXT NOT NULL CHECK (role IN ('tenant', 'landlord', 'company')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS properties (
    id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL REFERENCES users(id),
    address TEXT NOT NULL,
    details JSONB,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'rented')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS agreements (
    id TEXT PRIMARY KEY,
    property_id TEXT NOT NULL REFERENCES properties(id),
    landlord_id TEXT NOT NULL REFERENCES users(id),
    tenant_id TEXT NOT NULL REFERENCES users(id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    rent DECIMAL(10,2) NOT NULL,
    deposit DECIMAL(10,2) NOT NULL,
    clauses JSONB,
    document_url TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'completed', 'terminated')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    property_id TEXT REFERENCES properties(id),
    doc_type TEXT NOT NULL,
    url TEXT NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    property_id TEXT NOT NULL REFERENCES properties(id),
    amount DECIMAL(10,2) NOT NULL,
    payment_type TEXT NOT NULL,
    proof_url TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS recommendations (
    id TEXT PRIMARY KEY,
    from_user_id TEXT NOT NULL REFERENCES users(id),
    to_user_id TEXT NOT NULL REFERENCES users(id),
    text TEXT NOT NULL,
    property_id TEXT REFERENCES properties(id),
    ai_rating DECIMAL(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS issues (
    id TEXT PRIMARY KEY,
    property_id TEXT NOT NULL REFERENCES properties(id),
    raised_by TEXT NOT NULL REFERENCES users(id),
    details TEXT NOT NULL,
    status TEXT DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS notifications (
    id TEXT PRIMARY KEY,
    recipient_id TEXT NOT NULL REFERENCES users(id),
    notif_type TEXT NOT NULL,
    method TEXT NOT NULL CHECK (method IN ('sms', 'email', 'push')),
    content TEXT NOT NULL,
    status TEXT DEFAULT 'sent' CHECK (status IN ('pending', 'sent', 'delivered', 'failed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id TEXT PRIMARY KEY,
    from_user_id TEXT NOT NULL REFERENCES users(id),
    to_user_id TEXT NOT NULL REFERENCES users(id),
    message TEXT NOT NULL,
    property_id TEXT REFERENCES properties(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- NEW TABLES FOR OCR AND REVIEW SYSTEM

-- OCR Scans table
CREATE TABLE IF NOT EXISTS ocr_scans (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    document_type TEXT NOT NULL CHECK (document_type IN ('rental_agreement', 'id_card', 'property_document')),
    original_image_url TEXT NOT NULL,
    extracted_data JSONB NOT NULL,
    confidence_scores JSONB,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'approved', 'rejected')),
    manual_corrections JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    reviewed_at TIMESTAMP WITH TIME ZONE
);

-- Review Requests table
CREATE TABLE IF NOT EXISTS review_requests (
    id TEXT PRIMARY KEY,
    requester_id TEXT NOT NULL REFERENCES users(id),
    reviewer_id TEXT NOT NULL REFERENCES users(id),
    reviewer_email TEXT, -- For external reviewers not on platform
    request_type TEXT NOT NULL CHECK (request_type IN ('tenant_review', 'landlord_review')),
    property_id TEXT REFERENCES properties(id),
    message TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'expired', 'declined')),
    deadline TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Review Responses table
CREATE TABLE IF NOT EXISTS review_responses (
    id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL REFERENCES review_requests(id),
    reviewer_id TEXT REFERENCES users(id), -- NULL for external reviewers
    reviewer_email TEXT, -- For external reviewers
    
    -- Structured review data
    payment_reliability INTEGER CHECK (payment_reliability BETWEEN 1 AND 5),
    property_maintenance INTEGER CHECK (property_maintenance BETWEEN 1 AND 5),
    communication INTEGER CHECK (communication BETWEEN 1 AND 5),
    lease_compliance INTEGER CHECK (lease_compliance BETWEEN 1 AND 5),
    responsiveness INTEGER CHECK (responsiveness BETWEEN 1 AND 5),
    property_condition INTEGER CHECK (property_condition BETWEEN 1 AND 5),
    fairness INTEGER CHECK (fairness BETWEEN 1 AND 5),
    privacy_respect INTEGER CHECK (privacy_respect BETWEEN 1 AND 5),
    
    overall_rating INTEGER NOT NULL CHECK (overall_rating BETWEEN 1 AND 5),
    comments TEXT,
    proof_urls JSONB, -- For negative feedback proof
    
    -- AI Analysis
    ai_overall_score DECIMAL(3,1), -- 0-10 scale
    ai_risk_assessment TEXT CHECK (ai_risk_assessment IN ('low', 'medium', 'high')),
    ai_green_flags JSONB,
    ai_red_flags JSONB,
    ai_analysis_summary TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Profiles with AI Scores (aggregated from reviews)
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id TEXT PRIMARY KEY REFERENCES users(id),
    overall_ai_score DECIMAL(3,1), -- 0-10 aggregated score
    total_reviews INTEGER DEFAULT 0,
    avg_payment_reliability DECIMAL(3,2),
    avg_property_maintenance DECIMAL(3,2),
    avg_communication DECIMAL(3,2),
    avg_lease_compliance DECIMAL(3,2),
    avg_responsiveness DECIMAL(3,2),
    avg_property_condition DECIMAL(3,2),
    avg_fairness DECIMAL(3,2),
    avg_privacy_respect DECIMAL(3,2),
    green_flags_count JSONB,
    red_flags_count JSONB,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_ocr_scans_user_id ON ocr_scans(user_id);
CREATE INDEX IF NOT EXISTS idx_ocr_scans_status ON ocr_scans(status);
CREATE INDEX IF NOT EXISTS idx_review_requests_requester ON review_requests(requester_id);
CREATE INDEX IF NOT EXISTS idx_review_requests_reviewer ON review_requests(reviewer_id);
CREATE INDEX IF NOT EXISTS idx_review_requests_status ON review_requests(status);
CREATE INDEX IF NOT EXISTS idx_review_responses_request ON review_responses(request_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_score ON user_profiles(overall_ai_score);

-- Sample data (keeping existing + adding new)
INSERT INTO users (id, name, email, phone, profile_photo, role) VALUES
('1', 'John Doe', 'john@example.com', '+91-9876543210', 'https://example.com/john.jpg', 'landlord'),
('2', 'Jane Smith', 'jane@example.com', '+91-9876543211', 'https://example.com/jane.jpg', 'tenant'),
('3', 'ABC Properties', 'contact@abcproperties.com', '+91-9876543212', 'https://example.com/abc.jpg', 'company')
ON CONFLICT (id) DO NOTHING;

INSERT INTO properties (id, owner_id, address, details, status) VALUES
('1', '1', '123 Main Street, Mumbai, Maharashtra', '{"bedrooms": 2, "bathrooms": 1, "area": "800 sqft"}', 'active'),
('2', '1', '456 Park Avenue, Delhi, NCR', '{"bedrooms": 3, "bathrooms": 2, "area": "1200 sqft"}', 'active')
ON CONFLICT (id) DO NOTHING;

-- Initialize user profiles for existing users
INSERT INTO user_profiles (user_id, overall_ai_score, total_reviews) VALUES
('1', 8.5, 0),
('2', 9.0, 0),
('3', 7.5, 0)
ON CONFLICT (user_id) DO NOTHING; 