import React, { useEffect, useState } from 'react';
import './App.css';

// Import all the components
import Dashboard from './components/Dashboard';
import PropertyDetails from './components/PropertyDetails';
import Documents from './components/Documents';
import Payments from './components/Payments';
import Issues from './components/Issues';
import Notifications from './components/Notifications';
import Chat from './components/Chat';
import OCRScanner from './components/OCRScanner';
import AIReviews from './components/AIReviews';
import Profile from './components/Profile';
import Login from './components/Login';

// API URL configuration for both development and production
const API_BASE = process.env.REACT_APP_API_URL || process.env.NODE_ENV === 'production' 
  ? 'https://rentum-ai-property-management.vercel.app/api'  // Updated with correct backend URL
  : 'http://localhost:8008'; // Local development

console.log('🔗 API_BASE URL:', API_BASE, '(Environment:', process.env.NODE_ENV, ')');
// Build fix applied - eslint warnings resolved ✅

function App() {
  // Navigation state
  const [activeTab, setActiveTab] = useState('users');
  const [darkMode, setDarkMode] = useState(false);
  
  // Connection status
  const [apiConnected, setApiConnected] = useState(null);
  
  // User authentication simulation
  const [currentUser, setCurrentUser] = useState(null);
  const [loginForm, setLoginForm] = useState({ email: '', role: 'tenant' });
  
  // Check for URL parameters (e.g., ?role=tenant&landlord_id=123)
  const [urlParams, setUrlParams] = useState(null);
  
  // State for users
  const [users, setUsers] = useState([]);
  const [userForm, setUserForm] = useState({ name: '', email: '', phone: '', role: 'tenant' });
  const [isRegistering, setIsRegistering] = useState(false);
  
  // State for properties
  const [properties, setProperties] = useState([]);
  const [propertyForm, setPropertyForm] = useState({ owner_id: '', address: '', details: '', status: 'active' });
  
  // State for agreements
  const [agreements, setAgreements] = useState([]);
  const [agreementForm, setAgreementForm] = useState({ property_id: '', landlord_id: '', tenant_id: '', start_date: '', end_date: '', rent: '', deposit: '', clauses: '', document_url: '' });
  
  // State for documents
  const [documents, setDocuments] = useState([]);
  const [documentForm, setDocumentForm] = useState({ user_id: '', property_id: '', doc_type: '', file: null });
  
  // State for payments
  const [payments, setPayments] = useState([]);
  const [paymentForm, setPaymentForm] = useState({ user_id: '', property_id: '', amount: '', payment_type: '', proof_file: null });
  
  // State for issues
  const [issues, setIssues] = useState([]);
  const [issueForm, setIssueForm] = useState({ property_id: '', raised_by: '', details: '' });
  
  // State for notifications
  const [notifications, setNotifications] = useState([]);
  
  // State for chat
  const [chat, setChat] = useState([]);
  const [chatForm, setChatForm] = useState({ from_user_id: '', to_user_id: '', message: '', property_id: '' });
  
  // State for OCR and review system
  const [ocrScans, setOcrScans] = useState([]);
  const [ocrForm, setOcrForm] = useState({ user_id: '', document_type: '', file: null });
  const [reviewRequests, setReviewRequests] = useState([]);
  const [reviewRequestForm, setReviewRequestForm] = useState({ requester_id: '', reviewer_id: '', reviewer_email: '', request_type: '', property_id: '', message: '' });
  const [reviewResponses, setReviewResponses] = useState([]);
  const [reviewResponseForm, setReviewResponseForm] = useState({ 
    request_id: '', reviewer_id: '', reviewer_email: '', 
    payment_reliability: '', property_maintenance: '', communication: '', lease_compliance: '',
    responsiveness: '', property_condition: '', fairness: '', privacy_respect: '',
    overall_rating: '', comments: ''
  });
  const [userProfile, setUserProfile] = useState(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get('role')) {
      const roleFromUrl = params.get('role');
      const landlordId = params.get('landlord_id');
      setUrlParams({ role: roleFromUrl, landlord_id: landlordId });
      setUserForm(prev => ({ ...prev, role: roleFromUrl }));
    }
  }, []);

  // Fetch users and other data
  useEffect(() => {
    const fetchData = async () => {
      console.log('🔄 Starting data fetch from API:', API_BASE);
      try {
        const [usersRes, propertiesRes, agreementsRes, documentsRes, paymentsRes, issuesRes, notificationsRes, chatRes, reviewRequestsRes, reviewResponsesRes] = await Promise.all([
          fetch(`${API_BASE}/users`),
          fetch(`${API_BASE}/properties`),
          fetch(`${API_BASE}/agreements`),
          fetch(`${API_BASE}/documents`),
          fetch(`${API_BASE}/payments`),
          fetch(`${API_BASE}/issues`),
          fetch(`${API_BASE}/notifications`),
          fetch(`${API_BASE}/chat`),
          fetch(`${API_BASE}/reviews/requests`),
          fetch(`${API_BASE}/reviews/responses`)
        ]);

        console.log('📊 API Response Status:', {
          users: usersRes.status,
          properties: propertiesRes.status,
          agreements: agreementsRes.status
        });

        if (usersRes.ok) {
          const usersData = await usersRes.json();
          console.log('✅ Users loaded:', usersData.length, 'users');
          setUsers(usersData);
          setApiConnected(true);
        } else {
          console.warn('⚠️ Users API failed, loading fallback demo data');
          setApiConnected(false);
          setUsers([
            { id: 1, name: 'John Tenant', email: 'tenant@demo.com', role: 'tenant', created_at: new Date().toISOString() },
            { id: 2, name: 'Jane Landlord', email: 'landlord@demo.com', role: 'landlord', created_at: new Date().toISOString() },
            { id: 3, name: 'ABC Company', email: 'company@demo.com', role: 'company', created_at: new Date().toISOString() }
          ]);
        }

        if (propertiesRes.ok) setProperties(await propertiesRes.json());
        else setProperties([
          { id: 1, owner_id: 1, address: '123 Demo Street, Demo City', status: 'active', created_at: new Date().toISOString() }
        ]);
        
        if (agreementsRes.ok) setAgreements(await agreementsRes.json());
        else setAgreements([
          { id: 1, property_id: 1, landlord_id: 2, tenant_id: 1, start_date: '2024-01-01', end_date: '2024-12-31', rent: '1500', deposit: '3000' }
        ]);
        
        if (documentsRes.ok) setDocuments(await documentsRes.json());
        else setDocuments([]);
        
        if (paymentsRes.ok) setPayments(await paymentsRes.json());
        else setPayments([
          { id: 1, user_id: 1, property_id: 1, amount: '1500', payment_type: 'rent', created_at: new Date().toISOString() }
        ]);
        
        if (issuesRes.ok) setIssues(await issuesRes.json());
        else setIssues([
          { id: 1, property_id: 1, raised_by: 1, details: 'Demo issue: Kitchen faucet leaking', status: 'open', created_at: new Date().toISOString() }
        ]);
        
        if (notificationsRes.ok) setNotifications(await notificationsRes.json());
        else setNotifications([
          { id: 1, recipient_id: 1, notif_type: 'payment_due', content: 'Rent payment due on 1st of next month', created_at: new Date().toISOString() }
        ]);
        
        if (chatRes.ok) setChat(await chatRes.json());
        else setChat([
          { id: 1, from_user_id: 1, to_user_id: 2, message: 'Hello! This is a demo message.', property_id: 1, created_at: new Date().toISOString() }
        ]);
        
        if (reviewRequestsRes.ok) setReviewRequests(await reviewRequestsRes.json());
        else setReviewRequests([]);
        
        if (reviewResponsesRes.ok) setReviewResponses(await reviewResponsesRes.json());
        else setReviewResponses([]);
      } catch (error) {
        console.error('❌ Failed to fetch initial data:', error);
        setApiConnected(false);
        // Fallback to demo data if API completely fails
        setUsers([
          { id: 1, name: 'John Tenant', email: 'tenant@demo.com', role: 'tenant', created_at: new Date().toISOString() },
          { id: 2, name: 'Jane Landlord', email: 'landlord@demo.com', role: 'landlord', created_at: new Date().toISOString() },
          { id: 3, name: 'ABC Company', email: 'company@demo.com', role: 'company', created_at: new Date().toISOString() }
        ]);
        setProperties([
          { id: 1, owner_id: 1, address: '123 Demo Street, Demo City', status: 'active', created_at: new Date().toISOString() }
        ]);
        setAgreements([
          { id: 1, property_id: 1, landlord_id: 2, tenant_id: 1, start_date: '2024-01-01', end_date: '2024-12-31', rent: '1500', deposit: '3000' }
        ]);
        setDocuments([]);
        setPayments([
          { id: 1, user_id: 1, property_id: 1, amount: '1500', payment_type: 'rent', created_at: new Date().toISOString() }
        ]);
        setIssues([
          { id: 1, property_id: 1, raised_by: 1, details: 'Demo issue: Kitchen faucet leaking', status: 'open', created_at: new Date().toISOString() }
        ]);
        setNotifications([
          { id: 1, recipient_id: 1, notif_type: 'payment_due', content: 'Rent payment due on 1st of next month', created_at: new Date().toISOString() }
        ]);
        setChat([
          { id: 1, from_user_id: 1, to_user_id: 2, message: 'Hello! This is a demo message.', property_id: 1, created_at: new Date().toISOString() }
        ]);
        setReviewRequests([]);
        setReviewResponses([]);
      }
    };

    fetchData();
  }, []);

  // Fetch user-specific data when user logs in
  useEffect(() => {
    if (currentUser) {
      fetch(`${API_BASE}/ocr/scans?user_id=${currentUser.id}`)
        .then(res => res.json())
        .then(setOcrScans)
        .catch(err => console.log('OCR scans fetch error:', err));
    }
  }, [currentUser]);

  // Login simulation
  const handleLogin = (e) => {
    e.preventDefault();
    console.log('🔐 Attempting login for:', loginForm.email, 'role:', loginForm.role);
    
    let user = users.find(u => u.email === loginForm.email && u.role === loginForm.role);
    
    // If user not found in loaded users, check against fallback demo users
    if (!user && loginForm.email.includes('@demo.com')) {
      const demoUsers = [
        { id: 1, name: 'John Tenant', email: 'tenant@demo.com', role: 'tenant', created_at: new Date().toISOString() },
        { id: 2, name: 'Jane Landlord', email: 'landlord@demo.com', role: 'landlord', created_at: new Date().toISOString() },
        { id: 3, name: 'ABC Company', email: 'company@demo.com', role: 'company', created_at: new Date().toISOString() }
      ];
      user = demoUsers.find(u => u.email === loginForm.email && u.role === loginForm.role);
      console.log('🎯 Using fallback demo user:', user);
    }
    
    if (user) {
      console.log('✅ Login successful for:', user.name);
      setCurrentUser(user);
      setActiveTab('dashboard');
      
      // Try to fetch profile, but don't fail if API is down
      fetch(`${API_BASE}/users/${user.id}/profile`)
        .then(res => res.json())
        .then(setUserProfile)
        .catch(err => {
          console.log('⚠️ Profile fetch error (non-critical):', err);
          // Set a basic profile for demo purposes
          setUserProfile({
            green_flags_count: { communication: 5, reliability: 4 },
            red_flags_count: { late_payment: 1 },
            overall_rating: 4.2
          });
        });
    } else {
      alert('User not found. Please use the demo accounts provided or register a new account.');
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    setActiveTab('users');
  };

  // Filter data based on user role
  const getFilteredData = () => {
    if (!currentUser) return { 
      documents, payments, issues, notifications, chat,
      ocr_scans: ocrScans, review_requests: reviewRequests, review_responses: reviewResponses
    };
    
    if (currentUser.role === 'tenant') {
      return {
        documents: documents.filter(d => d.user_id === currentUser.id),
        payments: payments.filter(p => p.user_id === currentUser.id),
        issues: issues.filter(i => i.raised_by === currentUser.id),
        notifications: notifications.filter(n => n.recipient_id === currentUser.id),
        chat: chat.filter(c => c.from_user_id === currentUser.id || c.to_user_id === currentUser.id),
        ocr_scans: ocrScans.filter(s => s.user_id === currentUser.id),
        review_requests: reviewRequests.filter(r => r.requester_id === currentUser.id || r.reviewer_id === currentUser.id),
        review_responses: reviewResponses.filter(r => {
          const request = reviewRequests.find(req => req.id === r.request_id);
          return request && (request.requester_id === currentUser.id || r.reviewer_id === currentUser.id);
        })
      };
    } else if (currentUser.role === 'landlord') {
      return {
        documents: documents.filter(d => d.user_id === currentUser.id),
        payments: payments.filter(p => p.user_id === currentUser.id),
        issues: issues.filter(i => i.raised_by === currentUser.id),
        notifications: notifications.filter(n => n.recipient_id === currentUser.id),
        chat: chat.filter(c => c.from_user_id === currentUser.id || c.to_user_id === currentUser.id),
        ocr_scans: ocrScans.filter(s => s.user_id === currentUser.id),
        review_requests: reviewRequests.filter(r => r.requester_id === currentUser.id || r.reviewer_id === currentUser.id),
        review_responses: reviewResponses.filter(r => {
          const request = reviewRequests.find(req => req.id === r.request_id);
          return request && (request.requester_id === currentUser.id || r.reviewer_id === currentUser.id);
        })
      };
    }
    
    return { 
      documents, payments, issues, notifications, chat,
      ocr_scans: ocrScans, review_requests: reviewRequests, review_responses: reviewResponses
    };
  };

  const filteredData = getFilteredData();

  // Handlers
  const handleUserChange = e => setUserForm({ ...userForm, [e.target.name]: e.target.value });
  const handleDocumentChange = e => setDocumentForm({ ...documentForm, [e.target.name]: e.target.value });
  const handlePaymentChange = e => setPaymentForm({ ...paymentForm, [e.target.name]: e.target.value });
  const handleIssueChange = e => setIssueForm({ ...issueForm, [e.target.name]: e.target.value });
  const handleChatChange = e => setChatForm({ ...chatForm, [e.target.name]: e.target.value });
  const handleLoginChange = e => setLoginForm({ ...loginForm, [e.target.name]: e.target.value });
  
  // OCR Upload Handler
  const handleOcrUpload = async () => {
    if (!currentUser) {
      alert('Please log in first to use the AI Scanner');
      return;
    }
    
    if (!ocrForm.file || !ocrForm.document_type) {
      alert('Please select a file and document type');
      return;
    }
    
    console.log('🔍 Starting OCR upload for user:', currentUser.id, 'document type:', ocrForm.document_type);
    
    const formData = new FormData();
    formData.append('file', ocrForm.file);
    formData.append('user_id', currentUser.id);
    formData.append('document_type', ocrForm.document_type);
    
    try {
      const res = await fetch(`${API_BASE}/ocr/scan`, {
        method: 'POST',
        body: formData
      });
      
      if (res.ok) {
        const newScan = await res.json();
        setOcrScans([...ocrScans, newScan]);
        setOcrForm({ user_id: '', document_type: '', file: null });
        autoFillFromOcrData(newScan);
      } else {
        console.warn('⚠️ OCR API failed, using demo OCR results');
        handleDemoOcr();
      }
    } catch (error) {
      console.warn('⚠️ OCR API connection failed, using demo OCR results:', error.message);
      handleDemoOcr();
    }
  };
  
  // Demo OCR functionality when API is unavailable
  const handleDemoOcr = () => {
    const demoOcrResult = {
      id: Date.now(),
      user_id: currentUser.id,
      document_type: ocrForm.document_type,
      status: 'completed',
      confidence_score: 0.85,
      extracted_data: ocrForm.document_type === 'rental_agreement' ? {
        property_address: '123 Demo Street, Demo City, Demo State 12345',
        rent_amount: '1500',
        security_deposit: '3000',
        lease_start_date: '2024-01-01',
        lease_end_date: '2024-12-31',
        landlord_name: 'Jane Landlord',
        tenant_name: 'John Tenant',
        property_type: 'Apartment',
        utilities_included: 'Water and Trash',
        pet_policy: 'No pets allowed',
        key_terms: ['Monthly rent due on 1st', 'Security deposit refundable', '30 day notice required']
      } : ocrForm.document_type === 'id_card' ? {
        name: 'Demo User',
        id_number: 'DEMO123456789',
        address: '123 Demo Street, Demo City',
        date_of_birth: '1990-01-01'
      } : {
        document_title: 'Demo Property Document',
        property_address: '123 Demo Street, Demo City',
        document_date: new Date().toISOString().split('T')[0]
      },
      confidence_scores: {
        property_address: 0.92,
        rent_amount: 0.88,
        landlord_name: 0.85,
        tenant_name: 0.87
      },
      created_at: new Date().toISOString()
    };

    setOcrScans([...ocrScans, demoOcrResult]);
    setOcrForm({ user_id: '', document_type: '', file: null });
    
    const message = `🎯 Demo OCR scan completed!\n\n📋 This is a demonstration of how our AI scanner works:\n• Document type: ${ocrForm.document_type}\n• Confidence score: 85%\n• Key information extracted\n\n⚠️ Note: This is demo data since the OCR API is currently unavailable.`;
    alert(message);
    
    autoFillFromOcrData(demoOcrResult);
  };

  const autoFillFromOcrData = (scanResult) => {
    if (scanResult.document_type === 'rental_agreement') {
      const message = `🎯 Rental agreement scanned successfully!\n\n📋 Go to the "Agreements" section to view all extracted data including:\n• Property information\n• Landlord and tenant details\n• Financial terms\n• Lease dates\n• Confidence scores\n\nThe AI has processed your document and the data is ready for review!`;
      alert(message);
          setActiveTab('agreements');
    } else {
      const message = `🎯 Document scanned successfully!\n\n📊 Document type: ${scanResult.document_type}\n📋 Check the "Agreements" section if this was a rental agreement, or the "AI Scanner" tab to see all scan results.`;
      alert(message);
    }
  };

  // Review handlers
  const handleReviewRequest = async () => {
    const requestData = {
      ...reviewRequestForm,
      requester_id: currentUser.id
    };
    
    try {
      const res = await fetch(`${API_BASE}/reviews/request`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData)
      });
      if (res.ok) {
        const newRequest = await res.json();
        setReviewRequests([...reviewRequests, newRequest]);
        setReviewRequestForm({ requester_id: '', reviewer_id: '', reviewer_email: '', request_type: '', property_id: '', message: '' });
        alert('Review request sent successfully!');
      }
    } catch (error) {
      alert('Review request failed: ' + error.message);
    }
  };

  const handleReviewResponse = async () => {
    const responseData = {
      ...reviewResponseForm,
      reviewer_id: currentUser.id
    };
    
    try {
      const res = await fetch(`${API_BASE}/reviews/response`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(responseData)
      });
      if (res.ok) {
        const newResponse = await res.json();
        setReviewResponses([...reviewResponses, newResponse]);
        setReviewResponseForm({ 
          request_id: '', reviewer_id: '', reviewer_email: '', 
          payment_reliability: '', property_maintenance: '', communication: '', lease_compliance: '',
          responsiveness: '', property_condition: '', fairness: '', privacy_respect: '',
          overall_rating: '', comments: ''
        });
        alert('Review submitted successfully with AI analysis!');
      }
    } catch (error) {
      alert('Review submission failed: ' + error.message);
    }
  };

  // CRUD operations
  const addUser = async e => {
    e.preventDefault();
    setIsRegistering(true);
    try {
      const res = await fetch(`${API_BASE}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userForm)
      });
      if (res.ok) {
        const newUser = await res.json();
        setUsers([...users, newUser]);
        setUserForm({ name: '', email: '', phone: '', role: 'tenant' });
        alert(`✅ Registration successful! Welcome ${newUser.name}!`);
      } else {
        const errorData = await res.json();
        alert(`❌ Registration failed: ${errorData.detail || 'Unknown error'}`);
      }
    } catch (error) {
      alert(`❌ Registration failed: ${error.message}`);
    } finally {
      setIsRegistering(false);
    }
  };

  // eslint-disable-next-line no-unused-vars
  const addProperty = async e => {
    e.preventDefault();
    const propertyData = { 
      ...propertyForm, 
      owner_id: currentUser ? currentUser.id : propertyForm.owner_id,
      details: propertyForm.details ? { info: propertyForm.details } : {} 
    };
    const res = await fetch(`${API_BASE}/properties`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(propertyData)
    });
    if (res.ok) {
      const newProperty = await res.json();
      setProperties([...properties, newProperty]);
      setPropertyForm({ owner_id: '', address: '', details: '', status: 'active' });
    }
  };

  // eslint-disable-next-line no-unused-vars
  const addAgreement = async e => {
    e.preventDefault();
    const res = await fetch(`${API_BASE}/agreements`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(agreementForm)
    });
    if (res.ok) { 
      const newItem = await res.json(); 
      setAgreements([...agreements, newItem]); 
      setAgreementForm({ property_id: '', landlord_id: '', tenant_id: '', start_date: '', end_date: '', rent: '', deposit: '', clauses: '', document_url: '' }); 
    }
  };

  const addDocument = async e => {
    e.preventDefault();
    if (!documentForm.file) {
      alert('Please select a file to upload');
      return;
    }
    
    const formData = new FormData();
    formData.append('file', documentForm.file);
    formData.append('user_id', currentUser ? currentUser.id : documentForm.user_id);
    formData.append('property_id', documentForm.property_id || '');
    formData.append('doc_type', documentForm.doc_type);
    
    try {
      const res = await fetch(`${API_BASE}/documents`, {
        method: 'POST',
        body: formData
      });
      if (res.ok) { 
        const newItem = await res.json(); 
        setDocuments([...documents, newItem]); 
        setDocumentForm({ user_id: '', property_id: '', doc_type: '', file: null }); 
        alert('Document uploaded successfully!');
      }
    } catch (error) {
      alert('Document upload failed: ' + error.message);
    }
  };

  const addPayment = async e => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('user_id', currentUser ? currentUser.id : paymentForm.user_id);
    formData.append('property_id', paymentForm.property_id);
    formData.append('amount', paymentForm.amount);
    formData.append('payment_type', paymentForm.payment_type);
    if (paymentForm.proof_file) {
      formData.append('proof_file', paymentForm.proof_file);
    }
    
    try {
      const res = await fetch(`${API_BASE}/payments`, {
        method: 'POST',
        body: formData
      });
      if (res.ok) { 
        const newItem = await res.json(); 
        setPayments([...payments, newItem]); 
        setPaymentForm({ user_id: '', property_id: '', amount: '', payment_type: '', proof_file: null }); 
        alert('Payment recorded successfully!');
      }
    } catch (error) {
      alert('Payment recording failed: ' + error.message);
    }
  };

  const addIssue = async e => {
    e.preventDefault();
    const issueData = { 
      ...issueForm, 
      raised_by: currentUser ? currentUser.id : issueForm.raised_by 
    };
    const res = await fetch(`${API_BASE}/issues`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(issueData)
    });
    if (res.ok) { 
      const newItem = await res.json(); 
      setIssues([...issues, newItem]); 
      setIssueForm({ property_id: '', raised_by: '', details: '' }); 
    }
  };

  const addChat = async e => {
    e.preventDefault();
    const chatData = { 
      ...chatForm, 
      from_user_id: currentUser ? currentUser.id : chatForm.from_user_id 
    };
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(chatData)
    });
    if (res.ok) { 
      const newItem = await res.json(); 
      setChat([...chat, newItem]); 
      setChatForm({ from_user_id: '', to_user_id: '', message: '', property_id: '' }); 
    }
  };

  const tabs = currentUser ? [
    { id: 'dashboard', label: 'Dashboard', icon: '🏠' },
    { id: 'property-details', label: 'Property Details', icon: '🏡' },
    { id: 'documents', label: 'Documents', icon: '📄' },
    { id: 'agreements', label: 'Agreements', icon: '📋' },
    { id: 'ocr-scanner', label: 'AI Scanner', icon: '🔍' },
    { id: 'payments', label: 'Payments', icon: '💳' },
    { id: 'ai-reviews', label: 'AI Reviews', icon: '🤖' },
    { id: 'profile', label: 'AI Profile', icon: '👤' },
    { id: 'issues', label: 'Issues', icon: '🔧' },
    { id: 'notifications', label: 'Notifications', icon: '🔔' },
    { id: 'chat', label: 'Messages', icon: '💬' }
  ] : [
    { id: 'users', label: 'Register/Login', icon: '👥' }
  ];

  // Login screen
  if (!currentUser) {
    return (
      <Login 
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        users={users}
        loginForm={loginForm}
        handleLoginChange={handleLoginChange}
        handleLogin={handleLogin}
        userForm={userForm}
        handleUserChange={handleUserChange}
        addUser={addUser}
        isRegistering={isRegistering}
        urlParams={urlParams}
        setLoginForm={setLoginForm}
        apiConnected={apiConnected}
      />
    );
  }

  const renderTabContent = () => {
    switch(activeTab) {
      case 'dashboard':
        return (
          <Dashboard 
            currentUser={currentUser}
            users={users}
            properties={properties}
            filteredData={filteredData}
            ocrScans={ocrScans}
            setActiveTab={setActiveTab}
          />
        );
      case 'property-details':
        return (
          <PropertyDetails 
            currentUser={currentUser}
            ocrScans={ocrScans}
            darkMode={darkMode}
          />
        );
      case 'documents':
        return (
          <Documents 
            filteredData={filteredData}
            documentForm={documentForm}
            handleDocumentChange={handleDocumentChange}
            addDocument={addDocument}
            setDocumentForm={setDocumentForm}
          />
        );
      case 'agreements':
        return (
          <div className="section">
            <h2>📋 Rental Agreements</h2>
            <div className="agreements-container">
              <div className="agreements-list">
                <h3>Your Agreements</h3>
                {agreements.length > 0 ? (
                  agreements.map(agreement => (
                    <div key={agreement.id} className="agreement-item">
                      <h4>Agreement #{agreement.id}</h4>
                      <p><strong>Property:</strong> {properties.find(p => p.id === agreement.property_id)?.address || 'N/A'}</p>
                      <p><strong>Start Date:</strong> {agreement.start_date}</p>
                      <p><strong>End Date:</strong> {agreement.end_date}</p>
                      <p><strong>Rent:</strong> ${agreement.rent}</p>
                      <p><strong>Deposit:</strong> ${agreement.deposit}</p>
                    </div>
                  ))
                ) : (
                  <p>No agreements found. Upload a rental agreement in the AI Scanner to extract agreement details automatically.</p>
                )}
              </div>
            </div>
          </div>
        );
      case 'payments':
        return (
          <Payments 
            currentUser={currentUser}
            filteredData={filteredData}
            paymentForm={paymentForm}
            handlePaymentChange={handlePaymentChange}
            addPayment={addPayment}
            setPaymentForm={setPaymentForm}
          />
        );
      case 'issues':
        return (
          <Issues 
            currentUser={currentUser}
            filteredData={filteredData}
            issueForm={issueForm}
            handleIssueChange={handleIssueChange}
            addIssue={addIssue}
          />
        );
      case 'notifications':
        return <Notifications filteredData={filteredData} />;
      case 'chat':
        return (
          <Chat 
            currentUser={currentUser}
            filteredData={filteredData}
            chatForm={chatForm}
            handleChatChange={handleChatChange}
            addChat={addChat}
          />
        );
      case 'ocr-scanner':
        return (
          <OCRScanner 
            currentUser={currentUser}
            filteredData={filteredData}
            ocrForm={ocrForm}
            setOcrForm={setOcrForm}
            handleOcrUpload={handleOcrUpload}
          />
        );
      case 'ai-reviews':
        return (
          <AIReviews 
            currentUser={currentUser}
            filteredData={filteredData}
            reviewRequestForm={reviewRequestForm}
            setReviewRequestForm={setReviewRequestForm}
            handleReviewRequest={handleReviewRequest}
            reviewResponseForm={reviewResponseForm}
            setReviewResponseForm={setReviewResponseForm}
            handleReviewResponse={handleReviewResponse}
          />
        );
      case 'profile':
        return (
          <Profile 
            currentUser={currentUser}
            userProfile={userProfile}
            setUserProfile={setUserProfile}
            API_BASE={API_BASE}
          />
        );
      default:
        return (
          <div className="section">
            <h2>{tabs.find(t => t.id === activeTab)?.icon} {tabs.find(t => t.id === activeTab)?.label}</h2>
            <p>Feature coming soon...</p>
          </div>
        );
    }
  };

  return (
    <div className={`App ${darkMode ? 'dark-mode' : ''}`}>
      <div className="header">
        <h1>🏠 Rentum AI Dashboard - {currentUser.role.toUpperCase()}</h1>
        <div className="header-actions">
          {apiConnected !== null && (
            <span className={`connection-status ${apiConnected ? 'connected' : 'demo'}`}>
              {apiConnected ? '🟢 Live Data' : '🟡 Demo Mode'}
            </span>
          )}
          <span className="user-greeting">Welcome, {currentUser.name}!</span>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
          <button 
            className="theme-toggle"
            onClick={() => setDarkMode(!darkMode)}
            title={`Switch to ${darkMode ? 'light' : 'dark'} mode`}
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
        </div>
      </div>
      
      {/* Navigation Tabs */}
      <div className="nav-tabs">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.icon} {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {renderTabContent()}
      </div>
    </div>
  );
}

export default App;
