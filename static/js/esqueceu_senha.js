let currentStep = 1;
let userEmail = '';
let resendTimer = 0;
let resendInterval;

function showStep(stepNumber) {
    // Hide all steps
    document.querySelectorAll('.step-form').forEach(form => {
        form.classList.remove('active');
    });

    // Show current step
    const stepForms = ['', 'emailStep', 'codeStep', 'passwordStep', 'successStep'];
    document.getElementById(stepForms[stepNumber]).classList.add('active');

    // Update step indicators
    document.querySelectorAll('.step').forEach((step, index) => {
        step.classList.remove('active', 'completed');
        if (index + 1 < stepNumber) {
            step.classList.add('completed');
        } else if (index + 1 === stepNumber) {
            step.classList.add('active');
        }
    });

    currentStep = stepNumber;
}

function handleEmailSubmit(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    userEmail = email;

    // Simulate API call
    showLoading('Enviando código...');

    setTimeout(() => {
        hideLoading();
        document.getElementById('emailDisplay').textContent = `Código enviado para: ${email}`;
        showStep(2);
        startResendTimer();
    }, 2000);
}

function handleCodeSubmit(event) {
    event.preventDefault();

    const code = document.getElementById('verificationCode').value;

    if (code.length !== 6) {
        showAlert('Por favor, digite um código de 6 dígitos.', 'danger');
        return;
    }

    // Simulate API call
    showLoading('Verificando código...');

    setTimeout(() => {
        hideLoading();
        // Simulate successful verification (in real app, validate with backend)
        if (code === '123456' || true) { // Always true for demo
            showStep(3);
        } else {
            showAlert('Código inválido. Tente novamente.', 'danger');
        }
    }, 1500);
}

function handlePasswordSubmit(event) {
    event.preventDefault();

    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (newPassword !== confirmPassword) {
        showAlert('As senhas não coincidem.', 'danger');
        return;
    }

    if (newPassword.length < 8) {
        showAlert('A senha deve ter pelo menos 8 caracteres.', 'danger');
        return;
    }

    // Simulate API call
    showLoading('Alterando senha...');

    setTimeout(() => {
        hideLoading();
        showStep(4);
    }, 2000);
}

function resendCode() {
    if (resendTimer > 0) return;

    showLoading('Reenviando código...');

    setTimeout(() => {
        hideLoading();
        showAlert('Código reenviado com sucesso!', 'success');
        startResendTimer();
    }, 1500);
}

function startResendTimer() {
    resendTimer = 60;
    const resendBtn = document.getElementById('resendBtn');

    resendInterval = setInterval(() => {
        resendTimer--;
        if (resendTimer > 0) {
            resendBtn.innerHTML = `<i class="fas fa-redo me-2"></i>Reenviar código (${resendTimer}s)`;
            resendBtn.disabled = true;
        } else {
            resendBtn.innerHTML = '<i class="fas fa-redo me-2"></i>Reenviar código';
            resendBtn.disabled = false;
            clearInterval(resendInterval);
        }
    }, 1000);
}

function goBackToEmail() {
    showStep(1);
    clearInterval(resendInterval);
}

function goBackToCode() {
    showStep(2);
    startResendTimer();
}

function showLoading(message) {
    // Simple loading simulation
    const forms = document.querySelectorAll('.step-form.active form');
    forms.forEach(form => {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${message}`;
            submitBtn.disabled = true;
        }
    });
}

function hideLoading() {
    const forms = document.querySelectorAll('.step-form form');
    forms.forEach(form => {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = false;
            // Restore original text based on form
            if (form.id === 'emailForm') {
                submitBtn.innerHTML = '<i class="fas fa-paper-plane me-2"></i>Enviar código';
            } else if (form.id === 'codeForm') {
                submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Verificar código';
            } else if (form.id === 'passwordForm') {
                submitBtn.innerHTML = '<i class="fas fa-save me-2"></i>Alterar senha';
            }
        }
    });
}

function showAlert(message, type) {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());

    // Create new alert
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} mt-3`;
    alert.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>${message}`;

    // Add to active form
    const activeForm = document.querySelector('.step-form.active');
    activeForm.appendChild(alert);

    // Auto remove after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// Initialize page
document.addEventListener('DOMContentLoaded', function () {
    showStep(1);
});