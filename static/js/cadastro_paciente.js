let currentStep = 1;
let emailVerified = false;
let resendTimer = 0;
let resendInterval;

function showStep(step) {
    const steps = document.querySelectorAll(".step-form");
    steps.forEach((el, index) => {
        el.classList.remove("active");
    });
    
    // Map step numbers to step IDs
    const stepIds = ['step1', 'stepEmailVerification', 'step2', 'step3'];
    const targetStep = document.getElementById(stepIds[step - 1]);
    if (targetStep) {
        targetStep.classList.add("active");
    }
}

function nextStep() {
    if (currentStep === 1) {
        // Skip email verification step if email is already verified
        if (emailVerified) {
            currentStep = 3; // Go to step2 (which is now step 3 in our numbering)
        } else {
            currentStep = 2; // Go to email verification
        }
    } else if (currentStep === 2) {
        // From email verification to step2
        currentStep = 3;
    } else if (currentStep === 3) {
        // From step2 to step3
        currentStep = 4;
    }
    
    if (currentStep <= 4) {
        showStep(currentStep);
    }
}

function prevStep() {
    if (currentStep === 4) {
        // From step3 to step2
        currentStep = 3;
    } else if (currentStep === 3) {
        // From step2 to email verification or step1
        currentStep = emailVerified ? 1 : 2;
    } else if (currentStep === 2) {
        // From email verification to step1
        currentStep = 1;
    }
    
    if (currentStep >= 1) {
        showStep(currentStep);
    }
}

function sendEmailVerification() {
    const email = document.getElementById('email').value;
    
    if (!email) {
        showAlert('Por favor, digite um email válido.', 'danger');
        return;
    }
    
    if (!isValidEmail(email)) {
        showAlert('Por favor, digite um email válido.', 'danger');
        return;
    }
    
    // Show loading
    const btn = event.target;
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enviando...';
    btn.disabled = true;
    
    // Simulate API call to send verification email
    setTimeout(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
        
        // Update email display
        document.getElementById('emailDisplay').textContent = email;
        
        // Go to email verification step
        currentStep = 2;
        showStep(currentStep);
        
        // Start resend timer
        startResendTimer();
        
        showAlert('Código de verificação enviado para seu email!', 'success');
    }, 2000);
}

function verifyEmailCode() {
    const code = document.getElementById('verificationCode').value;
    
    if (!code || code.length !== 6) {
        showAlert('Por favor, digite um código de 6 dígitos.', 'danger');
        return;
    }
    
    // Show loading
    const btn = event.target;
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Verificando...';
    btn.disabled = true;
    
    // Simulate API call to verify code
    setTimeout(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
        
        // For demo purposes, accept any 6-digit code
        // In real implementation, validate with backend
        if (code.match(/^\d{6}$/)) {
            emailVerified = true;
            clearInterval(resendInterval);
            showAlert('Email verificado com sucesso!', 'success');
            
            // Continue to next step
            setTimeout(() => {
                nextStep();
            }, 1000);
        } else {
            showAlert('Código inválido. Tente novamente.', 'danger');
        }
    }, 1500);
}

function resendEmailCode() {
    if (resendTimer > 0) return;
    
    const btn = document.getElementById('resendEmailBtn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Reenviando...';
    btn.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
        
        showAlert('Código reenviado com sucesso!', 'success');
        startResendTimer();
        
        // Clear the verification code input
        document.getElementById('verificationCode').value = '';
    }, 1500);
}

function goBackToEmailEdit() {
    // Reset email verification status
    emailVerified = false;
    clearInterval(resendInterval);
    
    // Go back to step 1
    currentStep = 1;
    showStep(currentStep);
    
    // Clear verification code
    document.getElementById('verificationCode').value = '';
}

function startResendTimer() {
    resendTimer = 60;
    const resendBtn = document.getElementById('resendEmailBtn');
    
    resendInterval = setInterval(() => {
        resendTimer--;
        if (resendTimer > 0) {
            resendBtn.innerHTML = `<i class="fas fa-redo me-2"></i>Reenviar (${resendTimer}s)`;
            resendBtn.disabled = true;
        } else {
            resendBtn.innerHTML = '<i class="fas fa-redo me-2"></i>Reenviar';
            resendBtn.disabled = false;
            clearInterval(resendInterval);
        }
    }, 1000);
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showAlert(message, type) {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert-custom');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-custom mt-3`;
    alert.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>${message}`;
    
    // Add to active form
    const activeForm = document.querySelector('.step-form.active');
    if (activeForm) {
        activeForm.appendChild(alert);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
}

// Form validation before submission
document.getElementById('multiStepForm').addEventListener('submit', function(e) {
    if (!emailVerified) {
        e.preventDefault();
        showAlert('Por favor, verifique seu email antes de continuar.', 'warning');
        return false;
    }
});

// Auto-format verification code input
document.addEventListener('DOMContentLoaded', function() {
    const verificationCodeInput = document.getElementById('verificationCode');
    
    if (verificationCodeInput) {
        // Only allow numbers
        verificationCodeInput.addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '');
            
            // Auto-verify when 6 digits are entered
            if (this.value.length === 6) {
                setTimeout(() => {
                    verifyEmailCode();
                }, 500);
            }
        });
        
        // Prevent paste of non-numeric content
        verificationCodeInput.addEventListener('paste', function(e) {
            e.preventDefault();
            const paste = (e.clipboardData || window.clipboardData).getData('text');
            const numericPaste = paste.replace(/[^0-9]/g, '').substring(0, 6);
            this.value = numericPaste;
            
            if (numericPaste.length === 6) {
                setTimeout(() => {
                    verifyEmailCode();
                }, 500);
            }
        });
    }
});