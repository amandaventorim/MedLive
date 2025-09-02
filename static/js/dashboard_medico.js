function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}

function startConsultation(patientId) {
    // Simulate starting a consultation
    alert('Iniciando consulta com o paciente...');
    // In a real application, this would redirect to the consultation room
    window.location.href = '/sala_consulta?patient=' + patientId;
}

// Update time every minute
function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit'
    });

    // Update any time displays if needed
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function () {
    updateTime();
    setInterval(updateTime, 60000); // Update every minute

    // Load doctor data if available
    const doctorData = JSON.parse(localStorage.getItem('doctorData') || '{}');
    if (doctorData.name) {
        // Update welcome message with doctor name
        const welcomeText = document.querySelector('.welcome-card h2');
        if (welcomeText) {
            welcomeText.textContent = `Bom dia, ${doctorData.name}! 👨‍⚕️`;
        }
    }

    // Simulate real-time updates
    setInterval(() => {
        // Update minutes remaining (simulate usage)
        const minutesElement = document.querySelector('.minutes-card h3');
        if (minutesElement) {
            let currentMinutes = parseInt(minutesElement.textContent);
            if (Math.random() > 0.95) { // 5% chance to decrease
                currentMinutes = Math.max(0, currentMinutes - 1);
                minutesElement.textContent = currentMinutes + ' min';

                // Update progress bar
                const progressBar = document.querySelector('.minutes-progress-bar');
                const percentage = (currentMinutes / 500) * 100;
                progressBar.style.width = percentage + '%';
            }
        }
    }, 30000); // Check every 30 seconds
});