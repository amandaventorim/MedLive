function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
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

    // Load user data if available
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    if (userData.name) {
        // Update welcome message with user name
        const welcomeText = document.querySelector('.welcome-card h2');
        if (welcomeText) {
            welcomeText.textContent = `Bem-vindo de volta, ${userData.name}! 👋`;
        }
    }

    // Load appointments from localStorage
    const appointments = JSON.parse(localStorage.getItem('appointments') || '[]');
    if (appointments.length > 0) {
        // Update appointment count
        const appointmentCount = document.querySelector('.stats-card .stats-icon.success + h3');
        if (appointmentCount) {
            appointmentCount.textContent = appointments.length;
        }
    }
});