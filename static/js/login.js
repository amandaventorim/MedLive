let selectedUserType = 'paciente';

function selectUserType(type) {
    selectedUserType = type;

    // Update active button
    document.querySelectorAll('.user-type-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Simple validation (in a real app, this would be handled by the backend)
    if (email && password) {
        // Store user info in localStorage for demo purposes
        localStorage.setItem('userType', selectedUserType);
        localStorage.setItem('userEmail', email);

        // Redirect based on user type
        if (selectedUserType === 'medico') {
            window.location.href = '/dashboard_medico';
        } else {
            window.location.href = '/dashboard_paciente';
        }
    } else {
        alert('Por favor, preencha todos os campos.');
    }
}



