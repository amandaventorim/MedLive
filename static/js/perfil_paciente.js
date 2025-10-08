function editarSecao(secao) {
    console.log('Editando seção:', secao);
    // Aqui você pode implementar a lógica de edição inline
}

function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}


// Adicionar funcionalidade aos botões de ação rápida
document.querySelectorAll('.botao-medlive, .botao-secundario').forEach(botao => {
    botao.addEventListener('click', function () {
        if (!this.hasAttribute('data-bs-toggle')) {
            console.log('Ação:', this.textContent.trim());
        }
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);

    if (urlParams.get('foto_sucesso') === '1') {
        // Limpar parâmetro da URL sem mostrar mensagem
        window.history.replaceState({}, document.title, window.location.pathname);
    }

    if (urlParams.get('erro') === 'tipo_invalido') {
        alert('Erro: Tipo de arquivo não permitido. Use apenas JPG, PNG ou WEBP.');
        window.history.replaceState({}, document.title, window.location.pathname);
    }

    if (urlParams.get('erro') === 'arquivo_muito_grande') {
        alert('Erro: Arquivo muito grande. Tamanho máximo: 5MB.');
        window.history.replaceState({}, document.title, window.location.pathname);
    }

    if (urlParams.get('erro') === 'upload_falhou') {
        alert('Erro: Falha no upload. Tente novamente.');
        window.history.replaceState({}, document.title, window.location.pathname);
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const fotoInput = document.getElementById('foto');
    const fotoPreview = document.querySelector('#modalEditarFoto .foto-usuario');

    if (fotoInput && fotoPreview) {
        fotoInput.addEventListener('change', function (e) {
            const file = e.target.files[0];

            if (file) {
                // Verificar se é uma imagem
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();

                    reader.onload = function (e) {
                        // Atualizar preview no modal
                        fotoPreview.src = e.target.result;
                    };

                    reader.readAsDataURL(file);
                } else {
                    alert('Por favor, selecione apenas arquivos de imagem.');
                    fotoInput.value = '';
                }
            }
        });
    }
});

// ========== FUNCIONALIDADE DE ALTERAÇÃO DE SENHA ==========

document.addEventListener('DOMContentLoaded', function() {
    const btnAlterarSenha = document.getElementById('btnAlterarSenha');
    const formAlterarSenha = document.getElementById('formAlterarSenha');
    const modalAlterarSenha = document.getElementById('modalAlterarSenha');
    
    // Função para limpar mensagens de erro
    function limparErros() {
        document.querySelectorAll('.text-danger, .alert-danger, .alert-success').forEach(el => {
            el.style.display = 'none';
            el.textContent = '';
        });
        
        // Remover classes de erro dos campos
        document.querySelectorAll('.is-invalid').forEach(el => {
            el.classList.remove('is-invalid');
        });
    }
    
    // Função para mostrar erro em campo específico
    function mostrarErro(campoId, mensagem) {
        const campo = document.getElementById(campoId);
        const erro = document.getElementById(`erro${campoId.charAt(0).toUpperCase() + campoId.slice(1)}`);
        
        if (campo && erro) {
            campo.classList.add('is-invalid');
            erro.textContent = mensagem;
            erro.style.display = 'block';
        }
    }
    
    // Função para mostrar erro geral
    function mostrarErroGeral(mensagem) {
        const erroGeral = document.getElementById('erroGeral');
        if (erroGeral) {
            erroGeral.textContent = mensagem;
            erroGeral.style.display = 'block';
        }
    }
    
    // Função para mostrar sucesso
    function mostrarSucesso(mensagem) {
        const sucessoSenha = document.getElementById('sucessoSenha');
        if (sucessoSenha) {
            sucessoSenha.textContent = mensagem;
            sucessoSenha.style.display = 'block';
        }
    }
    
    // Validação em tempo real
    document.getElementById('novaSenha').addEventListener('input', function() {
        const senha = this.value;
        if (senha.length > 0 && senha.length < 6) {
            mostrarErro('novaSenha', 'Senha deve ter pelo menos 6 caracteres');
        } else {
            document.getElementById('erroNovaSenha').style.display = 'none';
            this.classList.remove('is-invalid');
        }
    });
    
    document.getElementById('confirmarSenha').addEventListener('input', function() {
        const novaSenha = document.getElementById('novaSenha').value;
        const confirmarSenha = this.value;
        
        if (confirmarSenha.length > 0 && novaSenha !== confirmarSenha) {
            mostrarErro('confirmarSenha', 'As senhas não coincidem');
        } else {
            document.getElementById('erroConfirmarSenha').style.display = 'none';
            this.classList.remove('is-invalid');
        }
    });
    
    // Limpar erros quando modal é aberto
    modalAlterarSenha.addEventListener('show.bs.modal', function() {
        limparErros();
        formAlterarSenha.reset();
    });
    
    // Evento de clique no botão alterar senha
    btnAlterarSenha.addEventListener('click', async function() {
        limparErros();
        
        // Obter valores dos campos
        const senhaAtual = document.getElementById('senhaAtual').value.trim();
        const novaSenha = document.getElementById('novaSenha').value.trim();
        const confirmarSenha = document.getElementById('confirmarSenha').value.trim();
        
        // Validações client-side
        let hasError = false;
        
        if (!senhaAtual) {
            mostrarErro('senhaAtual', 'Campo obrigatório');
            hasError = true;
        }
        
        if (!novaSenha) {
            mostrarErro('novaSenha', 'Campo obrigatório');
            hasError = true;
        } else if (novaSenha.length < 6) {
            mostrarErro('novaSenha', 'Senha deve ter pelo menos 6 caracteres');
            hasError = true;
        }
        
        if (!confirmarSenha) {
            mostrarErro('confirmarSenha', 'Campo obrigatório');
            hasError = true;
        } else if (novaSenha !== confirmarSenha) {
            mostrarErro('confirmarSenha', 'As senhas não coincidem');
            hasError = true;
        }
        
        if (hasError) return;
        
        // Mostrar loading
        const btnText = this.querySelector('.btn-text');
        const spinner = this.querySelector('.spinner-border');
        btnText.textContent = 'Alterando...';
        spinner.classList.remove('d-none');
        this.disabled = true;
        
        try {
            // Preparar dados do formulário
            const formData = new FormData();
            formData.append('senha_atual', senhaAtual);
            formData.append('nova_senha', novaSenha);
            formData.append('confirmar_senha', confirmarSenha);
            
            // Enviar requisição
            const response = await fetch('/alterar_senha', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.sucesso) {
                mostrarSucesso(result.mensagem);
                
                // Fechar modal após 2 segundos
                setTimeout(() => {
                    const modal = bootstrap.Modal.getInstance(modalAlterarSenha);
                    modal.hide();
                    
                    // Mostrar notificação de sucesso na página
                    alert('Senha alterada com sucesso!');
                }, 2000);
                
            } else {
                // Verificar tipo de erro
                if (result.erro.includes('atual incorreta')) {
                    mostrarErro('senhaAtual', result.erro);
                } else if (result.erro.includes('não coincidem')) {
                    mostrarErro('confirmarSenha', result.erro);
                } else if (result.erro.includes('6 caracteres')) {
                    mostrarErro('novaSenha', result.erro);
                } else {
                    mostrarErroGeral(result.erro);
                }
            }
            
        } catch (error) {
            console.error('Erro ao alterar senha:', error);
            mostrarErroGeral('Erro de conexão. Tente novamente.');
        } finally {
            // Restaurar botão
            btnText.textContent = 'Alterar Senha';
            spinner.classList.add('d-none');
            this.disabled = false;
        }
    });
});

