function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}

function editarSecao(secao) {
    // Aqui você pode implementar a lógica de edição inline
}

// Adicionar funcionalidade aos switches de horário
document.querySelectorAll('.switch-disponibilidade input').forEach(switch_ => {
    switch_.addEventListener('change', function () {
        const horarioItem = this.closest('.horario-item');
        const periodo = horarioItem.querySelector('.horario-periodo');

        if (this.checked) {
            periodo.textContent = '08:00 - 18:00';
            periodo.style.color = '#6c757d';
        } else {
            periodo.textContent = 'Indisponível';
            periodo.style.color = '#dc3545';
        }
    });
});

// Preview de foto de perfil
document.addEventListener('DOMContentLoaded', function() {
    const fotoInput = document.getElementById('foto');
    const fotoPreview = document.querySelector('#modalEditarFoto .foto-usuario');

    if (fotoInput && fotoPreview) {
        fotoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];

            if (file) {
                // Verificar se é uma imagem
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();

                    reader.onload = function(e) {
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

document.addEventListener('DOMContentLoaded', function() {
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

// Funcionalidades de disponibilidade
function editarDisponibilidade() {
    document.getElementById('disponibilidade-view').style.display = 'none';
    document.getElementById('disponibilidade-edit').style.display = 'block';
    
    // Carregar disponibilidades atuais
    carregarDisponibilidades();
}

function cancelarEdicaoDisponibilidade() {
    document.getElementById('disponibilidade-view').style.display = 'block';
    document.getElementById('disponibilidade-edit').style.display = 'none';
}

function carregarDisponibilidades() {
    fetch('/obter_disponibilidades')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const disponibilidades = data.disponibilidades;
                const dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo'];
                
                // Primeiro, resetar todos os campos
                dias.forEach(dia => {
                    const checkbox = document.getElementById(`${dia}_ativo`);
                    const horarioInputs = document.getElementById(`horario-${dia}`);
                    const inicioInput = document.querySelector(`input[name="${dia}_inicio"]`);
                    const fimInput = document.querySelector(`input[name="${dia}_fim"]`);
                    
                    if (checkbox) {
                        checkbox.checked = false;
                    }
                    if (horarioInputs) {
                        horarioInputs.style.display = 'none';
                    }
                    if (inicioInput) {
                        inicioInput.value = '08:00';
                    }
                    if (fimInput) {
                        fimInput.value = '18:00';
                    }
                });
                
                // Agora configurar com os dados do servidor
                dias.forEach((dia, index) => {
                    const diaSemana = index + 1; // 1-7
                    const checkbox = document.getElementById(`${dia}_ativo`);
                    const horarioInputs = document.getElementById(`horario-${dia}`);
                    const inicioInput = document.querySelector(`input[name="${dia}_inicio"]`);
                    const fimInput = document.querySelector(`input[name="${dia}_fim"]`);
                    
                    if (checkbox && horarioInputs && inicioInput && fimInput) {
                        if (disponibilidades[diaSemana]) {
                            checkbox.checked = true;
                            horarioInputs.style.display = 'block';
                            inicioInput.value = disponibilidades[diaSemana].horaInicio;
                            fimInput.value = disponibilidades[diaSemana].horaFim;
                        }
                    }
                });
            } else {
                console.error('Erro na resposta:', data.message);
                showToast('Erro ao carregar disponibilidades: ' + (data.message || 'Erro desconhecido'), 'error');
            }
        })
        .catch(error => {
            console.error('Erro ao carregar disponibilidades:', error);
            showToast('Erro de conexão ao carregar disponibilidades', 'error');
        });
}

function salvarDisponibilidade() {
    const form = document.getElementById('form-disponibilidade');
    if (!form) {
        showToast('Erro: Formulário não encontrado', 'error');
        return;
    }
    
    // Coletar dados como JSON (método que funciona)
    const dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo'];
    const dadosJSON = {};
    let temDiaAtivo = false;
    
    dias.forEach(dia => {
        const checkbox = document.getElementById(`${dia}_ativo`);
        if (checkbox && checkbox.checked) {
            dadosJSON[`${dia}_ativo`] = 'on';
            temDiaAtivo = true;
            
            const inicioInput = document.querySelector(`input[name="${dia}_inicio"]`);
            const fimInput = document.querySelector(`input[name="${dia}_fim"]`);
            
            if (inicioInput && inicioInput.value) {
                dadosJSON[`${dia}_inicio`] = inicioInput.value;
            }
            if (fimInput && fimInput.value) {
                dadosJSON[`${dia}_fim`] = fimInput.value;
            }
        }
    });
    
    if (!temDiaAtivo) {
        showToast('Selecione pelo menos um dia da semana para configurar sua disponibilidade', 'error');
        return;
    }
    
    // Validar horários
    let horarioValido = true;
    dias.forEach(dia => {
        const checkbox = document.getElementById(`${dia}_ativo`);
        if (checkbox && checkbox.checked) {
            const inicioInput = document.querySelector(`input[name="${dia}_inicio"]`);
            const fimInput = document.querySelector(`input[name="${dia}_fim"]`);
            
            if (inicioInput && fimInput) {
                const inicio = inicioInput.value;
                const fim = fimInput.value;
                
                if (!inicio || !fim) {
                    showToast(`Por favor, preencha os horários para ${dia}`, 'error');
                    horarioValido = false;
                    return;
                }
                
                if (inicio >= fim) {
                    showToast(`O horário de início deve ser menor que o de fim para ${dia}`, 'error');
                    horarioValido = false;
                    return;
                }
            }
        }
    });
    
    if (!horarioValido) {
        return;
    }
    
    // Mostrar loading
    const botaoSalvar = document.querySelector('button.btn.botao-medlive[onclick="salvarDisponibilidade()"]');
    if (!botaoSalvar) {
        showToast('Erro: Botão não encontrado', 'error');
        return;
    }
    
    const textoOriginal = botaoSalvar.innerHTML;
    botaoSalvar.innerHTML = '<i class="bi bi-hourglass-split me-1"></i> Salvando...';
    botaoSalvar.disabled = true;
    
    // Usar o endpoint JSON que funciona
    fetch('/salvar_disponibilidade', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(dadosJSON)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showToast('Disponibilidade salva com sucesso!', 'success');
            cancelarEdicaoDisponibilidade();
            setTimeout(() => {
                atualizarVisualizacaoDisponibilidade();
            }, 500);
        } else {
            showToast(data.message || 'Erro ao salvar disponibilidade', 'error');
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        showToast('Erro ao salvar disponibilidade: ' + error.message, 'error');
    })
    .finally(() => {
        botaoSalvar.innerHTML = textoOriginal;
        botaoSalvar.disabled = false;
    });
}

// ...existing code...

function atualizarVisualizacaoDisponibilidade() {
    fetch('/obter_disponibilidades')
        .then(response => {
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const disponibilidades = data.disponibilidades;
                const dias = [
                    { nome: 'segunda', label: 'Segunda-feira' },
                    { nome: 'terca', label: 'Terça-feira' },
                    { nome: 'quarta', label: 'Quarta-feira' },
                    { nome: 'quinta', label: 'Quinta-feira' },
                    { nome: 'sexta', label: 'Sexta-feira' },
                    { nome: 'sabado', label: 'Sábado' },
                    { nome: 'domingo', label: 'Domingo' }
                ];
                
                dias.forEach((dia, index) => {
                    const diaSemana = index + 1; // 1-7
                    const periodoElement = document.getElementById(`periodo-${dia.nome}`);
                    const statusElement = document.getElementById(`status-${dia.nome}`);
                    
                    if (periodoElement && statusElement) {
                        if (disponibilidades[diaSemana]) {
                            const inicio = disponibilidades[diaSemana].horaInicio;
                            const fim = disponibilidades[diaSemana].horaFim;
                            periodoElement.textContent = `${inicio} - ${fim}`;
                            statusElement.innerHTML = '<i class="bi bi-check-circle text-success"></i>';
                        } else {
                            periodoElement.textContent = 'Indisponível';
                            statusElement.innerHTML = '<i class="bi bi-x-circle text-danger"></i>';
                        }
                    }
                });
            }
        })
        .catch(error => {
            // Silencioso - não mostrar erro no console em produção
        });
}

function showToast(message, type = 'info') {
    // Criar toast element
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'} border-0`;
    toast.setAttribute('role', 'alert');
    toast.style.marginBottom = '10px';
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    // Adicionar ao container de toasts
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.appendChild(toast);
    
    // Mostrar toast
    toast.style.display = 'block';
    
    // Auto remover após 5 segundos
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 5000);
    
    // Tentar usar Bootstrap Toast se disponível
    if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
        try {
            const bsToast = new bootstrap.Toast(toast);
            bsToast.show();
            
            toast.addEventListener('hidden.bs.toast', () => {
                if (toast.parentElement) {
                    toast.remove();
                }
            });
        } catch (e) {
            // Bootstrap Toast não disponível, usar fallback simples
        }
    }
}

// Adicionar event listeners quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    // Carregar disponibilidades iniciais
    setTimeout(() => {
        atualizarVisualizacaoDisponibilidade();
    }, 500);
    
    // Event listeners para switches no formulário de edição
    const dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo'];
    
    dias.forEach(dia => {
        const checkbox = document.getElementById(`${dia}_ativo`);
        const horarioInputs = document.getElementById(`horario-${dia}`);
        
        if (checkbox && horarioInputs) {
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    horarioInputs.style.display = 'block';
                    // Garantir que há valores padrão nos campos de horário
                    const inicioInput = document.querySelector(`input[name="${dia}_inicio"]`);
                    const fimInput = document.querySelector(`input[name="${dia}_fim"]`);
                    if (inicioInput && !inicioInput.value) {
                        inicioInput.value = '08:00';
                    }
                    if (fimInput && !fimInput.value) {
                        fimInput.value = '18:00';
                    }
                } else {
                    horarioInputs.style.display = 'none';
                }
            });
        }
    });
});

