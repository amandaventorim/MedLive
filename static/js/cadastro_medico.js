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

// Função para validar CPF
function validarCPF(cpf) {
    // Remove caracteres não numéricos
    cpf = cpf.replace(/[^\d]/g, '');
    
    // Verifica se tem 11 dígitos
    if (cpf.length !== 11) {
        return false;
    }
    
    // Verifica se todos os dígitos são iguais
    if (/^(\d)\1{10}$/.test(cpf)) {
        return false;
    }
    
    // Calcula o primeiro dígito verificador
    let soma = 0;
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let resto = 11 - (soma % 11);
    let dv1 = (resto < 2) ? 0 : resto;
    
    // Calcula o segundo dígito verificador
    soma = 0;
    for (let i = 0; i < 10; i++) {
        soma += parseInt(cpf.charAt(i)) * (11 - i);
    }
    resto = 11 - (soma % 11);
    let dv2 = (resto < 2) ? 0 : resto;
    
    // Verifica se os dígitos verificadores estão corretos
    return (parseInt(cpf.charAt(9)) === dv1 && parseInt(cpf.charAt(10)) === dv2);
}

// Função para validar email
function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Função para validar se é maior de idade
function validarIdade(dataNascimento) {
    const hoje = new Date();
    const nascimento = new Date(dataNascimento);
    let idade = hoje.getFullYear() - nascimento.getFullYear();
    const diferenca = hoje.getMonth() - nascimento.getMonth();
    
    if (diferenca < 0 || (diferenca === 0 && hoje.getDate() < nascimento.getDate())) {
        idade--;
    }
    
    return idade >= 18;
}

// Função para mostrar erro
function mostrarErro(campo, mensagem) {
    // Remove erro anterior se existir
    const erroAnterior = campo.parentNode.querySelector('.error-message');
    if (erroAnterior) {
        erroAnterior.remove();
    }
    
    // Adiciona classe de erro
    campo.classList.remove('is-valid');
    campo.classList.add('is-invalid');
    
    // Cria elemento de erro
    const erro = document.createElement('div');
    erro.className = 'error-message text-danger small mt-1';
    erro.textContent = mensagem;
    
    // Insere após o campo
    campo.parentNode.appendChild(erro);
}

// Função para limpar erro e mostrar sucesso
function limparErro(campo) {
    campo.classList.remove('is-invalid');
    campo.classList.add('is-valid');
    const erro = campo.parentNode.querySelector('.error-message');
    if (erro) {
        erro.remove();
    }
}

// Função para validar etapa 1
function validarEtapa1() {
    let valido = true;
    
    // Validar nome
    const nome = document.getElementById('nome');
    if (nome.value.trim().length < 2) {
        mostrarErro(nome, 'Nome deve ter pelo menos 2 caracteres');
        valido = false;
    } else {
        limparErro(nome);
    }
    
    // Validar email
    const email = document.getElementById('email');
    if (!validarEmail(email.value)) {
        mostrarErro(email, 'Digite um email válido');
        valido = false;
    } else {
        limparErro(email);
    }
    
    // Validar data de nascimento
    const dataNasc = document.getElementById('nasc');
    if (!dataNasc.value) {
        mostrarErro(dataNasc, 'Data de nascimento é obrigatória');
        valido = false;
    } else if (!validarIdade(dataNasc.value)) {
        mostrarErro(dataNasc, 'Você deve ter pelo menos 18 anos');
        valido = false;
    } else {
        limparErro(dataNasc);
    }
    
    // Validar gênero
    const genero = document.getElementById('genero');
    if (!genero.value) {
        mostrarErro(genero, 'Selecione um gênero');
        valido = false;
    } else {
        limparErro(genero);
    }
    
    return valido;
}

// Função para validar etapa 2
function validarEtapa2() {
    let valido = true;
    
    // Validar CPF
    const cpf = document.getElementById('cpf');
    if (!validarCPF(cpf.value)) {
        mostrarErro(cpf, 'CPF inválido. Verifique os números digitados');
        valido = false;
    } else {
        limparErro(cpf);
    }
    
    // Validar senha
    const senha = document.getElementById('senha');
    if (senha.value.length < 6) {
        mostrarErro(senha, 'Senha deve ter pelo menos 6 caracteres');
        valido = false;
    } else {
        limparErro(senha);
    }
    
    // Validar confirmação de senha
    const confiSenha = document.getElementById('confisenha');
    if (senha.value !== confiSenha.value) {
        mostrarErro(confiSenha, 'Senhas não coincidem');
        valido = false;
    } else {
        limparErro(confiSenha);
    }
    
    return valido;
}

