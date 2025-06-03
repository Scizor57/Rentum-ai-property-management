# Rentum AI — Masterplan

## App Overview & Objectives

Rentum AI is a web-based property management platform for the Indian rental market, built for individual landlords and tenants. It leverages AI and modern design to automate, secure, and simplify the rental experience, from agreement management to payments and communication. The vision is to bring transparency, convenience, and trust to rental relationships.

---

## Target Audience

- **MVP Focus:** Individual landlords and tenants in India.
- **Future Expansion:** Property managers and real estate companies with extended profile/permissions.
- **User familiarity:** Comfortable with OTP authentication, digital payments, and document uploads.

---

## Core Features & Functionality

- **User Onboarding:** Email or phone-based registration with OTP, Google login with OTP approval. Optional two-factor authentication.
- **Profile Management:** Landlords and tenants manage their own profiles and rental history.
- **Property Management:** Add properties manually or via AI-powered lease scanning (OCR).
- **Document Vault:** Upload and securely store key docs (Aadhaar, PAN, police verification, agreements, payment proofs).
- **Automated Data Extraction:** AI/OCR auto-fills property and agreement details, followed by user review and confirmation.
- **Security Deposit & Payment Handling:** App wallet for loading money via UPI/cards/wallets, schedule auto-payments, upload payment proofs, and manage deposits.
- **Reminders & Notifications:** SMS, email, and push for rent, renewals, and requests.
- **Recommendations & Feedback:** Landlords and tenants can request or provide digital recommendations via templates, with AI-aided analysis.
- **Chat & Requests:** Built-in messaging for direct landlord–tenant communication, with conversational LLM agent as a future upgrade.
- **Issue Management:** Tenants can raise issues, landlords can respond, all tracked within property/rental tabs.
- **Manual Review:** After OCR, users must verify and confirm extracted data to handle scan errors.
- **Fraud Prevention:** Dual-approval for all sensitive steps (both landlord and tenant must confirm).

---

## High-Level Technical Stack Recommendations

- **Frontend:** Responsive web app (React, Vue, or Angular recommended for modularity and UI flexibility).
- **Backend:** Node.js, Python (FastAPI), or similar for RESTful APIs and background processing.
- **Database:** Cloud-hosted relational DB (PostgreSQL, MySQL) with strong encryption.
- **Cloud Storage:** AWS S3, Google Cloud Storage, or Azure Blob in Indian region for documents (AES-256 encryption at rest).
- **Authentication:** OTP-based login (email/SMS), Google login with OTP, optional 2FA (TOTP apps).
- **Payment Gateway:** Razorpay, Paytm, or similar for wallet and rent payment handling.
- **OCR/AI Services:** Best-in-class cloud OCR (e.g., Mistral, Google Vision, or AWS Textract) with fallback to manual review.
- **SMS/Email:** Twilio, SendGrid, or local providers for notifications and OTPs.
- **Future Expansion:** Architect backend for multi-tenancy and scalable user/role management to accommodate property managers/companies.

---

## Conceptual Data Model

- **User:** (Landlord, Tenant, Company)  
  - Name, contact, profile photo, ID docs, recommendations, roles
- **Property:**  
  - Address, details, agreement (scanned/original), current/past tenants, status
- **Rental Agreement:**  
  - Parties, dates, rent, clauses, deposit info, digital copy, extracted fields
- **Payment:**  
  - Wallet top-ups, rent transactions, payment proofs, schedule/auto-pay status
- **Recommendation:**  
  - From/to user, text, AI rating, template, linked to past properties
- **Issue:**  
  - Property, raised by, status, details, resolution
- **Notifications:**  
  - Type, recipient, method (SMS/email/push), content, status

---

## User Interface Design Principles

- **Clean, modern, minimal, and professional look**
- **Sky blue + white gradient** color palette
- **Light/dark mode toggle**
- **Dashboard-centric navigation**
- **Card-based views for properties/rentals**
- **Step-by-step guided flows for uploads, scans, payments**
- **Clear, prominent CTAs**
- **Accessibility:** Readable fonts, intuitive color contrast, mobile responsiveness
- **Persistent chat/messaging bar**

---

## Security Considerations

- **All sensitive data encrypted at rest (AES-256) and in transit (SSL/TLS)**
- **Field masking in UI for Aadhaar, PAN, and other PII**
- **No password storage; OTP-based authentication**
- **Role-based access control (RBAC) for user actions and data visibility**
- **Full audit logs for document access and changes**
- **Manual user review after OCR data extraction**
- **Dual-approval flows for critical actions (e.g., finalizing agreements, releasing deposits)**
- **Cloud storage in India for regulatory compliance**

---

## Development Phases / Milestones

1. **Phase 1: MVP Launch**
    - User onboarding (OTP, Google)
    - Property and agreement management (manual and AI/OCR flows)
    - Document vault
    - Payment wallet integration
    - SMS/email reminders
    - Basic recommendations
    - Manual review after OCR
    - Chat and issue management
    - Clean, responsive UI (light/dark mode)
2. **Phase 2: Enhanced Automation & Integrations**
    - ID/document verification APIs
    - Conversational LLM agent for requests
    - UPI auto-mandates
    - Company/property manager accounts
    - Regional language support (OCR and UI)
3. **Phase 3: Scale & Optimize**
    - Advanced analytics for property performance
    - Fraud/forgery detection tools
    - Integration with external rental platforms
    - Advanced notification/push systems
    - New features based on user feedback

---

## Potential Challenges & Solutions

- **OCR accuracy:**  
  Solution: Always require user verification after AI scan, especially for poor-quality uploads or non-English docs.
- **Indian language handling:**  
  Solution: Start with Hindi/English, add regional OCR and UI later as adoption grows.
- **Document forgery/fraud:**  
  Solution: Dual-approval, audit logs, and future integration with government ID verification APIs.
- **Scalability:**  
  Solution: Cloud-native backend, modular design, plan for multi-tenancy early.

---

## Future Expansion Possibilities

- Onboard property management companies with advanced admin/permission models.
- Full KYC/ID verification flows for users.
- Direct integration with legal, police, or local municipality systems for verification.
- Advanced analytics and reporting for landlords/companies.
- Mobile app for iOS/Android once workflows are validated on web.
- Integration with IoT/smart home features for automated property management.

---

*This masterplan is a living document—feel free to update as your vision evolves!*

