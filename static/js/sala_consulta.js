let consultationStartTime = Date.now();
let micMuted = false;
let cameraOff = false;
let screenSharing = false;
let recording = false;

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
    document.getElementById('prescriptionModal').classList.add('show');
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
    simulateConnectionChanges();
    simulatePatientMessages();

    // Get patient info from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const patientId = urlParams.get('patient');

    if (patientId) {
        // Load patient-specific data
        console.log('Loading data for patient:', patientId);
    }
});