const consultations = [
    {
        id: 1,
        doctor: "Dr. Carlos Silva",
        specialty: "Cardiologia",
        date: "2025-01-31",
        time: "14:00",
        type: "Videochamada",
        status: "today",
        price: "R$ 150,00",
        avatar: "CS",
        rating: 4.8,
        prescription: true
    },
    {
        id: 2,
        doctor: "Dra. Ana Santos",
        specialty: "Dermatologia",
        date: "2025-02-01",
        time: "09:00",
        type: "Videochamada",
        status: "upcoming",
        price: "R$ 120,00",
        avatar: "AS",
        rating: 4.9,
        prescription: false
    },
    {
        id: 3,
        doctor: "Dr. Pedro Costa",
        specialty: "Clínica Geral",
        date: "2025-01-29",
        time: "16:30",
        type: "Chat",
        status: "completed",
        price: "R$ 100,00",
        avatar: "PC",
        rating: 4.7,
        prescription: true
    },
    {
        id: 4,
        doctor: "Dra. Maria Oliveira",
        specialty: "Pediatria",
        date: "2025-02-05",
        time: "10:00",
        type: "Videochamada",
        status: "upcoming",
        price: "R$ 130,00",
        avatar: "MO",
        rating: 4.9,
        prescription: false
    },
    {
        id: 5,
        doctor: "Dr. Roberto Lima",
        specialty: "Neurologia",
        date: "2025-01-25",
        time: "11:00",
        type: "Videochamada",
        status: "cancelled",
        price: "R$ 180,00",
        avatar: "RL",
        rating: 4.6,
        prescription: false
    }
];

let filteredConsultations = [...consultations];
let currentFilter = 'all';

