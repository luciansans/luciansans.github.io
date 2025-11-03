// Queue Management

// Load doctors for queue dropdown
async function loadDoctorsForQueue() {
    try {
        const response = await fetch(`${API_BASE_URL}/doctors`);
        const doctors = await response.json();
        
        const select = document.getElementById('queueDoctorSelect');
        select.innerHTML = '<option value="">Select a doctor</option>' +
            doctors.map(doctor => 
                `<option value="${doctor.doctor_id}">${doctor.full_name} - ${doctor.specialization}</option>`
            ).join('');
    } catch (error) {
        console.error('Error loading doctors:', error);
    }
}

// Load queue status for selected doctor
async function loadQueueStatus() {
    const doctorId = document.getElementById('queueDoctorSelect').value;
    
    if (!doctorId) {
        document.getElementById('queueList').innerHTML = '<p>Please select a doctor</p>';
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/queue/status/${doctorId}`);
        
        if (!response.ok) {
            throw new Error('Failed to load queue');
        }

        const queue = await response.json();
        displayQueue(queue);
    } catch (error) {
        console.error('Error loading queue:', error);
        document.getElementById('queueList').innerHTML = '<p>Failed to load queue status</p>';
    }
}

function displayQueue(queue) {
    const container = document.getElementById('queueList');
    
    if (queue.length === 0) {
        container.innerHTML = '<p>No patients in queue</p>';
        return;
    }

    container.innerHTML = `
        <h3>Current Queue (${queue.length} patients)</h3>
        ${queue.map(entry => `
            <div class="queue-item">
                <div class="queue-position">${entry.position || '—'}</div>
                <div class="queue-details">
                    <p><strong>Appointment ID:</strong> ${entry.appointment_id}</p>
                    <p><strong>Priority:</strong> ${entry.priority}</p>
                    <p><strong>Status:</strong> <span class="status-badge status-${entry.status}">${entry.status}</span></p>
                    <p><strong>Check-in:</strong> ${formatDateTime(entry.check_in_time)}</p>
                </div>
                <div class="queue-wait">
                    <p><strong>Est. Wait:</strong></p>
                    <p>${entry.estimated_wait_minutes || 0} min</p>
                </div>
            </div>
        `).join('')}
    `;
}

// Check in patient
async function checkInPatient(appointmentId) {
    if (!authToken) {
        showToast('Please login to check in', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/queue/check-in?appointment_id=${appointmentId}&priority=routine`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Check-in failed');
        }

        showToast('Checked in successfully!', 'success');
        loadQueueStatus();
    } catch (error) {
        showToast(error.message, 'error');
        console.error('Check-in error:', error);
    }
}

// Call next patient (for staff)
async function callNextPatient() {
    const doctorId = document.getElementById('queueDoctorSelect').value;
    
    if (!doctorId) {
        showToast('Please select a doctor', 'error');
        return;
    }

    if (!authToken) {
        showToast('Please login to call patients', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/queue/call-next/${doctorId}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to call next patient');
        }

        const nextPatient = await response.json();
        showToast(`Called patient from appointment #${nextPatient.appointment_id}`, 'success');
        loadQueueStatus();
    } catch (error) {
        showToast(error.message, 'error');
        console.error('Call next error:', error);
    }
}

// Auto-refresh queue every 30 seconds
let queueRefreshInterval = null;

function startQueueAutoRefresh() {
    if (queueRefreshInterval) {
        clearInterval(queueRefreshInterval);
    }
    
    queueRefreshInterval = setInterval(() => {
        const doctorId = document.getElementById('queueDoctorSelect').value;
        if (doctorId) {
            loadQueueStatus();
        }
    }, 30000); // 30 seconds
}

function stopQueueAutoRefresh() {
    if (queueRefreshInterval) {
        clearInterval(queueRefreshInterval);
        queueRefreshInterval = null;
    }
}

// Start auto-refresh when queue section is active
document.addEventListener('DOMContentLoaded', () => {
    const queueSection = document.getElementById('queue');
    if (queueSection) {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.target.classList.contains('active')) {
                    startQueueAutoRefresh();
                } else {
                    stopQueueAutoRefresh();
                }
            });
        });
        
        observer.observe(queueSection, { attributes: true, attributeFilter: ['class'] });
    }
});

// Make functions globally available
window.loadQueueStatus = loadQueueStatus;
window.loadDoctorsForQueue = loadDoctorsForQueue;
window.checkInPatient = checkInPatient;
window.callNextPatient = callNextPatient;