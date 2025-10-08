let currentStep = 1;

function showStep(step) {
    const steps = document.querySelectorAll(".step-form");
    steps.forEach((el, index) => {
        if (index === step - 1) {
            el.classList.add("active");
            el.style.display = "block";
        } else {
            el.classList.remove("active");
            el.style.display = "none";
        }
    });
}

// ====== FUNÇÕES DE VALIDAÇÃO ======

function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]/g, '');
    if (cpf.length !== 11) return false;
    if (/^(\d)\1{10}$/.test(cpf)) return false;
    
    let soma = 0;
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let resto = 11 - (soma % 11);
    let dv1 = (resto < 2) ? 0 : resto;
    
    soma = 0;
    for (let i = 0; i < 10; i++) {
        soma += parseInt(cpf.charAt(i)) * (11 - i);
    }
    resto = 11 - (soma % 11);
    let dv2 = (resto < 2) ? 0 : resto;
    
    return (parseInt(cpf.charAt(9)) === dv1 && parseInt(cpf.charAt(10)) === dv2);
}

function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function validarNome(nome) {
    return nome && nome.trim().length >= 2 && nome.trim().includes(' ');
}

function mostrarErro(campo, mensagem) {
    const erroAnterior = campo.parentNode.querySelector('.error-message');
    if (erroAnterior) {
        erroAnterior.remove();
    }
    
    campo.classList.remove('is-valid');
    campo.classList.add('is-invalid');
    
    const erro = document.createElement('div');
    erro.className = 'error-message text-danger small mt-1';
    erro.textContent = mensagem;
    
    campo.parentNode.appendChild(erro);
}

function limparErro(campo) {
    campo.classList.remove('is-invalid');
    campo.classList.add('is-valid');
    const erro = campo.parentNode.querySelector('.error-message');
    if (erro) {
        erro.remove();
    }
}

function validarEtapa1() {
    let valido = true;
    
    const nome = document.getElementById('nome');
    if (!validarNome(nome.value)) {
        mostrarErro(nome, 'Digite o nome completo');
        valido = false;
    } else {
        limparErro(nome);
    }
    
    const email = document.getElementById('email');
    if (!validarEmail(email.value)) {
        mostrarErro(email, 'Digite um email válido');
        valido = false;
    } else {
        limparErro(email);
    }
    
    return valido;
}

function validarEtapa2() {
    let valido = true;
    
    const cpf = document.getElementById('cpf');
    if (!validarCPF(cpf.value)) {
        mostrarErro(cpf, 'CPF inválido');
        valido = false;
    } else {
        limparErro(cpf);
    }
    
    return valido;
}

function nextStep() {
    let podeAvancar = false;
    
    if (currentStep === 1) {
        podeAvancar = validarEtapa1();
    } else if (currentStep === 2) {
        podeAvancar = validarEtapa2();
    }
    
    if (podeAvancar && currentStep < 3) {
        currentStep++;
        showStep(currentStep);
    }
}

function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
    }
}

// Validação em tempo real
document.addEventListener('DOMContentLoaded', function() {
    const cpfInput = document.getElementById('cpf');
    if (cpfInput) {
        cpfInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            e.target.value = value;
        });
        
        cpfInput.addEventListener('blur', function() {
            if (this.value && !validarCPF(this.value)) {
                mostrarErro(this, 'CPF inválido');
            } else if (this.value) {
                limparErro(this);
            }
        });
    }
    
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            if (this.value && !validarEmail(this.value)) {
                mostrarErro(this, 'Email inválido');
            } else if (this.value) {
                limparErro(this);
            }
        });
    }
    
    const nomeInput = document.getElementById('nome');
    if (nomeInput) {
        nomeInput.addEventListener('blur', function() {
            if (!validarNome(this.value)) {
                mostrarErro(this, 'Digite o nome completo');
            } else {
                limparErro(this);
            }
        });
    }
});