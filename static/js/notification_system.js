// Sistema de Notificações Persistentes - MedLive
// Gerencia notificações na navbar com persistência em banco

class NotificationSystem {
    constructor(userId, userType) {
        this.userId = userId;
        this.userType = userType;
        this.dropdownOpen = false;
        this.notifications = [];
        this.unreadCount = 0;
        
        this.initializeElements();
        this.loadNotifications();
        this.setupEventListeners();
        this.startPolling();
    }
    
    initializeElements() {
        this.button = document.getElementById('notificationsButton');
        this.badge = document.getElementById('notificationBadge');
        this.dropdown = document.getElementById('notificationsDropdown');
        this.list = document.getElementById('notificationsList');
        
        // Verificar se todos os elementos foram encontrados
        if (!this.button) {
            console.warn('Notifications button not found');
        }
        if (!this.dropdown) {
            console.warn('Notifications dropdown not found');
        }
        if (!this.list) {
            console.warn('Notifications list not found');
        }
        if (!this.badge) {
            console.warn('Notifications badge not found');
        }
        
        console.log('Notification elements initialized:', {
            button: !!this.button,
            dropdown: !!this.dropdown,
            list: !!this.list,
            badge: !!this.badge
        });
    }
    
    setupEventListeners() {
        // Event listener para o botão de notificações
        if (this.button) {
            this.button.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.toggleDropdown();
            });
        }
        
        // Fechar dropdown quando clicar fora (com delay para evitar conflito)
        document.addEventListener('click', (e) => {
            // Delay para permitir que o clique do botão seja processado primeiro
            setTimeout(() => {
                if (!e.target.closest('.notifications-wrapper') && this.dropdownOpen) {
                    this.closeDropdown();
                }
            }, 10);
        });
        
        // Esc para fechar
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeDropdown();
            }
        });
        
        // Melhor controle para mobile
        window.addEventListener('resize', () => {
            if (this.dropdownOpen && window.innerWidth <= 576) {
                this.adjustMobilePosition();
            }
        });
        
        // Prevenir scroll do body quando dropdown está aberto no mobile
        if (window.innerWidth <= 576) {
            document.addEventListener('touchmove', (e) => {
                if (this.dropdownOpen && !e.target.closest('.notifications-dropdown')) {
                    e.preventDefault();
                }
            }, { passive: false });
        }
    }
    
    adjustMobilePosition() {
        if (window.innerWidth <= 576 && this.dropdown) {
            this.dropdown.classList.add('mobile-fixed');
            document.body.style.overflow = this.dropdownOpen ? 'hidden' : '';
        } else {
            this.dropdown.classList.remove('mobile-fixed');
            document.body.style.overflow = '';
        }
    }
    
    toggleDropdown() {
        if (this.dropdownOpen) {
            this.closeDropdown();
        } else {
            this.openDropdown();
        }
    }
    
    openDropdown() {
        if (!this.dropdown) {
            console.warn('Dropdown element not found');
            return;
        }
        
        console.log('Opening dropdown...');
        this.dropdownOpen = true;
        
        // Forçar exibição
        this.dropdown.style.display = 'block';
        this.dropdown.style.opacity = '0';
        this.dropdown.style.transform = 'translateY(-10px) scale(0.95)';
        
        if (this.button) {
            this.button.classList.add('active');
        }
        
        // Ajustar posição para mobile
        this.adjustMobilePosition();
        
        // Recarregar notificações
        this.loadNotifications();
        
        // Adicionar classe para animação com delay
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                this.dropdown.classList.add('show');
                this.dropdown.style.opacity = '';
                this.dropdown.style.transform = '';
            });
        });
        
        console.log('Dropdown opened, dropdownOpen:', this.dropdownOpen);
    }
    
    closeDropdown() {
        if (!this.dropdown) return;
        
        console.log('Closing dropdown...');
        this.dropdownOpen = false;
        this.dropdown.classList.remove('show');
        this.dropdown.classList.remove('mobile-fixed');
        
        if (this.button) {
            this.button.classList.remove('active');
        }
        
        document.body.style.overflow = '';
        
        // Esconder após animação
        setTimeout(() => {
            if (!this.dropdownOpen && this.dropdown) {
                this.dropdown.style.display = 'none';
            }
        }, 300);
        
        console.log('Dropdown closed, dropdownOpen:', this.dropdownOpen);
    }
    
    async loadNotifications() {
        try {
            const response = await fetch(`/api/notifications/${this.userType}/${this.userId}`);
            if (response.ok) {
                const data = await response.json();
                this.notifications = data.notifications || [];
                this.unreadCount = data.unread_count || 0;
                this.updateBadge();
                this.renderNotifications();
            }
        } catch (error) {
            console.error('Erro ao carregar notificações:', error);
        }
    }
    
    updateBadge() {
        if (this.unreadCount > 0) {
            this.badge.textContent = this.unreadCount > 99 ? '99+' : this.unreadCount;
            this.badge.style.display = 'block';
            this.button.classList.add('has-notifications');
        } else {
            this.badge.style.display = 'none';
            this.button.classList.remove('has-notifications');
        }
    }
    
    renderNotifications() {
        if (this.notifications.length === 0) {
            this.list.innerHTML = `
                <div class="text-center text-muted p-3">
                    <i class="bi bi-bell-slash"></i>
                    <p class="mb-0">Nenhuma notificação</p>
                </div>
            `;
            return;
        }
        
        this.list.innerHTML = this.notifications.map(notification => 
            this.renderNotificationItem(notification)
        ).join('');
        
        // Adicionar event listeners
        this.list.querySelectorAll('.notification-item').forEach(item => {
            item.addEventListener('click', () => {
                const notificationId = item.dataset.notificationId;
                this.handleNotificationClick(notificationId);
            });
        });
    }
    
    renderNotificationItem(notification) {
        const isUnread = !notification.lida;
        const timeAgo = this.getTimeAgo(notification.dataInclusao);
        const iconClass = this.getIconClass(notification.tipo);
        const iconColor = this.getIconColor(notification.tipo);
        
        let actionButtons = '';
        if (notification.acaoRequerida && notification.tipo === 'confirmacao_consulta') {
            actionButtons = `
                <div class="notification-actions">
                    <button class="btn btn-sm btn-success" onclick="confirmPresence(${notification.idNotificacao}, true)">
                        <i class="bi bi-check"></i> Sim, vou comparecer
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="confirmPresence(${notification.idNotificacao}, false)">
                        <i class="bi bi-x"></i> Não posso comparecer
                    </button>
                </div>
            `;
        } else if (notification.tipo === 'consulta_iniciada' && notification.dadosAdicionais) {
            const dados = JSON.parse(notification.dadosAdicionais);
            actionButtons = `
                <div class="notification-actions">
                    <button class="btn btn-sm btn-danger" onclick="joinVideoCall('${dados.room_id}')">
                        <i class="bi bi-camera-video"></i> Entrar na Consulta
                    </button>
                </div>
            `;
        }
        
        return `
            <div class="notification-item ${isUnread ? 'unread' : ''}" data-notification-id="${notification.idNotificacao}">
                <div class="notification-content">
                    <div class="notification-icon ${iconColor}">
                        <i class="bi ${iconClass}"></i>
                    </div>
                    <div class="notification-text">
                        <div class="notification-title">${notification.titulo}</div>
                        <div class="notification-message">${notification.mensagem}</div>
                        <div class="notification-time">${timeAgo}</div>
                        ${actionButtons}
                    </div>
                </div>
            </div>
        `;
    }
    
    getIconClass(tipo) {
        const icons = {
            'novo_agendamento': 'bi-calendar-plus',
            'consulta_iniciada': 'bi-camera-video',
            'confirmacao_consulta': 'bi-question-circle',
            'resposta_confirmacao': 'bi-check-circle',
            'consulta_cancelada': 'bi-x-circle',
            'default': 'bi-bell'
        };
        return icons[tipo] || icons.default;
    }
    
    getIconColor(tipo) {
        const colors = {
            'novo_agendamento': 'success',
            'consulta_iniciada': 'info',
            'confirmacao_consulta': 'warning',
            'resposta_confirmacao': 'success',
            'consulta_cancelada': 'danger',
            'default': 'info'
        };
        return colors[tipo] || colors.default;
    }
    
    getTimeAgo(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);
        
        if (diffInSeconds < 60) return 'Agora mesmo';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m atrás`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h atrás`;
        if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d atrás`;
        
        return date.toLocaleDateString('pt-BR');
    }
    
    async handleNotificationClick(notificationId) {
        // Marcar como lida se ainda não foi
        const notification = this.notifications.find(n => n.idNotificacao == notificationId);
        if (notification && !notification.lida) {
            await this.markAsRead(notificationId);
        }
        
        // Ações específicas baseadas no tipo
        if (notification) {
            this.handleNotificationAction(notification);
        }
    }
    
    handleNotificationAction(notification) {
        switch (notification.tipo) {
            case 'novo_agendamento':
                // Redirecionar para agenda
                if (this.userType === 'medico') {
                    window.location.href = '/consultas_medico';
                }
                break;
                
            case 'consulta_iniciada':
                // Já tem botão de ação na notificação
                break;
                
            case 'confirmacao_consulta':
                // Botões de ação já estão na notificação
                break;
                
            default:
                console.log('Notificação clicada:', notification);
        }
    }
    
    async markAsRead(notificationId) {
        try {
            const response = await fetch(`/api/notifications/${notificationId}/read`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: this.userId,
                    user_type: this.userType
                })
            });
            
            if (response.ok) {
                // Atualizar localmente
                const notification = this.notifications.find(n => n.idNotificacao == notificationId);
                if (notification) {
                    notification.lida = true;
                    this.unreadCount = Math.max(0, this.unreadCount - 1);
                    this.updateBadge();
                    this.renderNotifications();
                }
            }
        } catch (error) {
            console.error('Erro ao marcar notificação como lida:', error);
        }
    }
    
    async markAllAsRead() {
        try {
            const response = await fetch(`/api/notifications/${this.userType}/${this.userId}/mark-all-read`, {
                method: 'POST'
            });
            
            if (response.ok) {
                // Atualizar localmente
                this.notifications.forEach(n => n.lida = true);
                this.unreadCount = 0;
                this.updateBadge();
                this.renderNotifications();
            }
        } catch (error) {
            console.error('Erro ao marcar todas como lidas:', error);
        }
    }
    
    addNotification(notification) {
        // Adicionar nova notificação no início da lista
        this.notifications.unshift(notification);
        
        // Limitar a 50 notificações na memória
        if (this.notifications.length > 50) {
            this.notifications = this.notifications.slice(0, 50);
        }
        
        if (!notification.lida) {
            this.unreadCount++;
        }
        
        this.updateBadge();
        this.renderNotifications();
        
        // Mostrar toast se o dropdown estiver fechado
        if (!this.dropdownOpen) {
            this.showToast(notification);
        }
        
        // Tocar som de notificação
        this.playNotificationSound();
    }
    
    showToast(notification) {
        const toast = document.createElement('div');
        toast.className = 'patient-toast';
        toast.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="bi ${this.getIconClass(notification.tipo)} toast-icon"></i>
                <div class="toast-message">
                    <strong>${notification.titulo}</strong><br>
                    ${notification.mensagem}
                </div>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Mostrar toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Remover toast após 5 segundos
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 5000);
        
        // Permitir fechar clicando
        toast.addEventListener('click', () => {
            toast.classList.remove('show');
            setTimeout(() => document.body.removeChild(toast), 300);
        });
    }
    
    playNotificationSound() {
        try {
            // Criar áudio apenas se tiver permissão
            const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmMgBTuU2+/BciMFr...');
            audio.volume = 0.3;
            audio.play().catch(() => {}); // Ignorar erros de permissão
        } catch (e) {
            // Navegador não permite reprodução automática
        }
    }
    
    startPolling() {
        // Atualizar notificações a cada 30 segundos
        setInterval(() => {
            this.loadNotifications();
        }, 30000);
    }
}

// Funções globais para ações de notificação
async function confirmPresence(notificationId, confirmed) {
    try {
        const response = await fetch('/api/confirm-presence', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                notification_id: notificationId,
                confirmed: confirmed
            })
        });
        
        if (response.ok) {
            // Marcar notificação como lida e recarregar
            if (window.notificationSystem) {
                await window.notificationSystem.markAsRead(notificationId);
            }
            
            const message = confirmed ? 
                'Presença confirmada! O médico foi notificado.' : 
                'Médico notificado que você não poderá comparecer.';
            
            window.showPatientNotification(message, 'success');
        }
    } catch (error) {
        console.error('Erro ao confirmar presença:', error);
        window.showPatientNotification('Erro ao enviar confirmação', 'error');
    }
}

function markAllAsRead() {
    if (window.notificationSystem) {
        window.notificationSystem.markAllAsRead();
    }
}

// Integração com WebSocket existente
function handleWebSocketNotification(data) {
    console.log('Notificação recebida via WebSocket:', data);
    
    // Adicionar à lista se for uma notificação persistente
    if (data.persistent && window.notificationSystem) {
        window.notificationSystem.addNotification(data);
    }
    
    // Manter comportamento existente para notificações de consulta
    if (data.type === 'consultation_started') {
        if (typeof window.patientManager !== 'undefined' && window.patientManager) {
            window.patientManager.handleNotification(data);
        }
    }
}

// Exportar para uso global
window.NotificationSystem = NotificationSystem;
window.toggleNotifications = toggleNotifications;
window.markAllAsRead = markAllAsRead;
window.confirmPresence = confirmPresence;
window.handleWebSocketNotification = handleWebSocketNotification;