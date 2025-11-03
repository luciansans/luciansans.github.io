// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';
let authToken = localStorage.getItem('authToken');
let currentUser = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeNavigation();
    checkAuthentication();
    loadDoctors();
});

// Navigation
function initializeNavigation() {
    // Handle navigation clicks
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = e.target.getAttribute('href').substring(1);
            navigateTo(target);
        });
    });

    // Handle form footer links
    document.querySelectorAll('.form-footer a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = e.target.getAttribute('href').substring(1);
            navigateTo(target);
        });
    });

    // Handle login form
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    
    // Handle register form
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
}

function navigateTo(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });

    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
        
        // Load section-specific data
        if (sectionId === 'appointments' && authToken) {
            loadAppointments();
        } else if (sectionId === 'doctors') {
            loadDoctors();
        } else if (sectionId === 'queue') {
            loadDoctorsForQueue();
        }
    }
}

// Authentication
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        authToken = data.access_token;
        currentUser = data.user;
        
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('currentUser', JSON.stringify(currentUser));

        showToast('Login successful!', 'success');
        updateAuthUI();
        navigateTo('home');
    } catch (error) {
        showToast('Login failed. Please check your credentials.', 'error');
        console.error('Login error:', error);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const role = document.getElementById('role').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register?username=${username}&email=${email}&password=${password}&role=${role}`, {
            method: 'POST',
        });

        if (!response.ok) {
            throw new Error('Registration failed');
        }

        showToast('Registration successful! Please login.', 'success');
        navigateTo('login');
    } catch (error) {
        showToast('Registration failed. Username or email may already exist.', 'error');
        console.error('Registration error:', error);
    }
}

function checkAuthentication() {
    authToken = localStorage.getItem('authToken');
    const userStr = localStorage.getItem('currentUser');
    
    if (authToken && userStr) {
        currentUser = JSON.parse(userStr);
        updateAuthUI();
    }
}

function updateAuthUI() {
    const authLink = document.getElementById('authLink');
    
    if (authToken && currentUser) {
        authLink.innerHTML = `<a href="#" onclick="handleLogout()">Logout (${currentUser.username})</a>`;
    } else {
        authLink.innerHTML = '<a href="#login">Login</a>';
    }
}

function handleLogout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    
    updateAuthUI();
    showToast('Logged out successfully', 'success');
    navigateTo('home');
}

// Load Doctors
async function loadDoctors() {
    try {
        const response = await fetch(`${API_BASE_URL}/doctors`);
        const doctors = await response.json();
        
        displayDoctors(doctors);
        populateDoctorSelects(doctors);
    } catch (error) {
        console.error('Error loading doctors:', error);
        showToast('Failed to load doctors', 'error');
    }
}

function displayDoctors(doctors) {
    const container = document.getElementById('doctorsList');
    
    if (doctors.length === 0) {
        container.innerHTML = '<p>No doctors available</p>';
        return;
    }

    container.innerHTML = doctors.map(doctor => `
        <div class="doctor-card">
            <h3>${doctor.full_name}</h3>
            <p class="specialization">${doctor.specialization}</p>
            <p>📧 ${doctor.email}</p>
            <p>📞 ${doctor.contact_number}</p>
            ${doctor.room_number ? `<p>🚪 Room ${doctor.room_number}</p>` : ''}
        </div>
    `).join('');
}

function populateDoctorSelects(doctors) {
    const selects = [
        document.getElementById('doctorSelect'),
        document.getElementById('queueDoctorSelect')
    ];

    selects.forEach(select => {
        if (select) {
            select.innerHTML = '<option value="">Select a doctor</option>' +
                doctors.map(doctor => 
                    `<option value="${doctor.doctor_id}">${doctor.full_name} - ${doctor.specialization}</option>`
                ).join('');
        }
    });
}

// Utility Functions
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-ZA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-ZA', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Make functions globally available
window.navigateTo = navigateTo;
window.handleLogout = handleLogout;
window.showToast = showToast;
window.formatDateTime = formatDateTime;
window.formatDate = formatDate;