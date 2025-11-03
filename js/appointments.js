// Appointments Management

// Show/Hide booking form
function showBookingForm() {
    document.getElementById('bookingForm').style.display = 'block';
}

function hideBookingForm() {
    document.getElementById('bookingForm').style.display = 'none';
    document.getElementById('appointmentForm').reset();
}

// Handle appointment booking
document.getElementById('appointmentForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!authToken) {
        showToast('Please login to book an appointment', 'error');
        navigateTo('login');
        return;
    }

    const doctorId = document.getElementById('doctorSelect').value;
    const appointmentDate = document.getElementById('appointmentDate').value;
    const appointmentType = document.getElementById('appointmentType').value;
    const reason = document.getElementById('reason').value;

    if (!doctorId) {
        showToast('Please select a doctor', 'error');
        return;
    }

    try {
        // Get patient_id from current user
        const patientId = currentUser.patient_id || 1; // Default to 1 for demo

        const response = await fetch(`${API_BASE_URL}/appointments/?patient_id=${patientId}&doctor_id=${doctorId}&appointment_date=${appointmentDate}&appointment_type=${appointmentType}&reason=${encodeURIComponent(reason)}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Booking failed');
        }

        const appointment = await response.json();
        showToast('Appointment booked successfully!', 'success');
        hideBookingForm();
        loadAppointments();
    } catch (error) {
        showToast(error.message, 'error');
        console.error('Booking error:', error);
    }
});

// Load appointments
async function loadAppointments() {
    if (!authToken) {
        document.getElementById('appointmentsList').innerHTML = '<p>Please login to view appointments</p>';
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/appointments/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`,
            }
        });

        if (!response.ok) {
            throw new Error('Failed to load appointments');
        }

        const appointments = await response.json();
        displayAppointments(appointments);
    } catch (error) {
        console.error('Error loading appointments:', error);
        document.getElementById('appointmentsList').innerHTML = '<p>Failed to load appointments</p>';
    }
}

function displayAppointments(appointments) {
    const container = document.getElementById('appointmentsList');
    
    if (appointments.length === 0) {
        container.innerHTML = '<p>No appointments found</p>';
        return;
    }

    container.innerHTML = appointments.map(apt => `
        <div class="appointment-card">
            <h4>Appointment #${apt.appointment_id}</h4>
            <p><strong>Date:</strong> ${formatDateTime(apt.appointment_date)}</p>
            <p><strong>Doctor ID:</strong> ${apt.doctor_id}</p>
            <p><strong>Type:</strong> ${apt.appointment_type}</p>
            <p><strong>Status:</strong> <span class="status-badge status-${apt.status}">${apt.status}</span></p>
            ${apt.reason ? `<p><strong>Reason:</strong> ${apt.reason}</p>` : ''}
            ${apt.notes ? `<p><strong>Notes:</strong> ${apt.notes}</p>` : ''}
            <div style="margin-top: 1rem;">
                ${apt.status === 'scheduled' ? `
                    <button class="btn btn-secondary" onclick="cancelAppointment(${apt.appointment_id})">Cancel</button>
                ` : ''}
            </div>
        </div>
    `).join('');
}

// Cancel appointment
async function cancelAppointment(appointmentId) {
    if (!confirm('Are you sure you want to cancel this appointment?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`,
            }
        });

        if (!response.ok) {
            throw new Error('Failed to cancel appointment');
        }

        showToast('Appointment cancelled successfully', 'success');
        loadAppointments();
    } catch (error) {
        showToast('Failed to cancel appointment', 'error');
        console.error('Cancel error:', error);
    }
}

// Make functions globally available
window.showBookingForm = showBookingForm;
window.hideBookingForm = hideBookingForm;
window.loadAppointments = loadAppointments;
window.cancelAppointment = cancelAppointment;