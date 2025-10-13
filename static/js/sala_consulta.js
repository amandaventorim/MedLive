let consultationStartTime = Date.now();
let micMuted = false;
let cameraOff = false;
let screenSharing = false;
let recording = false;
let websocketConnection = null;

// Timer
function updateTimer() {
    const elapsed = Date.now() - consultationStartTime;
    const minutes = Math.floor(elapsed / 60000);
    const seconds = Math.floor((elapsed % 60000) / 1000);
    document.getElementById('consultationTimer').textContent =
        `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

setInterval(updateTimer, 1000);

// Controls
function toggleMic() {
    micMuted = !micMuted;
    const button = document.getElementById('micButton');
    const icon = button.querySelector('i');

    if (micMuted) {
        button.classList.add('muted');
        icon.className = 'bi bi-mic-mute';
        button.title = 'Ativar Microfone';
    } else {
        button.classList.remove('muted');
        icon.className = 'bi bi-mic';
        button.title = 'Silenciar Microfone';
    }
}

function toggleCamera() {
    cameraOff = !cameraOff;
    const button = document.getElementById('cameraButton');
    const icon = button.querySelector('i');

    if (cameraOff) {
        button.classList.add('off');
        icon.className = 'bi bi-camera-video-off';
        button.title = 'Ativar Câmera';
    } else {
        button.classList.remove('off');
        icon.className = 'bi bi-camera-video';
        button.title = 'Desativar Câmera';
    }
}

function toggleScreenShare() {
    screenSharing = !screenSharing;
    const button = document.getElementById('screenButton');
    const icon = button.querySelector('i');

    if (screenSharing) {
        button.classList.add('sharing');
        icon.className = 'bi bi-display-fill';
        button.title = 'Parar Compartilhamento';
    } else {
        button.classList.remove('sharing');
        icon.className = 'bi bi-display';
        button.title = 'Compartilhar Tela';
    }
}

function toggleRecording() {
    recording = !recording;
    const indicator = document.getElementById('recordingIndicator');

    if (recording) {
        indicator.style.display = 'block';
        alert('Gravação iniciada. O paciente foi notificado.');
    } else {
        indicator.style.display = 'none';
        alert('Gravação finalizada e salva no prontuário.');
    }
}

function endConsultation() {
    if (confirm('Deseja realmente encerrar a consulta?')) {
        alert('Consulta encerrada. Redirecionando...');
        window.location.href = 'dashboard_medico.html';
    }
}

// Chat
function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (message) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message own';
        messageDiv.innerHTML = `<strong>Você:</strong> ${message}`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        input.value = '';
    }
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Tools
function openPrescription() {
    console.log('=== Função openPrescription chamada ===');
    const modal = document.getElementById('prescriptionModal');
    console.log('Modal encontrado:', modal);
    if (modal) {
        console.log('Adicionando classe show ao modal de receita');
        modal.classList.add('show');
        console.log('Classes do modal após adicionar show:', modal.className);
    } else {
        console.error('ERRO: Modal de receita não encontrado no DOM!');
        alert('Erro: Modal de receita não encontrado. Verifique a estrutura HTML.');
    }
}

function closePrescription() {
    document.getElementById('prescriptionModal').classList.remove('show');
}

function savePrescription() {
    const medication = document.getElementById('medication').value;
    const dosage = document.getElementById('dosage').value;
    const frequency = document.getElementById('frequency').value;
    const duration = document.getElementById('duration').value;
    const observations = document.getElementById('observations').value;

    if (!medication || !dosage || !frequency || !duration) {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return;
    }

    // Simulate saving prescription
    alert('Receita salva com sucesso! O paciente receberá uma cópia por email.');
    closePrescription();

    // Clear form
    document.getElementById('prescriptionForm').reset();
}

function openMedicalRecord() {
    alert('Abrindo prontuário do paciente...');
    // In a real application, this would open the medical record
}

function shareScreen() {
    alert('Iniciando compartilhamento de tela...');
    toggleScreenShare();
}

// Simulate connection status changes
function simulateConnectionChanges() {
    const statuses = [
        { text: 'Conectado', class: '', icon: 'bi-wifi' },
        { text: 'Conectando...', class: 'connecting', icon: 'bi-wifi' },
        { text: 'Reconectando...', class: 'connecting', icon: 'bi-arrow-clockwise' }
    ];

    setInterval(() => {
        if (Math.random() > 0.95) { // 5% chance
            const status = statuses[Math.floor(Math.random() * statuses.length)];
            const indicator = document.getElementById('connectionStatus');
            indicator.className = 'status-indicator ' + status.class;
            indicator.innerHTML = `<i class="bi ${status.icon}"></i>${status.text}`;

            // Reset to connected after a few seconds
            if (status.class) {
                setTimeout(() => {
                    indicator.className = 'status-indicator';
                    indicator.innerHTML = '<i class="bi bi-wifi"></i>Conectado';
                }, 3000);
            }
        }
    }, 10000);
}

// Simulate patient messages
function simulatePatientMessages() {
    const messages = [
        'Estou me sentindo melhor hoje',
        'A dor diminuiu bastante',
        'Tomei o medicamento conforme orientado',
        'Tenho uma dúvida sobre a dosagem',
        'Quando devo retornar?'
    ];

    setInterval(() => {
        if (Math.random() > 0.9) { // 10% chance
            const message = messages[Math.floor(Math.random() * messages.length)];
            const chatMessages = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message other';
            messageDiv.innerHTML = `<strong>João Silva:</strong> ${message}`;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }, 15000);
}

// Initialize
document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM carregado, inicializando sala de consulta...');
    
    // Verificar se os modais existem
    const prescriptionModal = document.getElementById('prescriptionModal');
    const examRequestModal = document.getElementById('examRequestModal');
    const certificateModal = document.getElementById('certificateModal');
    const waitingQueueModal = document.getElementById('waitingQueueModal');
    
    console.log('Modal de receita:', prescriptionModal ? 'Encontrado' : 'NÃO ENCONTRADO');
    console.log('Modal de exame:', examRequestModal ? 'Encontrado' : 'NÃO ENCONTRADO');
    console.log('Modal de atestado:', certificateModal ? 'Encontrado' : 'NÃO ENCONTRADO');
    console.log('Modal de fila:', waitingQueueModal ? 'Encontrado' : 'NÃO ENCONTRADO');
    
    // Inicializar simulações
    simulateConnectionChanges();
    simulatePatientMessages();

    // Get patient info from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const patientId = urlParams.get('patient');

    if (patientId) {
        // Load patient-specific data
        console.log('Loading data for patient:', patientId);
    }
    
    // Adicionar listener para o dropdown
    const dropdown = document.getElementById('documentsDropdown');
    if (dropdown) {
        console.log('Dropdown de documentos encontrado');
        dropdown.addEventListener('click', function(e) {
            console.log('Dropdown clicado');
        });
    } else {
        console.error('Dropdown de documentos NÃO ENCONTRADO');
    }
    
    // Função de teste global
    window.testModals = function() {
        console.log('=== TESTANDO MODAIS ===');
        console.log('Testando openPrescription...');
        openPrescription();
        setTimeout(() => {
            closePrescription();
            console.log('Testando openExamRequest...');
            openExamRequest();
            setTimeout(() => {
                closeExamRequest();
                console.log('Testando openCertificate...');
                openCertificate();
                setTimeout(() => {
                    closeCertificate();
                    console.log('=== TESTE COMPLETO ===');
                }, 1000);
            }, 1000);
        }, 1000);
    };
    
    console.log('Para testar os modais, digite no console: testModals()');
});

function openWaitingQueue() {
    document.getElementById('waitingQueueModal').classList.add('show');
}

function closeWaitingQueue() {
    document.getElementById('waitingQueueModal').classList.remove('show');
}


function refreshQueue() {
    // Simula atualização da fila de espera
    const button = event.target;
    const originalText = button.innerHTML;
    
    button.innerHTML = '<i class="bi bi-arrow-clockwise me-1 spin"></i>Atualizando...';
    button.disabled = true;
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.disabled = false;
        
        // Simula uma pequena mudança na fila
        const badges = document.querySelectorAll('#waitingQueueList .badge');
        if (badges.length > 0) {
            const randomBadge = badges[Math.floor(Math.random() * badges.length)];
            randomBadge.textContent = 'Atualizado';
            randomBadge.className = 'badge bg-success';
            
            setTimeout(() => {
                // Volta ao estado original após 2 segundos
                location.reload();
            }, 2000);
        }
    }, 1500);
}


// Exam Request Functions
function openExamRequest() {
    console.log('=== Função openExamRequest chamada ===');
    const modal = document.getElementById('examRequestModal');
    console.log('Modal encontrado:', modal);
    if (modal) {
        console.log('Adicionando classe show ao modal de exame');
        modal.classList.add('show');
        console.log('Classes do modal após adicionar show:', modal.className);
    } else {
        console.error('ERRO: Modal de solicitação de exame não encontrado no DOM!');
        alert('Erro: Modal de exame não encontrado. Verifique a estrutura HTML.');
    }
}

function closeExamRequest() {
    document.getElementById('examRequestModal').classList.remove('show');
}

function saveExamRequest() {
    const examType = document.getElementById('examType').value;
    const justification = document.getElementById('examJustification').value;
    const urgency = document.getElementById('examUrgency').value;

    if (!examType || !justification) {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return;
    }

    // Simulate generating and downloading exam request
    const examData = {
        patient: 'João Silva',
        examType: examType,
        justification: justification,
        urgency: urgency,
        date: new Date().toLocaleDateString('pt-BR'),
        doctor: 'Dr. Carlos Silva',
        crm: 'CRM/SP 123456'
    };

    generateExamRequestPDF(examData);
    alert('Solicitação de exame gerada com sucesso! O download iniciará automaticamente.');
    closeExamRequest();
    document.getElementById('examRequestForm').reset();
}

// Certificate Functions
function openCertificate() {
    console.log('=== Função openCertificate chamada ===');
    const modal = document.getElementById('certificateModal');
    console.log('Modal encontrado:', modal);
    if (modal) {
        console.log('Adicionando classe show ao modal de atestado');
        modal.classList.add('show');
        console.log('Classes do modal após adicionar show:', modal.className);
    } else {
        console.error('ERRO: Modal de atestado não encontrado no DOM!');
        alert('Erro: Modal de atestado não encontrado. Verifique a estrutura HTML.');
    }
}

function closeCertificate() {
    document.getElementById('certificateModal').classList.remove('show');
}

function saveCertificate() {
    const certificateType = document.getElementById('certificateType').value;
    const startDate = document.getElementById('certificateStartDate').value;
    const endDate = document.getElementById('certificateEndDate').value;
    const cid = document.getElementById('certificateCID').value;
    const observations = document.getElementById('certificateObservations').value;

    if (!certificateType || !startDate) {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return;
    }

    // Simulate generating and downloading certificate
    const certificateData = {
        patient: 'João Silva',
        type: certificateType,
        startDate: startDate,
        endDate: endDate,
        cid: cid,
        observations: observations,
        date: new Date().toLocaleDateString('pt-BR'),
        doctor: 'Dr. Carlos Silva',
        crm: 'CRM/SP 123456'
    };

    generateCertificatePDF(certificateData);
    alert('Atestado médico gerado com sucesso! O download iniciará automaticamente.');
    closeCertificate();
    document.getElementById('certificateForm').reset();
}

// PDF Generation Functions (simulated)
function generateExamRequestPDF(data) {
    // In a real application, this would generate a proper PDF
    const content = `
SOLICITAÇÃO DE EXAME MÉDICO

Paciente: ${data.patient}
Tipo de Exame: ${data.examType}
Urgência: ${data.urgency}
Data: ${data.date}

Justificativa Clínica:
${data.justification}

Médico Solicitante: ${data.doctor}
${data.crm}
    `;
    
    downloadTextFile(content, `solicitacao_exame_${data.patient.replace(' ', '_')}_${Date.now()}.txt`);
}

function generateCertificatePDF(data) {
    // In a real application, this would generate a proper PDF
    const content = `
ATESTADO MÉDICO

Atesto para os devidos fins que o(a) paciente ${data.patient} 
esteve sob meus cuidados médicos.

Tipo de Atestado: ${data.type}
Período: ${data.startDate} ${data.endDate ? 'a ' + data.endDate : ''}
${data.cid ? 'CID: ' + data.cid : ''}

${data.observations ? 'Observações: ' + data.observations : ''}

Data: ${data.date}

${data.doctor}
${data.crm}
    `;
    
    downloadTextFile(content, `atestado_${data.patient.replace(' ', '_')}_${Date.now()}.txt`);
}

// Enhanced prescription save with download
function savePrescription() {
    const medication = document.getElementById('medication').value;
    const dosage = document.getElementById('dosage').value;
    const frequency = document.getElementById('frequency').value;
    const duration = document.getElementById('duration').value;
    const observations = document.getElementById('observations').value;

    if (!medication || !dosage || !frequency || !duration) {
        alert('Por favor, preencha todos os campos obrigatórios.');
        return;
    }

    // Generate prescription data
    const prescriptionData = {
        patient: 'João Silva',
        medication: medication,
        dosage: dosage,
        frequency: frequency,
        duration: duration,
        observations: observations,
        date: new Date().toLocaleDateString('pt-BR'),
        doctor: 'Dr. Carlos Silva',
        crm: 'CRM/SP 123456'
    };

    generatePrescriptionPDF(prescriptionData);
    alert('Receita médica gerada com sucesso! O download iniciará automaticamente.');
    closePrescription();
    document.getElementById('prescriptionForm').reset();
}

function generatePrescriptionPDF(data) {
    // In a real application, this would generate a proper PDF
    const content = `
RECEITA MÉDICA

Paciente: ${data.patient}
Data: ${data.date}

PRESCRIÇÃO:
Medicamento: ${data.medication}
Dosagem: ${data.dosage}
Frequência: ${data.frequency}
Duração do tratamento: ${data.duration}

${data.observations ? 'Observações: ' + data.observations : ''}

${data.doctor}
${data.crm}
    `;
    
    downloadTextFile(content, `receita_${data.patient.replace(' ', '_')}_${Date.now()}.txt`);
}

// Utility function to download text files (simulating PDF download)
function downloadTextFile(content, filename) {
    const element = document.createElement('a');
    const file = new Blob([content], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = filename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// ========== INTEGRAÇÃO COM SISTEMA DE NOTIFICAÇÕES ==========

// Conectar ao WebSocket da consulta
function connectToConsultationWebSocket() {
    if (!window.consultationData || !window.consultationData.userId) {
        console.log('Dados da consulta não disponíveis para WebSocket');
        return;
    }
    
    const { userId, userType } = window.consultationData;
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/${userType}/${userId}`;
    
    console.log('Conectando ao WebSocket da consulta:', wsUrl);
    
    websocketConnection = new WebSocket(wsUrl);
    
    websocketConnection.onopen = function() {
        console.log('Conectado ao sistema de notificações da consulta');
        showConsultationNotification('Conectado ao sistema de notificações', 'success');
    };
    
    websocketConnection.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            console.log('Notificação recebida na consulta:', data);
            handleConsultationNotification(data);
        } catch (error) {
            console.error('Erro ao processar notificação da consulta:', error);
        }
    };
    
    websocketConnection.onclose = function() {
        console.log('Conexão WebSocket da consulta perdida');
        showConsultationNotification('Conexão perdida', 'warning');
        // Tentar reconectar após 3 segundos
        setTimeout(connectToConsultationWebSocket, 3000);
    };
    
    websocketConnection.onerror = function(error) {
        console.error('Erro no WebSocket da consulta:', error);
    };
}

