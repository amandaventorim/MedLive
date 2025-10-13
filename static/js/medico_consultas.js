// Funções para iniciar consulta e gerenciar notificações do médico

// Função para iniciar consulta
async function iniciarConsulta(agendamentoId) {
    try {
        // Mostrar loading
        showNotification('Iniciando consulta...', 'info');
        
        const response = await fetch(`/consulta/${agendamentoId}/iniciar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Mostrar confirmação
            showNotification('Consulta iniciada! Paciente notificado.', 'success');
            
            // Aguardar um pouco antes de abrir a sala
            setTimeout(() => {
                // Redirecionar para sala de videoconferência
                window.location.href = `/videoconferencia/${data.room_id}`;
            }, 1000);
            
            // Atualizar status na interface se necessário
            updateConsultationStatus(agendamentoId, 'em_andamento');
            
        } else {
            showNotification(data.detail || 'Erro ao iniciar consulta', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showNotification('Erro de conexão ao iniciar consulta', 'error');
    }
}

// Função para mostrar notificações visuais
function showNotification(message, type = 'info') {
    // Remove notificações anteriores
    const existingNotifications = document.querySelectorAll('.medlive-notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Cria nova notificação
    const notification = document.createElement('div');
    notification.className = `alert alert-${getBootstrapClass(type)} alert-dismissible fade show medlive-notification`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 500px;
        box-shadow: 0 4px 20px rgba(0, 25, 66, 0.3);
        border-left: 4px solid ${getBorderColor(type)};
    `;
    
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="${getIcon(type)} me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remover após 5 segundos (exceto para erros)
    if (type !== 'error') {
        setTimeout(() => {
            if (notification.parentElement) {
                notification.classList.remove('show');
                setTimeout(() => notification.remove(), 150);
            }
        }, 5000);
    }
}

// Função para mapear tipos para classes Bootstrap
function getBootstrapClass(type) {
    const mapping = {
        'success': 'success',
        'error': 'danger',
        'warning': 'warning',
        'info': 'info'
    };
    return mapping[type] || 'info';
}

// Função para obter cor da borda
function getBorderColor(type) {
    const mapping = {
        'success': '#28a745',
        'error': '#dc3545',
        'warning': '#ffc107',
        'info': '#17a2b8'
    };
    return mapping[type] || '#17a2b8';
}

// Função para obter ícone
function getIcon(type) {
    const mapping = {
        'success': 'bi bi-check-circle-fill',
        'error': 'bi bi-exclamation-triangle-fill',
        'warning': 'bi bi-exclamation-triangle',
        'info': 'bi bi-info-circle-fill'
    };
    return mapping[type] || 'bi bi-info-circle-fill';
}

// Função para atualizar status da consulta na interface
function updateConsultationStatus(agendamentoId, novoStatus) {
    // Procurar pelo elemento que representa este agendamento
    const statusElements = document.querySelectorAll(`[data-agendamento-id="${agendamentoId}"] .status-badge`);
    const statusLabels = {
        'agendado': 'Agendado',
        'em_andamento': 'Em Andamento',
        'finalizado': 'Finalizado',
        'cancelado': 'Cancelado'
    };
    
    statusElements.forEach(element => {
        element.textContent = statusLabels[novoStatus] || novoStatus;
        element.className = `badge status-badge status-${novoStatus}`;
    });
    
    // Atualizar botões de ação se necessário
    const actionButtons = document.querySelectorAll(`[data-agendamento-id="${agendamentoId}"] .btn-iniciar-consulta`);
    actionButtons.forEach(button => {
        if (novoStatus === 'em_andamento') {
            button.textContent = 'Entrar na Sala';
            button.classList.remove('btn-primary');
            button.classList.add('btn-success');
        }
    });
}

// Função para conectar ao WebSocket (opcional - para receber notificações do paciente)
function connectToWebSocket(medicoId) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/medico/${medicoId}`;
    
    const websocket = new WebSocket(wsUrl);
    
    websocket.onopen = function() {
        console.log('Médico conectado ao sistema de notificações');
    };
    
    websocket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        handleDoctorNotification(data);
    };
    
    websocket.onclose = function() {
        console.log('Conexão WebSocket perdida. Tentando reconectar...');
        setTimeout(() => connectToWebSocket(medicoId), 3000);
    };
    
    websocket.onerror = function(error) {
        console.error('Erro no WebSocket do médico:', error);
    };
    
    return websocket;
}

// Função para tratar notificações recebidas pelo médico
function handleDoctorNotification(data) {
    if (data.type === 'patient_joined') {
        showNotification(data.message, 'info');
        
        // Opcionalmente, tocar um som
        playNotificationSound();
    }
}

// Função para tocar som de notificação
function playNotificationSound() {
    // Cria um beep simples usando Web Audio API
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
    } catch (error) {
        console.log('Não foi possível reproduzir o som de notificação');
    }
}

// Função para adicionar event listeners aos botões de iniciar consulta
function setupConsultationButtons() {
    document.addEventListener('click', function(event) {
        if (event.target.matches('.btn-iniciar-consulta') || event.target.closest('.btn-iniciar-consulta')) {
            event.preventDefault();
            const button = event.target.closest('.btn-iniciar-consulta');
            const agendamentoId = button.getAttribute('data-agendamento-id');
            
            if (agendamentoId) {
                iniciarConsulta(agendamentoId);
            } else {
                showNotification('ID do agendamento não encontrado', 'error');
            }
        }
    });
}

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    // Configurar botões de consulta
    setupConsultationButtons();
    
    // Conectar ao WebSocket se ID do médico estiver disponível
    if (typeof medicoId !== 'undefined' && medicoId) {
        connectToWebSocket(medicoId);
    }
});

// Exportar funções para uso global
window.MedLive = window.MedLive || {};
window.MedLive.iniciarConsulta = iniciarConsulta;
window.MedLive.showNotification = showNotification;