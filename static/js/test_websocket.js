function detectEnvironment() {
    const isLocal = window.location.hostname === '127.0.0.1' ||
        window.location.hostname === 'localhost' ||
        window.location.hostname.startsWith('192.168.') ||
        window.location.hostname.startsWith('10.') ||
        window.location.hostname.startsWith('172.');

    document.getElementById('environment').textContent = isLocal ? 'Local (Desenvolvimento)' : 'Hospedado (Produção)';
    document.getElementById('pageUrl').textContent = window.location.href;
    document.getElementById('protocol').textContent = window.location.protocol;
}

function log(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const logElement = document.getElementById('logs');
    const logLine = document.createElement('div');
    logLine.innerHTML = `<span style="color: #666;">[${timestamp}]</span> ${message}`;
    logElement.appendChild(logLine);
    logElement.scrollTop = logElement.scrollHeight;

    console.log(`[${timestamp}] ${message}`);
}

function updateStatus(message, type) {
    const statusEl = document.getElementById('status');
    statusEl.textContent = `Status: ${message}`;
    statusEl.className = `status ${type}`;
}

function testBasicWebSocket() {
    log('🔗 Iniciando teste de WebSocket básico...', 'info');
    updateStatus('Testando WebSocket básico...', 'warning');

    const wsPath = '/ws/medico/999';
    const wsUrl = window.WebSocketUtil ?
        window.WebSocketUtil.getURL(wsPath) :
        getFallbackURL(wsPath);

    log(`📍 URL gerada: ${wsUrl}`);

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        log('✅ WebSocket conectado com sucesso!', 'success');
        updateStatus('WebSocket conectado!', 'success');

        // Enviar mensagem de teste
        ws.send('{"type": "test", "message": "Hello from test page"}');
        log('📤 Mensagem de teste enviada');

        // Fechar após 2 segundos
        setTimeout(() => {
            ws.close();
            log('🔌 Conexão fechada');
        }, 2000);
    };

    ws.onmessage = (event) => {
        log(`📥 Mensagem recebida: ${event.data}`);
    };

    ws.onclose = (event) => {
        log(`🔚 WebSocket fechado - Código: ${event.code}, Razão: ${event.reason}`);
        if (event.code === 1000) {
            updateStatus('Teste concluído com sucesso', 'success');
        } else {
            updateStatus(`Falha na conexão - Código: ${event.code}`, 'error');
        }
    };

    ws.onerror = (error) => {
        log(`❌ Erro no WebSocket: ${error}`, 'error');
        updateStatus('Erro na conexão WebSocket', 'error');
    };
}

function testVideoWebSocket() {
    log('📹 Testando WebSocket de vídeo...', 'info');
    updateStatus('Testando WebSocket de vídeo...', 'warning');

    const wsPath = '/ws/video/test_room/medico/999';
    const wsUrl = window.WebSocketUtil ?
        window.WebSocketUtil.getURL(wsPath) :
        getFallbackURL(wsPath);

    log(`📍 URL de vídeo: ${wsUrl}`);

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        log('✅ WebSocket de vídeo conectado!', 'success');
        updateStatus('WebSocket de vídeo conectado!', 'success');

        setTimeout(() => {
            ws.close();
        }, 2000);
    };

    ws.onmessage = (event) => {
        log(`📥 Resposta do servidor de vídeo: ${event.data}`);
    };

    ws.onclose = (event) => {
        log(`🔚 WebSocket de vídeo fechado - Código: ${event.code}`);
        updateStatus('Teste de vídeo concluído', event.code === 1000 ? 'success' : 'error');
    };

    ws.onerror = (error) => {
        log(`❌ Erro no WebSocket de vídeo: ${error}`, 'error');
        updateStatus('Erro no WebSocket de vídeo', 'error');
    };
}

function testNotificationWebSocket() {
    log('🔔 Testando WebSocket de notificação...', 'info');
    updateStatus('Testando WebSocket de notificação...', 'warning');

    const wsPath = '/ws/paciente/999';
    const wsUrl = window.WebSocketUtil ?
        window.WebSocketUtil.getURL(wsPath) :
        getFallbackURL(wsPath);

    log(`📍 URL de notificação: ${wsUrl}`);

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        log('✅ WebSocket de notificação conectado!', 'success');
        updateStatus('WebSocket de notificação conectado!', 'success');

        setTimeout(() => {
            ws.close();
        }, 2000);
    };

    ws.onmessage = (event) => {
        log(`📥 Notificação recebida: ${event.data}`);
    };

    ws.onclose = (event) => {
        log(`🔚 WebSocket de notificação fechado - Código: ${event.code}`);
        updateStatus('Teste de notificação concluído', event.code === 1000 ? 'success' : 'error');
    };

    ws.onerror = (error) => {
        log(`❌ Erro no WebSocket de notificação: ${error}`, 'error');
        updateStatus('Erro no WebSocket de notificação', 'error');
    };
}

function getFallbackURL(path) {
    const isLocal = window.location.hostname === '127.0.0.1' ||
        window.location.hostname === 'localhost';
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    let host = window.location.host;

    if (isLocal && !window.location.port) {
        host = `${window.location.hostname}:8000`;
    } else if (isLocal && window.location.port !== '8000') {
        host = `${window.location.hostname}:8000`;
    }

    return `${protocol}//${host}${path}`;
}

function clearLogs() {
    document.getElementById('logs').innerHTML = '';
}

// Inicializar página
window.onload = () => {
    detectEnvironment();
    log('🚀 Página de teste carregada');
    log(`🌐 Ambiente: ${document.getElementById('environment').textContent}`);
    log(`📍 URL: ${window.location.href}`);
};

