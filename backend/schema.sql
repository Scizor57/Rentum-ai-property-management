-- Rentum AI Database Schema for Supabase (Fixed Version)
-- Run this in your Supabase SQL editor

-- Drop tables if they exist (in reverse order due to foreign keys)
DROP TABLE IF EXISTS chat_messages CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS issues CASCADE;
DROP TABLE IF EXISTS recommendations CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS agreements CASCADE;
DROP TABLE IF EXISTS properties CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table (no dependencies)
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    profile_photo TEXT,
    role TEXT NOT NULL CHECK (role IN ('tenant', 'landlord', 'company')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Properties table (depends on users)
CREATE TABLE properties (
    id TEXT PRIMARY KEY,
    owner_id TEXT NOT NULL,
    address TEXT NOT NULL,
    details JSONB,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Agreements table (depends on properties and users)
CREATE TABLE agreements (
    id TEXT PRIMARY KEY,
    property_id TEXT NOT NULL,
    landlord_id TEXT NOT NULL,
    tenant_id TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    rent DECIMAL(10,2) NOT NULL,
    deposit DECIMAL(10,2) NOT NULL,
    clauses JSONB,
    document_url TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'expired', 'terminated')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    FOREIGN KEY (landlord_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (tenant_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Documents table (depends on users and properties)
CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    property_id TEXT,
    doc_type TEXT NOT NULL,
    url TEXT NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE SET NULL
);

-- Payments table (depends on users and properties)
CREATE TABLE payments (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    property_id TEXT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_type TEXT NOT NULL,
    proof_url TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

-- Recommendations table (depends on users and properties)
CREATE TABLE recommendations (
    id TEXT PRIMARY KEY,
    from_user_id TEXT NOT NULL,
    to_user_id TEXT NOT NULL,
    text TEXT NOT NULL,
    property_id TEXT,
    ai_rating DECIMAL(3,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (from_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (to_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE SET NULL
);

-- Issues table (depends on properties and users)
CREATE TABLE issues (
    id TEXT PRIMARY KEY,
    property_id TEXT NOT NULL,
    raised_by TEXT NOT NULL,
    details TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    FOREIGN KEY (raised_by) REFERENCES users(id) ON DELETE CASCADE
);

-- Notifications table (depends on users)
CREATE TABLE notifications (
    id TEXT PRIMARY KEY,
    recipient_id TEXT NOT NULL,
    notif_type TEXT NOT NULL,
    method TEXT NOT NULL CHECK (method IN ('SMS', 'email', 'push')),
    content TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'sent' CHECK (status IN ('pending', 'sent', 'delivered', 'failed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Chat messages table (depends on users and properties)
CREATE TABLE chat_messages (
    id TEXT PRIMARY KEY,
    from_user_id TEXT NOT NULL,
    to_user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    property_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (from_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (to_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE SET NULL
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_properties_owner ON properties(owner_id);
CREATE INDEX idx_properties_status ON properties(status);
CREATE INDEX idx_agreements_property ON agreements(property_id);
CREATE INDEX idx_agreements_landlord ON agreements(landlord_id);
CREATE INDEX idx_agreements_tenant ON agreements(tenant_id);
CREATE INDEX idx_agreements_status ON agreements(status);
CREATE INDEX idx_documents_user ON documents(user_id);
CREATE INDEX idx_documents_property ON documents(property_id);
CREATE INDEX idx_payments_user ON payments(user_id);
CREATE INDEX idx_payments_property ON payments(property_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_recommendations_from ON recommendations(from_user_id);
CREATE INDEX idx_recommendations_to ON recommendations(to_user_id);
CREATE INDEX idx_issues_property ON issues(property_id);
CREATE INDEX idx_issues_raised_by ON issues(raised_by);
CREATE INDEX idx_issues_status ON issues(status);
CREATE INDEX idx_notifications_recipient ON notifications(recipient_id);
CREATE INDEX idx_notifications_status ON notifications(status);
CREATE INDEX idx_chat_from_user ON chat_messages(from_user_id);
CREATE INDEX idx_chat_to_user ON chat_messages(to_user_id);
CREATE INDEX idx_chat_property ON chat_messages(property_id);

-- Insert sample data for testing
INSERT INTO users (id, name, email, phone, profile_photo, role) VALUES 
('1', 'John Doe', 'john@example.com', '+91-9876543210', 'https://example.com/john.jpg', 'landlord'),
('2', 'Jane Smith', 'jane@example.com', '+91-9876543211', 'https://example.com/jane.jpg', 'tenant'),
('3', 'ABC Properties', 'contact@abcproperties.com', '+91-9876543212', 'https://example.com/abc.jpg', 'company');

INSERT INTO properties (id, owner_id, address, details, status) VALUES 
('1', '1', '123 Main Street, Mumbai, Maharashtra', '{"bedrooms": 2, "bathrooms": 1, "area": "800 sqft"}', 'active'),
('2', '1', '456 Park Avenue, Delhi, Delhi', '{"bedrooms": 3, "bathrooms": 2, "area": "1200 sqft"}', 'active'),
('3', '3', '789 Garden Road, Bangalore, Karnataka', '{"bedrooms": 1, "bathrooms": 1, "area": "600 sqft"}', 'inactive');

-- Verify tables were created
SELECT 'Tables created successfully!' as status; 