
let doctors = [];
let filteredDoctors = [];

async function fetchDoctors() {
    const loadingSpinner = document.getElementById('loadingSpinner');
    loadingSpinner.style.display = 'block';
    try {
        const response = await fetch('/api/medicos');
        doctors = await response.json();
        console.log('Médicos recebidos da API:', doctors);
        filteredDoctors = [...doctors];
        renderDoctors(doctors);
    } catch (error) {
        console.error('Erro ao buscar médicos:', error);
    } finally {
        loadingSpinner.style.display = 'none';
    }
}

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
                            ${doctor.foto 
                                ? `<img src="${doctor.foto}" alt="${doctor.name}" class="doctor-photo">` 
                                : doctor.name.split(' ').map(n => n[0]).join('')
                            }
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
                        
                        <a href="/agendar_consulta?idMedico=${doctor.id}" class="btn btn-agendar" onclick="scheduleAppointment(${doctor.id})">
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
        window.location.href = `/agendar_consulta?idMedico=${doctorId}`;
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
    aplicarIconesEspecialidades();
    fetchDoctors();
});

// Função para mapear especialidades para ícones
function getIconeEspecialidade(nomeEspecialidade) {
    const iconMap = {
        'cardiologia': 'bi-heart-pulse',
        'dermatologia': 'bi-person-check',
        'ortopedia': 'bi-bandaid',
        'pediatria': 'bi-emoji-smile',
        'ginecologia': 'bi-gender-female',
        'oftalmologia': 'bi-eye',
        'psiquiatria': 'bi-brain',
        'neurologia': 'bi-activity',
        'endocrinologia': 'bi-droplet',
        'urologia': 'bi-clipboard-pulse',
        'otorrinolaringologia': 'bi-headphones',
        'gastroenterologia': 'bi-virus',
        'pneumologia': 'bi-wind',
        'reumatologia': 'bi-person-wheelchair',
        'nefrologia': 'bi-diagram-3',
        'oncologia': 'bi-shield-plus',
        'hematologia': 'bi-heart',
        'infectologia': 'bi-shield-check',
        'geriatria': 'bi-person-walking',
        'anestesiologia': 'bi-capsule',
        'radiologia': 'bi-radioactive',
        'patologia': 'bi-clipboard-data',
        'medicina de emergência': 'bi-hospital',
        'medicina do trabalho': 'bi-briefcase',
        'medicina esportiva': 'bi-lightning',
        'nutrologia': 'bi-egg-fried',
        'cirurgia geral': 'bi-scissors',
        'clínica geral': 'bi-clipboard-heart'
    };
    const nome = nomeEspecialidade.toLowerCase().trim();
    return iconMap[nome] || 'bi-heart-pulse';
}

// Função para aplicar ícones às especialidades
function aplicarIconesEspecialidades() {
    const icones = document.querySelectorAll('.esp-icon-busca');
    icones.forEach(icone => {
        const especialidade = icone.getAttribute('data-especialidade');
        if (especialidade) {
            const iconeClass = getIconeEspecialidade(especialidade);
            icone.classList.add(iconeClass);
        }
    });
}
