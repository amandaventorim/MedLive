const doctors = [
    {
        id: 1,
        name: "Dr. Carlos Silva",
        specialty: "Cardiologia",
        rating: 4.8,
        reviews: 127,
        price: "R$ 150",
        availability: "Hoje às 14:00",
        crm: "CRM 12345",
        experience: "15 anos"
    },
    {
        id: 2,
        name: "Dra. Ana Santos",
        specialty: "Dermatologia",
        rating: 4.9,
        reviews: 89,
        price: "R$ 120",
        availability: "Amanhã às 09:00",
        crm: "CRM 67890",
        experience: "12 anos"
    },
    {
        id: 3,
        name: "Dr. Pedro Costa",
        specialty: "Clínica Geral",
        rating: 4.7,
        reviews: 203,
        price: "R$ 100",
        availability: "Hoje às 16:30",
        crm: "CRM 11111",
        experience: "20 anos"
    },
    {
        id: 4,
        name: "Dra. Maria Oliveira",
        specialty: "Pediatria",
        rating: 4.9,
        reviews: 156,
        price: "R$ 130",
        availability: "Amanhã às 10:00",
        crm: "CRM 22222",
        experience: "18 anos"
    },
    {
        id: 5,
        name: "Dra. Julia Ferreira",
        specialty: "Ginecologia",
        rating: 4.8,
        reviews: 94,
        price: "R$ 140",
        availability: "Hoje às 15:00",
        crm: "CRM 33333",
        experience: "14 anos"
    },
    {
        id: 6,
        name: "Dr. Roberto Lima",
        specialty: "Neurologia",
        rating: 4.6,
        reviews: 78,
        price: "R$ 180",
        availability: "Amanhã às 11:00",
        crm: "CRM 44444",
        experience: "22 anos"
    }
];

let filteredDoctors = [...doctors];

function renderDoctors(doctorsToRender) {
    const doctorsList = document.getElementById('doctorsList');
    const noResults = document.getElementById('noResults');

    if (doctorsToRender.length === 0) {
        doctorsList.innerHTML = '';
        noResults.style.display = 'block';
        return;
    }

    noResults.style.display = 'none';

    doctorsList.innerHTML = doctorsToRender.map(doctor => `
                <div class="col-lg-4 col-md-6">
                    <div class="doctor-card">
                        <div class="doctor-avatar">
                            ${doctor.name.split(' ').map(n => n[0]).join('')}
                        </div>
                        <h5 class="text-center fw-bold text-azul">${doctor.name}</h5>
                        <p class="text-center text-secondary mb-2">${doctor.specialty}</p>
                        <p class="text-center small text-muted mb-2">${doctor.crm} • ${doctor.experience}</p>
                        
                        <div class="text-center mb-3">
                            <div class="rating-stars">
                                ${'★'.repeat(Math.floor(doctor.rating))}${'☆'.repeat(5 - Math.floor(doctor.rating))}
                                <span class="text-muted">${doctor.rating} (${doctor.reviews} avaliações)</span>
                            </div>
                        </div>
                        
                        <div class="text-center mb-3">
                            <div class="fw-bold text-azul">${doctor.price}</div>
                            <small class="text-success">${doctor.availability}</small>
                        </div>
                        
                        <a href="/agendar_consulta" class="btn btn-agendar" onclick="scheduleAppointment(${doctor.id})">
                            <i class="bi bi-calendar-plus me-2"></i>Agendar Consulta
                        </a>
                    </div>
                </div>
            `).join('');
}

function searchDoctors() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const loadingSpinner = document.getElementById('loadingSpinner');

    loadingSpinner.style.display = 'block';

    setTimeout(() => {
        filteredDoctors = doctors.filter(doctor =>
            doctor.name.toLowerCase().includes(searchTerm) ||
            doctor.specialty.toLowerCase().includes(searchTerm)
        );

        applyFilters();
        loadingSpinner.style.display = 'none';
    }, 1000);
}

function filterBySpecialty(specialty) {
    document.getElementById('specialtyFilter').value = specialty;
    applyFilters();
}

function applyFilters() {
    const specialtyFilter = document.getElementById('specialtyFilter').value;
    const availabilityFilter = document.getElementById('availabilityFilter').value;
    const ratingFilter = document.getElementById('ratingFilter').value;

    let filtered = [...filteredDoctors];

    if (specialtyFilter) {
        filtered = filtered.filter(doctor => doctor.specialty === specialtyFilter);
    }

    if (availabilityFilter === 'hoje') {
        filtered = filtered.filter(doctor => doctor.availability.includes('Hoje'));
    }

    if (ratingFilter) {
        filtered = filtered.filter(doctor => doctor.rating >= parseFloat(ratingFilter));
    }

    renderDoctors(filtered);
}

function scheduleAppointment(doctorId) {
    const doctor = doctors.find(d => d.id === doctorId);
    if (doctor) {
        localStorage.setItem('selectedDoctor', JSON.stringify(doctor));
        window.location.href = '/agendar_consulta';
    }
}

function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}

// Event listeners
document.getElementById('searchInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        searchDoctors();
    }
});

document.getElementById('specialtyFilter').addEventListener('change', applyFilters);
document.getElementById('availabilityFilter').addEventListener('change', applyFilters);
document.getElementById('ratingFilter').addEventListener('change', applyFilters);

// Initialize page
document.addEventListener('DOMContentLoaded', function () {
    renderDoctors(doctors);
});