function detectEnvironment() {
    const isLocal = window.location.hostname === '127.0.0.1' ||
        window.location.hostname === 'localhost' ||
        window.location.hostname.startsWith('192.168.') ||
        window.location.hostname.startsWith('10.') ||
        window.location.hostname.startsWith('172.');

    document.getElementById('environment').textContent = isLocal ? 'Local (Desenvolvimento)' : 'Hospedado (Produção)';
    document.getElementById('pageUrl').textContent = window.location.href;
    document.getElementById('protocol').textContent = window.location.protocol;
}

function log(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const logElement = document.getElementById('logs');
    const logLine = document.createElement('div');
    logLine.innerHTML = `<span style="color: #666;">[${timestamp}]</span> ${message}`;
    logElement.appendChild(logLine);
    logElement.scrollTop = logElement.scrollHeight;

    console.log(`[${timestamp}] ${message}`);
}

function updateStatus(message, type) {
    const statusEl = document.getElementById('status');
    statusEl.textContent = `Status: ${message}`;
    statusEl.className = `status ${type}`;
}

function testBasicWebSocket() {
    log('🔗 Iniciando teste de WebSocket básico...', 'info');
    updateStatus('Testando WebSocket básico...', 'warning');

    const wsPath = '/ws/medico/999';
    const wsUrl = window.WebSocketUtil ?
        window.WebSocketUtil.getURL(wsPath) :
        getFallbackURL(wsPath);

    log(`📍 URL gerada: ${wsUrl}`);

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        log('✅ WebSocket conectado com sucesso!', 'success');
        updateStatus('WebSocket conectado!', 'success');

        // Enviar mensagem de teste
        ws.send('{"type": "test", "message": "Hello from test page"}');
        log('📤 Mensagem de teste enviada');

        // Fechar após 2 segundos
        setTimeout(() => {
            ws.close();
            log('🔌 Conexão fechada');
        }, 2000);
    };

    ws.onmessage = (event) => {
        log(`📥 Mensagem recebida: ${event.data}`);
    };

    ws.onclose = (event) => {
        log(`🔚 WebSocket fechado - Código: ${event.code}, Razão: ${event.reason}`);
        if (event.code === 1000) {
            updateStatus('Teste concluído com sucesso', 'success');
        } else {
            updateStatus(`Falha na conexão - Código: ${event.code}`, 'error');
        }
    };

    ws.onerror = (error) => {
        log(`❌ Erro no WebSocket: ${error}`, 'error');
        updateStatus('Erro na conexão WebSocket', 'error');
    };
}

function testVideoWebSocket() {
    log('📹 Testando WebSocket de vídeo...', 'info');
    updateStatus('Testando WebSocket de vídeo...', 'warning');

    const wsPath = '/ws/video/test_room/medico/999';
    const wsUrl = window.WebSocketUtil ?
        window.WebSocketUtil.getURL(wsPath) :
        getFallbackURL(wsPath);

    log(`📍 URL de vídeo: ${wsUrl}`);

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        log('✅ WebSocket de vídeo conectado!', 'success');
        updateStatus('WebSocket de vídeo conectado!', 'success');

        setTimeout(() => {
            ws.close();
        }, 2000);
    };

    ws.onmessage = (event) => {
        log(`📥 Resposta do servidor de vídeo: ${event.data}`);
    };

    ws.onclose = (event) => {
        log(`🔚 WebSocket de vídeo fechado - Código: ${event.code}`);
        updateStatus('Teste de vídeo concluído', event.code === 1000 ? 'success' : 'error');
    };

    ws.onerror = (error) => {
        log(`❌ Erro no WebSocket de vídeo: ${error}`, 'error');
        updateStatus('Erro no WebSocket de vídeo', 'error');
    };
}

function testNotificationWebSocket() {
    log('🔔 Testando WebSocket de notificação...', 'info');
    updateStatus('Testando WebSocket de notificação...', 'warning');

    const wsPath = '/ws/paciente/999';
    const wsUrl = window.WebSocketUtil ?
        window.WebSocketUtil.getURL(wsPath) :
        getFallbackURL(wsPath);

    log(`📍 URL de notificação: ${wsUrl}`);

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        log('✅ WebSocket de notificação conectado!', 'success');
        updateStatus('WebSocket de notificação conectado!', 'success');

        setTimeout(() => {
            ws.close();
        }, 2000);
    };

    ws.onmessage = (event) => {
        log(`📥 Notificação recebida: ${event.data}`);
    };

    ws.onclose = (event) => {
        log(`🔚 WebSocket de notificação fechado - Código: ${event.code}`);
        updateStatus('Teste de notificação concluído', event.code === 1000 ? 'success' : 'error');
    };

    ws.onerror = (error) => {
        log(`❌ Erro no WebSocket de notificação: ${error}`, 'error');
        updateStatus('Erro no WebSocket de notificação', 'error');
    };
}

function getFallbackURL(path) {
    const isLocal = window.location.hostname === '127.0.0.1' ||
        window.location.hostname === 'localhost';
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    let host = window.location.host;

    if (isLocal && !window.location.port) {
        host = `${window.location.hostname}:8000`;
    } else if (isLocal && window.location.port !== '8000') {
        host = `${window.location.hostname}:8000`;
    }

    return `${protocol}//${host}${path}`;
}

function clearLogs() {
    document.getElementById('logs').innerHTML = '';
}

// Inicializar página
window.onload = () => {
    detectEnvironment();
    log('🚀 Página de teste carregada');
    log(`🌐 Ambiente: ${document.getElementById('environment').textContent}`);
    log(`📍 URL: ${window.location.href}`);
};