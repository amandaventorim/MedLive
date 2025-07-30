function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    const toggleButton = document.querySelector('.navbar-toggler');

    if (navbarNav.classList.contains('show')) {
        navbarNav.classList.remove('show');
        toggleButton.setAttribute('aria-expanded', 'false');
    } else {
        navbarNav.classList.add('show');
        toggleButton.setAttribute('aria-expanded', 'true');
    }
}
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        const navbarNav = document.getElementById('navbarNav');
        const toggleButton = document.querySelector('.navbar-toggler');
        if (navbarNav.classList.contains('show')) {
            navbarNav.classList.remove('show');
            toggleButton.setAttribute('aria-expanded', 'false');
        }
    });
});
window.addEventListener('resize', () => {
    if (window.innerWidth >= 992) {
        const navbarNav = document.getElementById('navbarNav');
        const toggleButton = document.querySelector('.navbar-toggler');
        navbarNav.classList.remove('show');
        toggleButton.setAttribute('aria-expanded', 'false');
    }
});