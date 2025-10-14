// ========== WEBSOCKET UTILITY ==========
// Utilitário para configurar WebSocket automaticamente para ambiente local ou hospedado

/**
 * Gera a URL WebSocket correta baseada no ambiente (local ou hospedado)
 * @param {string} path - Caminho do WebSocket (ex: '/ws/video/room/user/1')
 * @returns {string} URL completa do WebSocket
 */
function getWebSocketURL(path) {
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
        // Se está local mas usando uma porta diferente (ex: proxy), usar 8000 para WebSocket
        host = `${window.location.hostname}:8000`;
    }
    // Para produção (hospedado), usar o host atual sem modificação
    
    // Garantir que o path comece com '/'
    if (!path.startsWith('/')) {
        path = '/' + path;
    }
    
    const wsUrl = `${protocol}//${host}${path}`;
    
    console.log('[WebSocket Util] Ambiente detectado:', isLocal ? 'Local' : 'Hospedado');
    console.log('[WebSocket Util] Host original:', window.location.host);
    console.log('[WebSocket Util] Host usado:', host);
    console.log('[WebSocket Util] URL gerada:', wsUrl);
    
    return wsUrl;
}

/**
 * Cria uma conexão WebSocket com configuração automática de ambiente
 * @param {string} path - Caminho do WebSocket
 * @param {Object} options - Opções de configuração
 * @returns {WebSocket} Instância do WebSocket
 */
function createWebSocket(path, options = {}) {
    const url = getWebSocketURL(path);
    const ws = new WebSocket(url);
    
    // Configurações padrão
    if (options.onOpen) ws.onopen = options.onOpen;
    if (options.onMessage) ws.onmessage = options.onMessage;
    if (options.onClose) ws.onClose = options.onClose;
    if (options.onError) ws.onError = options.onError;
    
    return ws;
}

// Disponibilizar globalmente
window.WebSocketUtil = {
    getURL: getWebSocketURL,
    create: createWebSocket
};