// Função para validar etapa 3
function validarEtapa3() {
    let valido = true;
    
    // Validar CRM
    const crm = document.getElementById('crm');
    if (crm.value.trim().length < 4) {
        mostrarErro(crm, 'CRM deve ter pelo menos 4 caracteres');
        valido = false;
    } else {
        limparErro(crm);
    }
    
    // Validar status profissional
    const status = document.getElementById('statusprofissional');
    if (!status.value) {
        mostrarErro(status, 'Selecione um status profissional');
        valido = false;
    } else {
        limparErro(status);
    }
    
    return valido;
}

function nextStep() {
    let podeAvancar = false;
    
    // Validar etapa atual antes de avançar
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

// Validação em tempo real para todos os campos
document.addEventListener('DOMContentLoaded', function() {
    // === CPF ===
    const cpfInput = document.getElementById('cpf');
    if (cpfInput) {
        // Máscara para CPF
        cpfInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            e.target.value = value;
        });
        
        // Validação em tempo real
        cpfInput.addEventListener('blur', function() {
            if (this.value && !validarCPF(this.value)) {
                mostrarErro(this, 'CPF inválido');
            } else if (this.value) {
                limparErro(this);
            }
        });
    }
    
    // === EMAIL ===
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
    
    // === NOME ===
    const nomeInput = document.getElementById('nome');
    if (nomeInput) {
        nomeInput.addEventListener('blur', function() {
            if (this.value.trim().length < 2) {
                mostrarErro(this, 'Nome deve ter pelo menos 2 caracteres');
            } else if (!this.value.trim().includes(' ')) {
                mostrarErro(this, 'Digite o nome completo');
            } else {
                limparErro(this);
            }
        });
    }
    
    // === DATA DE NASCIMENTO ===
    const nascInput = document.getElementById('nasc');
    if (nascInput) {
        nascInput.addEventListener('change', function() {
            if (!this.value) {
                mostrarErro(this, 'Data de nascimento é obrigatória');
            } else if (!validarIdade(this.value)) {
                mostrarErro(this, 'Você deve ter pelo menos 18 anos');
            } else {
                limparErro(this);
            }
        });
    }
    
    // === SENHA ===
    const senhaInput = document.getElementById('senha');
    if (senhaInput) {
        senhaInput.addEventListener('input', function() {
            if (this.value.length < 6) {
                mostrarErro(this, 'Senha deve ter pelo menos 6 caracteres');
            } else {
                limparErro(this);
            }
        });
    }
    
    // === CONFIRMAR SENHA ===
    const confiSenhaInput = document.getElementById('confisenha');
    if (confiSenhaInput) {
        confiSenhaInput.addEventListener('input', function() {
            const senha = document.getElementById('senha').value;
            if (this.value && this.value !== senha) {
                mostrarErro(this, 'Senhas não coincidem');
            } else if (this.value) {
                limparErro(this);
            }
        });
    }
    
    // === CRM ===
    const crmInput = document.getElementById('crm');
    if (crmInput) {
        crmInput.addEventListener('blur', function() {
            if (this.value.trim().length < 4) {
                mostrarErro(this, 'CRM deve ter pelo menos 4 caracteres');
            } else {
                limparErro(this);
            }
        });
    }
    
    // === GÊNERO ===
    const generoSelect = document.getElementById('genero');
    if (generoSelect) {
        generoSelect.addEventListener('change', function() {
            if (!this.value) {
                mostrarErro(this, 'Selecione um gênero');
            } else {
                limparErro(this);
            }
        });
    }
    
    // === STATUS PROFISSIONAL ===
    const statusSelect = document.getElementById('statusprofissional');
    if (statusSelect) {
        statusSelect.addEventListener('change', function() {
            if (!this.value) {
                mostrarErro(this, 'Selecione um status profissional');
            } else {
                limparErro(this);
            }
        });
    }
});