function renderConsultations(consultationsToRender) {
    const consultationsList = document.getElementById('consultationsList');
    const emptyState = document.getElementById('emptyState');

    if (consultationsToRender.length === 0) {
        consultationsList.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';

    consultationsList.innerHTML = consultationsToRender.map(consultation => {
        const statusText = {
            today: 'Hoje',
            upcoming: 'Agendada',
            completed: 'Realizada',
            cancelled: 'Cancelada'
        };

        const actionButtons = getActionButtons(consultation);

        return `
                    <div class="consultation-card ${consultation.status}">
                        <div class="row align-items-center">
                            <div class="col-md-8">
                                <div class="d-flex align-items-center">
                                    <div class="doctor-avatar">${consultation.avatar}</div>
                                    <div class="flex-grow-1">
                                        <div class="d-flex align-items-center gap-2 mb-2">
                                            <div class="consultation-time">${formatDate(consultation.date)} às ${consultation.time}</div>
                                            <span class="status-badge ${consultation.status}">${statusText[consultation.status]}</span>
                                        </div>
                                        <h5 class="fw-bold text-azul mb-1">${consultation.doctor}</h5>
                                        <div class="d-flex align-items-center gap-2 mb-2">
                                            <span class="text-secondary">${consultation.specialty}</span>
                                            <span class="consultation-type">${consultation.type}</span>
                                        </div>
                                        <div class="d-flex align-items-center gap-3">
                                            <div class="rating-stars">
                                                ${'★'.repeat(Math.floor(consultation.rating))}${'☆'.repeat(5 - Math.floor(consultation.rating))}
                                                <span class="text-muted">${consultation.rating}</span>
                                            </div>
                                            <span class="fw-bold text-success">${consultation.price}</span>
                                            ${consultation.prescription ? '<a href="#" class="prescription-link"><i class="bi bi-file-earmark-medical me-1"></i>Ver receita</a>' : ''}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 text-end">
                                ${actionButtons}
                            </div>
                        </div>
                    </div>
                `;
    }).join('');
}

function getActionButtons(consultation) {
    switch (consultation.status) {
        case 'today':
            return `
                        <div class="d-flex gap-2 justify-content-end flex-wrap">
                            <a href="/sala_espera" class="btn btn-join" onclick="joinConsultation(${consultation.id})">
                                <i class="bi bi-camera-video me-2"></i>Entrar
                            </a>
                            <a href="/agendar_consulta" class="btn btn-azul" onclick="rescheduleConsultation(${consultation.id})">
                                <i class="bi bi-calendar me-2"></i>Reagendar
                            </a>
                            
                        </div>
                    `;
                    
        case 'upcoming':
            return `
                        <div class="d-flex gap-2 justify-content-end flex-wrap">
                            <a href="/agendar_consulta" class="btn btn-azul" onclick="rescheduleConsultation(${consultation.id})">
                                <i class="bi bi-calendar me-2"></i>Reagendar
                            </a>
                            <button class="btn btn-cancel" onclick="cancelConsultation(${consultation.id})">
                                <i class="bi bi-x-circle me-2"></i>Cancelar
                            </button>
                        </div>
                    `;
        case 'completed':
            return `
                         <div class="d-flex gap-2 justify-content-end flex-wrap">
                            <a href="/agendar_consulta" class="btn btn-azul" onclick="rescheduleConsultation(${consultation.id})">
                                <i class="bi bi-arrow-repeat me-2"></i>Agendar Novamente
                            </a>
                            <button class="btn btn-azul-claro" onclick="cancelConsultation(${consultation.id})">
                                <i class="bi  bi-calendar me-2"></i>Detalhes
                            </button>
                        </div>
                    `;
        case 'cancelled':
            return `
                        <div class="d-flex gap-2 justify-content-end flex-wrap">
                            <a href="/agendar_consulta" class="btn btn-azul" onclick="bookAgain(${consultation.id})">
                                <i class="bi bi-arrow-repeat me-2"></i>Agendar Novamente
                            </a>
                        </div>
                    `;
        default:
            return '';
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    if (date.toDateString() === today.toDateString()) {
        return 'Hoje';
    } else if (date.toDateString() === tomorrow.toDateString()) {
        return 'Amanhã';
    } else {
        return date.toLocaleDateString('pt-BR');
    }
}

function filterConsultations(status) {
    // Update active tab
    document.querySelectorAll('.filter-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    event.target.classList.add('active');

    currentFilter = status;
    applyFilters();
}

function searchConsultations() {
    applyFilters();
}

function filterBySpecialty() {
    applyFilters();
}

function filterByType() {
    applyFilters();
}

function applyFilters() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const specialtyFilter = document.getElementById('specialtyFilter').value;
    const typeFilter = document.getElementById('typeFilter').value;

    let filtered = [...consultations];

    // Filter by status
    if (currentFilter !== 'all') {
        filtered = filtered.filter(consultation => consultation.status === currentFilter);
    }

    // Filter by search term
    if (searchTerm) {
        filtered = filtered.filter(consultation =>
            consultation.doctor.toLowerCase().includes(searchTerm) ||
            consultation.specialty.toLowerCase().includes(searchTerm)
        );
    }

    // Filter by specialty
    if (specialtyFilter) {
        filtered = filtered.filter(consultation => consultation.specialty === specialtyFilter);
    }

    // Filter by type
    if (typeFilter) {
        filtered = filtered.filter(consultation => consultation.type === typeFilter);
    }

    filteredConsultations = filtered;
    renderConsultations(filtered);
}

function clearFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('specialtyFilter').value = '';
    document.getElementById('typeFilter').value = '';

    // Reset to 'all' tab
    document.querySelectorAll('.filter-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector('.filter-tab').classList.add('active');

    currentFilter = 'all';
    applyFilters();
}

function joinConsultation(consultationId) {
    const consultation = consultations.find(c => c.id === consultationId);
    if (consultation) {
        alert(`Entrando na consulta com ${consultation.doctor}...`);
        window.location.href = 'sala_consulta.html?consultation=' + consultationId;
    }
}

function rescheduleConsultation(consultationId) {
    const consultation = consultations.find(c => c.id === consultationId);
    if (consultation) {
        if (confirm(`Deseja reagendar a consulta com ${consultation.doctor}?`)) {
            alert('Redirecionando para reagendamento...');
            // In a real application, this would redirect to rescheduling page
        }
    }
}

function cancelConsultation(consultationId) {
    const consultation = consultations.find(c => c.id === consultationId);
    if (consultation) {
        if (confirm(`Deseja realmente cancelar a consulta com ${consultation.doctor}?`)) {
            // Update consultation status
            consultation.status = 'cancelled';
            alert('Consulta cancelada com sucesso.');
            applyFilters();
        }
    }
}

function viewDetails(consultationId) {
    const consultation = consultations.find(c => c.id === consultationId);
    if (consultation) {
        alert(`Mostrando detalhes da consulta com ${consultation.doctor}...`);
        // In a real application, this would show a modal with consultation details
    }
}

function bookAgain(consultationId) {
    const consultation = consultations.find(c => c.id === consultationId);
    if (consultation) {
        localStorage.setItem('selectedDoctor', JSON.stringify({
            name: consultation.doctor,
            specialty: consultation.specialty,
            rating: consultation.rating
        }));
        window.location.href = 'agendar_consulta.html';
    }
}

function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}

// Initialize page
document.addEventListener('DOMContentLoaded', function () {
    // Load appointments from localStorage if available
    const savedAppointments = JSON.parse(localStorage.getItem('appointments') || '[]');
    if (savedAppointments.length > 0) {
        // Add saved appointments to the list
        savedAppointments.forEach(appointment => {
            consultations.push({
                id: consultations.length + 1,
                doctor: appointment.doctor,
                specialty: appointment.specialty,
                date: appointment.date,
                time: appointment.time,
                type: appointment.type === 'video' ? 'Videochamada' : 'Chat',
                status: 'upcoming',
                price: `R$ ${appointment.price.toFixed(2).replace('.', ',')}`,
                avatar: appointment.doctor.split(' ').map(n => n[0]).join(''),
                rating: 4.8,
                prescription: false
            });
        });
    }

    renderConsultations(consultations);
});