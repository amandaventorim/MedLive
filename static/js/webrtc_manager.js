// ========== WEBRTC MANAGER ==========
class WebRTCManager {
    constructor() {
        this.localStream = null;
        this.remoteStreams = new Map();
        this.peerConnections = new Map();
        this.websocket = null;
        this.roomId = null;
        this.userId = null;
        this.userType = null;
        this.isConnected = false;
        
        // Configuração STUN/TURN (usando servidores públicos gratuitos)
        this.rtcConfig = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' },
                { urls: 'stun:stun1.l.google.com:19302' }
            ]
        };
        
        // Elementos DOM
        this.localVideo = null;
        this.remoteVideosContainer = null;
        this.participantsCount = null;
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Listener para quando a página é fechada
        window.addEventListener('beforeunload', () => {
            this.cleanup();
        });
    }
    
    async initialize(roomId, userId, userType) {
        this.roomId = roomId;
        this.userId = userId;
        this.userType = userType;
        
        console.log(`Inicializando WebRTC para ${userType} ${userId} na sala ${roomId}`);
        
        // Encontrar elementos DOM
        this.localVideo = document.getElementById('localVideo');
        this.remoteVideosContainer = document.getElementById('remoteVideos');
        this.participantsCount = document.getElementById('participantsCount');
        
        if (!this.localVideo || !this.remoteVideosContainer) {
            console.error('Elementos de vídeo não encontrados no DOM');
            return false;
        }
        
        try {
            // Obter mídia local
            await this.getUserMedia();
            
            // Conectar WebSocket
            this.connectWebSocket();
            
            return true;
        } catch (error) {
            console.error('Erro ao inicializar WebRTC:', error);
            return false;
        }
    }
    
    async getUserMedia() {
        try {
            this.localStream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                },
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true
                }
            });
            
            if (this.localVideo) {
                this.localVideo.srcObject = this.localStream;
            }
            
            console.log('Mídia local obtida com sucesso');
        } catch (error) {
            console.error('Erro ao obter mídia:', error);
            // Tentar apenas áudio se vídeo falhar
            try {
                this.localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                console.log('Apenas áudio obtido');
            } catch (audioError) {
                console.error('Erro ao obter áudio:', audioError);
                throw audioError;
            }
        }
    }
    
    connectWebSocket() {
        const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${location.host}/ws/video/${this.roomId}/${this.userType}/${this.userId}`;
        
        console.log('[DEBUG] Conectando WebSocket:', wsUrl);
        console.log('[DEBUG] Room ID:', this.roomId);
        console.log('[DEBUG] User Type:', this.userType);
        console.log('[DEBUG] User ID:', this.userId);
        
        this.websocket = new WebSocket(wsUrl);
        
        this.websocket.onopen = () => {
            console.log('WebSocket conectado');
            this.isConnected = true;
            this.showNotification('Conectado à sala de videoconferência', 'success');
        };
        
        this.websocket.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                this.handleWebSocketMessage(message);
            } catch (error) {
                console.error('Erro ao processar mensagem WebSocket:', error);
            }
        };
        
        this.websocket.onclose = () => {
            console.log('WebSocket desconectado');
            this.isConnected = false;
            this.showNotification('Desconectado da sala', 'warning');
            
            // Tentar reconectar após 3 segundos
            setTimeout(() => {
                if (this.roomId) {
                    this.connectWebSocket();
                }
            }, 3000);
        };
        
        this.websocket.onerror = (error) => {
            console.error('Erro no WebSocket:', error);
        };
    }
    
    async handleWebSocketMessage(message) {
        console.log('Mensagem WebSocket recebida:', message);
        
        switch (message.type) {
            case 'room_users':
                // Usuários já presentes na sala
                for (const user of message.users) {
                    const userId = `${user.user_type}_${user.user_id}`;
                    await this.createPeerConnection(userId, true); // true = criar oferta
                }
                this.updateParticipantsCount();
                break;
                
            case 'user_joined':
                // Novo usuário entrou
                const newUserId = `${message.user_type}_${message.user_id}`;
                await this.createPeerConnection(newUserId, false); // false = aguardar oferta
                this.updateParticipantsCount();
                this.showNotification(`${message.user_type} entrou na sala`, 'info');
                break;
                
            case 'user_left':
                // Usuário saiu
                const leftUserId = `${message.user_type}_${message.user_id}`;
                this.removePeerConnection(leftUserId);
                this.updateParticipantsCount();
                this.showNotification(`${message.user_type} saiu da sala`, 'info');
                break;
                
            case 'webrtc_signal':
                // Sinalização WebRTC
                await this.handleWebRTCSignal(message.from_user, message.signal_data);
                break;
                
            case 'chat_message':
                // Mensagem de chat (se implementado)
                this.handleChatMessage(message);
                break;
        }
    }
    
    async createPeerConnection(remoteUserId, createOffer = false) {
        console.log(`Criando conexão peer com ${remoteUserId}, createOffer: ${createOffer}`);
        
        const peerConnection = new RTCPeerConnection(this.rtcConfig);
        this.peerConnections.set(remoteUserId, peerConnection);
        
        // Adicionar stream local
        if (this.localStream) {
            this.localStream.getTracks().forEach(track => {
                peerConnection.addTrack(track, this.localStream);
            });
        }
        
        // Listener para stream remoto
        peerConnection.ontrack = (event) => {
            console.log('Stream remoto recebido de', remoteUserId);
            const remoteStream = event.streams[0];
            this.remoteStreams.set(remoteUserId, remoteStream);
            this.displayRemoteStream(remoteUserId, remoteStream);
        };
        
        // Listener para candidatos ICE
        peerConnection.onicecandidate = (event) => {
            if (event.candidate) {
                this.sendWebRTCSignal(remoteUserId, {
                    type: 'ice-candidate',
                    candidate: event.candidate
                });
            }
        };
        
        // Listener para mudança de estado da conexão
        peerConnection.onconnectionstatechange = () => {
            console.log(`Estado da conexão com ${remoteUserId}:`, peerConnection.connectionState);
            if (peerConnection.connectionState === 'failed') {
                // Tentar reconectar
                this.removePeerConnection(remoteUserId);
                setTimeout(() => {
                    this.createPeerConnection(remoteUserId, createOffer);
                }, 2000);
            }
        };
        
        // Criar oferta se necessário
        if (createOffer) {
            try {
                const offer = await peerConnection.createOffer();
                await peerConnection.setLocalDescription(offer);
                
                this.sendWebRTCSignal(remoteUserId, {
                    type: 'offer',
                    offer: offer
                });
            } catch (error) {
                console.error('Erro ao criar oferta:', error);
            }
        }
    }
    
    async handleWebRTCSignal(fromUser, signalData) {
        console.log(`Sinal WebRTC de ${fromUser}:`, signalData.type);
        
        const peerConnection = this.peerConnections.get(fromUser);
        if (!peerConnection) {
            console.error(`Conexão peer não encontrada para ${fromUser}`);
            return;
        }
        
        try {
            switch (signalData.type) {
                case 'offer':
                    await peerConnection.setRemoteDescription(signalData.offer);
                    const answer = await peerConnection.createAnswer();
                    await peerConnection.setLocalDescription(answer);
                    
                    this.sendWebRTCSignal(fromUser, {
                        type: 'answer',
                        answer: answer
                    });
                    break;
                    
                case 'answer':
                    await peerConnection.setRemoteDescription(signalData.answer);
                    break;
                    
                case 'ice-candidate':
                    await peerConnection.addIceCandidate(signalData.candidate);
                    break;
            }
        } catch (error) {
            console.error(`Erro ao processar sinal WebRTC de ${fromUser}:`, error);
        }
    }
    
    sendWebRTCSignal(targetUser, signalData) {
        if (this.websocket && this.isConnected) {
            const message = {
                type: 'webrtc_signal',
                target_user: targetUser,
                signal_data: signalData
            };
            
            this.websocket.send(JSON.stringify(message));
        }
    }
    
    displayRemoteStream(userId, stream) {
        // Remover vídeo existente se houver
        const existingVideo = document.getElementById(`remote-${userId}`);
        if (existingVideo) {
            existingVideo.remove();
        }
        
        // Criar novo elemento de vídeo
        const videoElement = document.createElement('video');
        videoElement.id = `remote-${userId}`;
        videoElement.autoplay = true;
        videoElement.playsInline = true;
        videoElement.srcObject = stream;
        videoElement.className = 'remote-video';
        
        // Adicionar ao container
        if (this.remoteVideosContainer) {
            this.remoteVideosContainer.appendChild(videoElement);
        }
        
        console.log(`Vídeo remoto adicionado para ${userId}`);
    }
    
    removePeerConnection(userId) {
        console.log(`Removendo conexão peer com ${userId}`);
        
        // Fechar conexão peer
        const peerConnection = this.peerConnections.get(userId);
        if (peerConnection) {
            peerConnection.close();
            this.peerConnections.delete(userId);
        }
        
        // Remover stream remoto
        this.remoteStreams.delete(userId);
        
        // Remover elemento de vídeo
        const videoElement = document.getElementById(`remote-${userId}`);
        if (videoElement) {
            videoElement.remove();
        }
    }
    
    updateParticipantsCount() {
        const count = this.peerConnections.size + 1; // +1 para incluir usuário local
        if (this.participantsCount) {
            this.participantsCount.textContent = count;
        }
        
        // Esconder/mostrar mensagem de espera
        const waitingMessage = document.getElementById('waitingMessage');
        if (waitingMessage) {
            if (this.peerConnections.size > 0) {
                waitingMessage.style.display = 'none';
            } else {
                waitingMessage.style.display = 'block';
            }
        }
        
        console.log(`Participantes na sala: ${count}`);
    }
    
    toggleMicrophone() {
        if (this.localStream) {
            const audioTrack = this.localStream.getAudioTracks()[0];
            if (audioTrack) {
                audioTrack.enabled = !audioTrack.enabled;
                return audioTrack.enabled;
            }
        }
        return false;
    }
    
    toggleCamera() {
        if (this.localStream) {
            const videoTrack = this.localStream.getVideoTracks()[0];
            if (videoTrack) {
                videoTrack.enabled = !videoTrack.enabled;
                return videoTrack.enabled;
            }
        }
        return false;
    }
    
    showNotification(message, type = 'info') {
        // Usar a função existente se disponível, senão criar uma simples
        if (typeof showConsultationNotification === 'function') {
            showConsultationNotification(message, type);
        } else {
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
    }
    
    cleanup() {
        console.log('Limpando recursos WebRTC...');
        
        // Fechar todas as conexões peer
        this.peerConnections.forEach(pc => pc.close());
        this.peerConnections.clear();
        
        // Parar stream local
        if (this.localStream) {
            this.localStream.getTracks().forEach(track => track.stop());
        }
        
        // Fechar WebSocket
        if (this.websocket) {
            this.websocket.close();
        }
        
        this.isConnected = false;
    }
}

// Instância global
window.webrtcManager = new WebRTCManager();
