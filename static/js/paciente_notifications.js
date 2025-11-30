// Sistema de notificações em tempo real para pacientes
// Versão: 2.0 - Botão vermelho para entrar na consulta

class PatientNotificationManager {
    constructor(userId) {
        this.userId = userId;
        this.websocket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.connect();
    }

    connect() {
        // Detectar se está rodando localmente ou hospedado
        const isLocal = window.location.hostname === '127.0.0.1' || 
                       window.location.hostname === 'localhost' || 
                       window.location.hostname.startsWith('192.168.') ||
                       window.location.hostname.startsWith('10.') ||
                       window.location.hostname.startsWith('172.');
        
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        let host = window.location.host;
        
        // Para desenvolvimento local, garantir que usa a porta 8000
        if (isLocal && !window.location.port) {
            host = `${window.location.hostname}:8000`;
        } else if (isLocal && window.location.port && window.location.port !== '8000') {
            // Se está local mas usando uma porta diferente, usar 8000 para WebSocket
            host = `${window.location.hostname}:8000`;
        }
        
        const wsUrl = `${protocol}//${host}/ws/paciente/${this.userId}`;
        
        console.log('Ambiente detectado:', isLocal ? 'Local' : 'Hospedado');
        console.log('Host usado para WebSocket:', host);
        console.log('Conectando ao sistema de notificações...', wsUrl);
        
        this.websocket = new WebSocket(wsUrl);
        
        this.websocket.onopen = () => {
            console.log('Conectado ao sistema de notificações');
            this.reconnectAttempts = 0;
            this.showConnectionStatus('Conectado ao sistema de notificações', 'success');
        };
        
        this.websocket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                console.log('Notificação recebida:', data);
                this.handleNotification(data);
            } catch (error) {
                console.error('Erro ao processar notificação:', error);
            }
        };
        
        this.websocket.onclose = () => {
            console.log('Conexão perdida. Tentando reconectar...');
            this.showConnectionStatus('Conexão perdida. Reconectando...', 'warning');
            this.reconnect();
        };
        
        this.websocket.onerror = (error) => {
            console.error('Erro no WebSocket:', error);
            this.showConnectionStatus('Erro de conexão', 'error');
        };
    }

    reconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);
            setTimeout(() => this.connect(), delay);
        } else {
            this.showConnectionStatus('Não foi possível conectar ao sistema de notificações', 'error');
        }
    }

    handleNotification(data) {
        console.log('Notificação recebida:', data);
        
        // Enviar para o sistema de notificações persistentes se disponível
        if (typeof window.handleWebSocketNotification === 'function') {
            window.handleWebSocketNotification(data);
        }
        
        switch (data.type) {
            case 'consultation_started':
                this.showConsultationNotification(data);
                break;
            case 'confirmacao_consulta':
                // Será tratada pelo sistema persistente
                break;
            default:
                console.log('Tipo de notificação desconhecido:', data.type);
        }
    }

    showConsultationNotification(data) {
        // Criar notificação visual
        const notification = this.createNotificationElement(data);
        document.body.appendChild(notification);
        
        // Notificação do browser
        this.showBrowserNotification(data);
        
        // Som de notificação
        this.playNotificationSound();
        
        // Vibração (se suportado)
        if ('vibrate' in navigator) {
            navigator.vibrate([200, 100, 200]);
        }
    }

    createNotificationElement(data) {
        // Remove notificações anteriores
        const existingNotifications = document.querySelectorAll('.consultation-notification');
        existingNotifications.forEach(n => n.remove());
        
        const notification = document.createElement('div');
        notification.className = 'consultation-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <div class="notification-header">
                    <i class="bi bi-camera-video"></i>
                    <strong>Consulta Iniciada</strong>
                    <button class="btn-close-notification" onclick="this.closest('.consultation-notification').remove()">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
                <div class="notification-body">
                    <p class="mb-2">${data.message}</p>
                    <small class="text-muted">
                        <i class="bi bi-clock me-1"></i>
                        ${new Date(data.timestamp).toLocaleTimeString()}
                    </small>
                </div>
                <div class="notification-actions">
                    <button class="btn btn-danger btn-sm" onclick="joinVideoCall('${data.room_id}')">
                        <i class="bi bi-camera-video me-1"></i>
                        Entrar na Consulta
                    </button>
                    <button class="btn btn-secondary btn-sm" onclick="this.closest('.consultation-notification').remove()">
                        <i class="bi bi-x me-1"></i>
                        Ignorar
                    </button>
                </div>
            </div>
        `;
        
        // Animação de entrada
        setTimeout(() => {
            notification.classList.add('notification-show');
        }, 100);
        
        return notification;
    }

    showBrowserNotification(data) {
        if (Notification.permission === 'granted') {
            const notification = new Notification('MedLive - Consulta Iniciada', {
                body: data.message,
                icon: '/static/img/medlive-icon.png',
                badge: '/static/img/medlive-badge.png',
                tag: 'consultation-started',
                requireInteraction: true,
                actions: [
                    { action: 'join', title: 'Entrar na Consulta' },
                    { action: 'ignore', title: 'Ignorar' }
                ]
            });

            notification.onclick = () => {
                window.focus();
                joinVideoCall(data.room_id);
                notification.close();
            };
        }
    }

    playNotificationSound() {
        // Tentar carregar som personalizado primeiro
        const audio = new Audio('/static/sounds/consultation-notification.mp3');
        audio.volume = 0.7;
        
        audio.play().catch(() => {
            // Fallback para beep usando Web Audio API
            try {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                
                // Sequência de beeps
                oscillator.frequency.value = 1000;
                oscillator.type = 'sine';
                
                gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
                
                oscillator.start(audioContext.currentTime);
                oscillator.stop(audioContext.currentTime + 0.2);
                
                // Segundo beep
                setTimeout(() => {
                    const oscillator2 = audioContext.createOscillator();
                    const gainNode2 = audioContext.createGain();
                    
                    oscillator2.connect(gainNode2);
                    gainNode2.connect(audioContext.destination);
                    
                    oscillator2.frequency.value = 1200;
                    oscillator2.type = 'sine';
                    
                    gainNode2.gain.setValueAtTime(0.3, audioContext.currentTime);
                    gainNode2.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
                    
                    oscillator2.start(audioContext.currentTime);
                    oscillator2.stop(audioContext.currentTime + 0.2);
                }, 300);
                
            } catch (error) {
                console.log('Não foi possível reproduzir o som de notificação');
            }
        });
    }

    showConnectionStatus(message, type) {
        // Remove status anterior
        const existingStatus = document.querySelector('.connection-status');
        if (existingStatus) {
            existingStatus.remove();
        }

        // Não mostrar status de sucesso se não for importante
        if (type === 'success') return;

        const status = document.createElement('div');
        status.className = `connection-status connection-status-${type}`;
        status.innerHTML = `
            <i class="bi bi-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
        `;
        
        document.body.appendChild(status);
        
        // Auto-remover status de aviso
        if (type === 'warning') {
            setTimeout(() => {
                if (status.parentElement) {
                    status.remove();
                }
            }, 3000);
        }
    }
}

// Função global para entrar na videoconferência
function joinVideoCall(roomId) {
    console.log('Entrando na videoconferência:', roomId);
    
    // Mostrar loading
    showPatientNotification('Entrando na consulta...', 'info');
    
    // Redirecionar para sala de videoconferência
    window.location.href = `/videoconferencia/${roomId}`;
    
    // Remover notificações de consulta
    const consultationNotifications = document.querySelectorAll('.consultation-notification');
    consultationNotifications.forEach(n => n.remove());
}

// Função para mostrar notificações simples
function showPatientNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `patient-notification patient-notification-${type}`;
    notification.innerHTML = `
        <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
        ${message}
    `;
    
    document.body.appendChild(notification);
    
    // Animação de entrada
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Auto-remover
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// Função para solicitar permissões de notificação
function requestNotificationPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                showPatientNotification('Notificações ativadas com sucesso!', 'success');
            } else if (permission === 'denied') {
                showPatientNotification('Notificações foram negadas. Você pode ativá-las nas configurações do navegador.', 'warning', 5000);
            }
        });
    }
}

// Inicialização quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    // Solicitar permissão para notificações
    setTimeout(requestNotificationPermission, 2000);
    
    // Inicializar gerenciador de notificações se ID do paciente estiver disponível
    if (typeof pacienteId !== 'undefined' && pacienteId) {
        console.log('Inicializando sistema de notificações para paciente:', pacienteId);
        window.patientManager = new PatientNotificationManager(pacienteId);
    } else {
        console.log('ID do paciente não encontrado - sistema de notificações não iniciado');
    }
});

// Exportar para uso global
window.MedLive = window.MedLive || {};
window.MedLive.PatientNotificationManager = PatientNotificationManager;
window.MedLive.joinVideoCall = joinVideoCall;
window.MedLive.showPatientNotification = showPatientNotification;