let currentStep = 1;

function showStep(step) {
    // Ocultar todas as etapas
    const allSteps = document.querySelectorAll(".step-form");
    allSteps.forEach(el => {
        el.classList.remove("active");
        el.style.display = "none";
    });
    
    // Mostrar a etapa correta baseada no número
    let targetStepId;
    if (step === 1) {
        targetStepId = "step1";
    } else if (step === 2) {
        targetStepId = "step2";
    } else if (step === 3) {
        targetStepId = "step3";
    }
    
    if (targetStepId) {
        const targetStep = document.getElementById(targetStepId);
        if (targetStep) {
            targetStep.classList.add("active");
            targetStep.style.display = "block";
        }
    }
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

function validarSenha(senha) {
    // Verifica se a senha existe
    if (!senha || senha.trim() === '') {
        return { valido: false, mensagem: 'Senha é obrigatória' };
    }
    
    // Verifica se a senha tem pelo menos 6 caracteres
    if (senha.length < 6) {
        return { valido: false, mensagem: 'A senha deve ter pelo menos 6 caracteres' };
    }
    
    // Verifica se a senha não excede 128 caracteres
    if (senha.length > 128) {
        return { valido: false, mensagem: 'A senha deve ter no máximo 128 caracteres' };
    }
    
    return { valido: true, mensagem: '' };
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
    if (!nome) {
        return false;
    }
    if (!validarNome(nome.value)) {
        mostrarErro(nome, 'Digite o nome completo (nome e sobrenome)');
        valido = false;
    } else {
        limparErro(nome);
    }
    
    const email = document.getElementById('email');
    if (!email) {
        return false;
    }
    if (!validarEmail(email.value)) {
        mostrarErro(email, 'Digite um email válido');
        valido = false;
    } else {
        limparErro(email);
    }
    
    const cpf = document.getElementById('cpf');
    if (!cpf) {
        return false;
    }
    if (!validarCPF(cpf.value)) {
        mostrarErro(cpf, 'Digite um CPF válido');
        valido = false;
    } else {
        limparErro(cpf);
    }
    
    const senha = document.getElementById('senha');
    if (!senha) {
        return false;
    }
    const resultadoSenha = validarSenha(senha.value);
    if (!resultadoSenha.valido) {
        mostrarErro(senha, resultadoSenha.mensagem);
        valido = false;
    } else {
        limparErro(senha);
    }
    
    return valido;
}

function validarEtapa2() {
    let valido = true;
    
    const genero = document.getElementById('genero');
    if (!genero || !genero.value) {
        mostrarErro(genero, 'Selecione o gênero');
        valido = false;
    } else {
        limparErro(genero);
    }
    
    const dataNasc = document.getElementById('nasc');
    if (!dataNasc || !dataNasc.value) {
        mostrarErro(dataNasc, 'Selecione a data de nascimento');
        valido = false;
    } else {
        limparErro(dataNasc);
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
    
    const senhaInput = document.getElementById('senha');
    if (senhaInput) {
        senhaInput.addEventListener('blur', function() {
            const resultado = validarSenha(this.value);
            if (!resultado.valido) {
                mostrarErro(this, resultado.mensagem);
            } else {
                limparErro(this);
            }
        });
        
        // Validação em tempo real - só mostra erro se a senha for muito longa
        senhaInput.addEventListener('input', function() {
            const resultado = validarSenha(this.value);
            // Só mostra erro imediatamente se a senha exceder o limite máximo
            if (this.value && this.value.length > 128) {
                mostrarErro(this, 'A senha deve ter no máximo 128 caracteres');
            } else if (this.value && resultado.valido) {
                limparErro(this);
            }
        });
    }
});

// Funções temporárias para a etapa de verificação de email (não implementadas)
function goBackToEmailEdit() {
    console.log('goBackToEmailEdit não implementada');
    // Por enquanto, volta para a etapa 1
    currentStep = 1;
    showStep(currentStep);
}

function resendEmailCode() {
    console.log('resendEmailCode não implementada');
    // Placeholder para reenvio de código
}

function verifyEmailCode() {
    console.log('verifyEmailCode não implementada');
    // Por enquanto, avança para a próxima etapa
    currentStep = 2;
    showStep(currentStep);
}