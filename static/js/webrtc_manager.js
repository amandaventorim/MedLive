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
            console.log('[DEBUG] Solicitando acesso à câmera e microfone...');
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
            
            console.log('[DEBUG] Mídia local obtida:', {
                videoTracks: this.localStream.getVideoTracks().length,
                audioTracks: this.localStream.getAudioTracks().length,
                streamId: this.localStream.id
            });
            
            if (this.localVideo) {
                this.localVideo.srcObject = this.localStream;
                console.log('[DEBUG] Stream local atribuído ao elemento de vídeo');
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
        // Usar o utilitário WebSocket para configuração automática
        const wsPath = `/ws/video/${this.roomId}/${this.userType}/${this.userId}`;
        const wsUrl = window.WebSocketUtil ? 
                     window.WebSocketUtil.getURL(wsPath) : 
                     this.getFallbackWebSocketURL(wsPath);
        
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
            console.log(`[DEBUG] Adicionando tracks ao peer ${remoteUserId}:`, {
                videoTracks: this.localStream.getVideoTracks().length,
                audioTracks: this.localStream.getAudioTracks().length
            });
            
            this.localStream.getTracks().forEach(track => {
                console.log(`[DEBUG] Adicionando track: ${track.kind} (enabled: ${track.enabled})`);
                peerConnection.addTrack(track, this.localStream);
            });
        } else {
            console.warn(`[DEBUG] Nenhum stream local disponível para ${remoteUserId}`);
        }
        
        // Listener para stream remoto
        peerConnection.ontrack = (event) => {
            console.log(`[DEBUG] Stream remoto recebido de ${remoteUserId}:`, {
                streams: event.streams.length,
                track: event.track.kind,
                trackEnabled: event.track.enabled
            });
            
            const remoteStream = event.streams[0];
            if (remoteStream) {
                console.log(`[DEBUG] Stream remoto details:`, {
                    streamId: remoteStream.id,
                    videoTracks: remoteStream.getVideoTracks().length,
                    audioTracks: remoteStream.getAudioTracks().length
                });
                
                this.remoteStreams.set(remoteUserId, remoteStream);
                this.displayRemoteStream(remoteUserId, remoteStream);
            } else {
                console.warn(`[DEBUG] Nenhum stream recebido de ${remoteUserId}`);
            }
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
                console.log(`[DEBUG] Criando oferta para ${remoteUserId}`);
                const offer = await peerConnection.createOffer();
                await peerConnection.setLocalDescription(offer);
                
                console.log(`[DEBUG] Oferta criada e definida localmente para ${remoteUserId}`);
                
                this.sendWebRTCSignal(remoteUserId, {
                    type: 'offer',
                    offer: offer
                });
            } catch (error) {
                console.error(`[DEBUG] Erro ao criar oferta para ${remoteUserId}:`, error);
            }
        }
    }
    
    async handleWebRTCSignal(fromUser, signalData) {
        console.log(`[DEBUG] Sinal WebRTC de ${fromUser}: ${signalData.type}`);
        
        const peerConnection = this.peerConnections.get(fromUser);
        if (!peerConnection) {
            console.error(`[DEBUG] Conexão peer não encontrada para ${fromUser}`);
            return;
        }
        
        try {
            switch (signalData.type) {
                case 'offer':
                    console.log(`[DEBUG] Processando oferta de ${fromUser}`);
                    await peerConnection.setRemoteDescription(signalData.offer);
                    console.log(`[DEBUG] Descrição remota definida para ${fromUser}`);
                    
                    const answer = await peerConnection.createAnswer();
                    await peerConnection.setLocalDescription(answer);
                    console.log(`[DEBUG] Resposta criada e definida localmente para ${fromUser}`);
                    
                    this.sendWebRTCSignal(fromUser, {
                        type: 'answer',
                        answer: answer
                    });
                    console.log(`[DEBUG] Resposta enviada para ${fromUser}`);
                    break;
                    
                case 'answer':
                    console.log(`[DEBUG] Processando resposta de ${fromUser}`);
                    await peerConnection.setRemoteDescription(signalData.answer);
                    console.log(`[DEBUG] Descrição remota (resposta) definida para ${fromUser}`);
                    break;
                    
                case 'ice-candidate':
                    console.log(`[DEBUG] Adicionando candidato ICE de ${fromUser}`);
                    await peerConnection.addIceCandidate(signalData.candidate);
                    console.log(`[DEBUG] Candidato ICE adicionado para ${fromUser}`);
                    break;
            }
        } catch (error) {
            console.error(`[DEBUG] Erro ao processar sinal WebRTC de ${fromUser}:`, error);
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
        console.log(`[DEBUG] Exibindo stream remoto para ${userId}`);
        
        // Remover vídeo existente se houver
        const existingVideo = document.getElementById(`remote-${userId}`);
        if (existingVideo) {
            console.log(`[DEBUG] Removendo vídeo existente para ${userId}`);
            existingVideo.remove();
        }
        
        // Criar novo elemento de vídeo
        const videoElement = document.createElement('video');
        videoElement.id = `remote-${userId}`;
        videoElement.autoplay = true;
        videoElement.playsInline = true;
        videoElement.muted = false; // Remote video should not be muted
        videoElement.srcObject = stream;
        videoElement.className = 'remote-video';
        
        // Adicionar listeners para debug
        videoElement.onloadedmetadata = () => {
            console.log(`[DEBUG] Metadata carregada para vídeo ${userId}:`, {
                videoWidth: videoElement.videoWidth,
                videoHeight: videoElement.videoHeight,
                duration: videoElement.duration
            });
        };
        
        videoElement.onplay = () => {
            console.log(`[DEBUG] Vídeo ${userId} começou a reproduzir`);
        };
        
        videoElement.onerror = (error) => {
            console.error(`[DEBUG] Erro no vídeo ${userId}:`, error);
        };
        
        // Adicionar ao container
        if (this.remoteVideosContainer) {
            this.remoteVideosContainer.appendChild(videoElement);
            console.log(`[DEBUG] Vídeo remoto adicionado ao DOM para ${userId}`);
            
            // Esconder mensagem de espera
            const waitingMessage = document.getElementById('waitingMessage');
            if (waitingMessage) {
                waitingMessage.style.display = 'none';
            }
        } else {
            console.error(`[DEBUG] Container de vídeos remotos não encontrado`);
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
    
    debugConnectionStates() {
        console.log('[DEBUG] === ESTADO DAS CONEXÕES WEBRTC ===');
        console.log('Local Stream:', {
            exists: !!this.localStream,
            videoTracks: this.localStream ? this.localStream.getVideoTracks().length : 0,
            audioTracks: this.localStream ? this.localStream.getAudioTracks().length : 0
        });
        
        console.log('Peer Connections:', this.peerConnections.size);
        for (const [userId, pc] of this.peerConnections) {
            console.log(`  ${userId}:`, {
                connectionState: pc.connectionState,
                iceConnectionState: pc.iceConnectionState,
                signalingState: pc.signalingState,
                localDescription: !!pc.localDescription,
                remoteDescription: !!pc.remoteDescription
            });
        }
        
        console.log('Remote Streams:', this.remoteStreams.size);
        for (const [userId, stream] of this.remoteStreams) {
            console.log(`  ${userId}:`, {
                streamId: stream.id,
                videoTracks: stream.getVideoTracks().length,
                audioTracks: stream.getAudioTracks().length
            });
        }
        console.log('===========================================');
    }
    
    getFallbackWebSocketURL(path) {
        // Fallback case if websocket_util.js isn't loaded
        const isLocal = location.hostname === '127.0.0.1' || 
                       location.hostname === 'localhost' || 
                       location.hostname.startsWith('192.168.') ||
                       location.hostname.startsWith('10.') ||
                       location.hostname.startsWith('172.');
        
        const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
        let host = location.host;
        
        if (isLocal && !location.port) {
            host = `${location.hostname}:8000`;
        } else if (isLocal && location.port && location.port !== '8000') {
            host = `${location.hostname}:8000`;
        }
        
        return `${protocol}//${host}${path}`;
    }
}

// Instância global
window.webrtcManager = new WebRTCManager();