// Tratar notificações recebidas durante a consulta
function handleConsultationNotification(data) {
    switch (data.type) {
        case 'patient_joined':
            showConsultationNotification(`${data.patient_name} entrou na consulta`, 'info');
            updateParticipantsList();
            break;
        case 'consultation_ended':
            showConsultationNotification('Consulta foi encerrada pelo outro participante', 'warning');
            setTimeout(() => {
                if (confirm('A consulta foi encerrada. Deseja sair da sala?')) {
                    window.close();
                }
            }, 2000);
            break;
        default:
            console.log('Tipo de notificação desconhecido na consulta:', data.type);
    }
}

// Mostrar notificações durante a consulta
function showConsultationNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `consultation-toast consultation-toast-${type}`;
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            <span>${message}</span>
            <button class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    // Estilos inline para a notificação
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#d4edda' : type === 'warning' ? '#fff3cd' : '#d1ecf1'};
        color: ${type === 'success' ? '#155724' : type === 'warning' ? '#856404' : '#0c5460'};
        border: 1px solid ${type === 'success' ? '#c3e6cb' : type === 'warning' ? '#ffeaa7' : '#bee5eb'};
        border-radius: 8px;
        padding: 12px 16px;
        z-index: 10000;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Atualizar lista de participantes
function updateParticipantsList() {
    console.log('Atualizando lista de participantes da consulta');
    // Implementar lógica para atualizar UI dos participantes se necessário
}

// Notificar outros participantes quando sair
function notifyConsultationEnd() {
    if (websocketConnection && websocketConnection.readyState === WebSocket.OPEN) {
        const message = {
            type: 'consultation_ended',
            user_name: window.consultationData.userName,
            user_type: window.consultationData.userType,
            timestamp: new Date().toISOString()
        };
        websocketConnection.send(JSON.stringify(message));
    }
}

// Sobrescrever função de encerrar consulta para incluir notificações
const originalEndConsultation = window.endConsultation || function() {};
function endConsultation() {
    if (confirm('Tem certeza que deseja encerrar a consulta?')) {
        // Notificar outros participantes
        notifyConsultationEnd();
        
        // Chamar função original se existir
        if (originalEndConsultation !== endConsultation) {
            originalEndConsultation();
        }
        
        // Fechar WebSocket
        if (websocketConnection) {
            websocketConnection.close();
        }
        
        // Redirecionar baseado no tipo de usuário
        const userType = window.consultationData.userType;
        if (userType === 'medico') {
            window.location.href = '/consultas_medico';
        } else {
            window.location.href = '/dashboard_paciente';
        }
    }
}

