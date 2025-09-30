let currentStep = 1;
let selectedDate = null;
let selectedTime = null;
let currentMonth = new Date();

const months = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
];

function initializePage() {
    const selectedDoctor = JSON.parse(localStorage.getItem('selectedDoctor') || '{}');
    
    // Tentar obter o ID do médico da URL se não estiver no localStorage
    const urlParams = new URLSearchParams(window.location.search);
    const idMedicoFromUrl = urlParams.get('idMedico');
    
    if (idMedicoFromUrl) {
        document.getElementById('inputIdMedico').value = idMedicoFromUrl;
    }

    if (selectedDoctor.name) {
        document.getElementById('doctorName').textContent = selectedDoctor.name;
        document.getElementById('doctorSpecialty').textContent = selectedDoctor.specialty;
        document.getElementById('doctorCrm').textContent = `${selectedDoctor.crm} • ${selectedDoctor.experience}`;
        document.getElementById('doctorRating').textContent = `${'★'.repeat(Math.floor(selectedDoctor.rating))}${'☆'.repeat(5 - Math.floor(selectedDoctor.rating))} ${selectedDoctor.rating} (${selectedDoctor.reviews} avaliações)`;
        document.getElementById('doctorAvatar').textContent = selectedDoctor.name.split(' ').map(n => n[0]).join('');

        document.getElementById('summaryDoctor').textContent = selectedDoctor.name;
        document.getElementById('summarySpecialty').textContent = selectedDoctor.specialty;
        
        // Preencher o ID do médico no campo hidden
        if (selectedDoctor.id) {
            document.getElementById('inputIdMedico').value = selectedDoctor.id;
        }
    } else if (idMedicoFromUrl) {
        // Se não há dados no localStorage mas há ID na URL, mostrar mensagem
        document.getElementById('doctorName').textContent = `Médico ID: ${idMedicoFromUrl}`;
        document.getElementById('summaryDoctor').textContent = `Médico ID: ${idMedicoFromUrl}`;
    }

    generateCalendar();
    addStepClickListeners();
}

function selectConsultationType(type, price) {
    // Função removida pois não há mais escolha de tipo de consulta
    // O fluxo começa na escolha da data
}

function generateCalendar() {
    const grid = document.getElementById('calendarGrid');
    const monthDisplay = document.getElementById('currentMonth');

    monthDisplay.textContent = `${months[currentMonth.getMonth()]} ${currentMonth.getFullYear()}`;

    // Clear grid
    grid.innerHTML = '';

    // Add day headers
    const dayHeaders = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
    dayHeaders.forEach(day => {
        const dayHeader = document.createElement('div');
        dayHeader.className = 'calendar-day-header';
        dayHeader.textContent = day;
        grid.appendChild(dayHeader);
    });

    // Get first day of month and number of days
    const firstDay = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), 1);
    const lastDay = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 0);
    const today = new Date();
    
    // Data limite (6 meses no futuro)
    const limiteFuturo = new Date();
    limiteFuturo.setMonth(limiteFuturo.getMonth() + 6);

    // Add empty cells for days before month starts
    for (let i = 0; i < firstDay.getDay(); i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar-day';
        grid.appendChild(emptyDay);
    }

    // Add days of month
    for (let day = 1; day <= lastDay.getDate(); day++) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';
        dayElement.textContent = day;

        const dayDate = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), day);

        // Validações de data
        if (dayDate < today) {
            dayElement.classList.add('unavailable');
            dayElement.title = 'Data no passado';
        } else if (dayDate > limiteFuturo) {
            dayElement.classList.add('unavailable');
            dayElement.title = 'Data muito longe no futuro (máximo 6 meses)';
        } else if (dayDate.getDay() === 0) { // Domingo
            dayElement.classList.add('unavailable');
            dayElement.title = 'Não há atendimento aos domingos';
        } else {
            dayElement.classList.add('available');
            dayElement.onclick = () => selectDate(day);
        }

        grid.appendChild(dayElement);
    }
}

function selectDate(day) {
    // Remove previous selection
    document.querySelectorAll('.calendar-day').forEach(dayEl => {
        dayEl.classList.remove('selected');
    });

    // Add selection to clicked day
    event.currentTarget.classList.add('selected');

    selectedDate = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), day);

    const dateStr = selectedDate.toLocaleDateString('pt-BR', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    document.getElementById('summaryDate').textContent = dateStr;

    setTimeout(() => {
        nextStep();
    }, 500);
}

function generateTimeSlots() {
    const timeSlotsContainer = document.getElementById('timeSlots');
    const selectedDateDisplay = document.getElementById('selectedDateDisplay');

    const dateStr = selectedDate.toLocaleDateString('pt-BR', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    selectedDateDisplay.innerHTML = `<strong>Data selecionada:</strong> ${dateStr}`;

    // Mostrar loading
    timeSlotsContainer.innerHTML = '<div class="text-center p-3"><i class="bi bi-hourglass-split"></i> Carregando horários disponíveis...</div>';

    // Obter ID do médico
    const idMedico = document.getElementById('inputIdMedico').value;
    if (!idMedico) {
        timeSlotsContainer.innerHTML = '<div class="alert alert-warning">Erro: ID do médico não encontrado.</div>';
        return;
    }

    // Formatar data para API (YYYY-MM-DD)
    const dataFormatada = selectedDate.toISOString().split('T')[0];

    // Buscar horários disponíveis da API
    fetch(`/api/horarios-disponiveis?idMedico=${idMedico}&data=${dataFormatada}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro na API: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            timeSlotsContainer.innerHTML = '';

            if (data.success && data.horarios && data.horarios.length > 0) {
                data.horarios.forEach(horario => {
                    const timeSlot = document.createElement('div');
                    timeSlot.className = 'time-slot';
                    timeSlot.textContent = horario;
                    timeSlot.onclick = () => selectTime(horario);
                    timeSlot.title = 'Clique para selecionar este horário';
                    timeSlotsContainer.appendChild(timeSlot);
                });
            } else {
                timeSlotsContainer.innerHTML = `
                    <div class="alert alert-info">
                        <i class="bi bi-info-circle me-2"></i>
                        ${data.message || 'Nenhum horário disponível para esta data.'}
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Erro ao carregar horários:', error);
            timeSlotsContainer.innerHTML = `
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle me-2"></i>
                    Erro ao carregar horários disponíveis. Tente recarregar a página.
                </div>
            `;
        });
}

function selectTime(time) {
    // Remove previous selection
    document.querySelectorAll('.time-slot').forEach(slot => {
        slot.classList.remove('selected');
    });

    // Add selection to clicked slot
    event.currentTarget.classList.add('selected');

    selectedTime = time;
    document.getElementById('summaryTime').textContent = time;

    setTimeout(() => {
        nextStep();
    }, 500);
}

function previousMonth() {
    currentMonth.setMonth(currentMonth.getMonth() - 1);
    generateCalendar();
}

function nextMonth() {
    currentMonth.setMonth(currentMonth.getMonth() + 1);
    generateCalendar();
}

function nextStep() {
    // Hide current step
    document.getElementById(`step${currentStep}`).classList.remove('active');
    document.getElementById(`step${currentStep}`).classList.add('completed');

    if (currentStep === 1) {
        document.getElementById('dateSelectionStep').style.display = 'none';
        document.getElementById('timeSelectionStep').style.display = 'block';
        generateTimeSlots();
    } else if (currentStep === 2) {
        document.getElementById('timeSelectionStep').style.display = 'none';
        document.getElementById('additionalInfoStep').style.display = 'block';
        document.getElementById('confirmButton').disabled = false;
    }

    currentStep++;
    if (currentStep <= 3) {
        document.getElementById(`step${currentStep}`).classList.add('active');
    }
}

function goToStep(stepNumber) {
    // Não permitir ir para passos futuros se não completou os anteriores
    if (stepNumber > currentStep && !canGoToStep(stepNumber)) {
        return;
    }

    // Atualizar estado visual dos passos
    updateStepIndicators(stepNumber);

    // Esconder todos os passos
    document.getElementById('dateSelectionStep').style.display = 'none';
    document.getElementById('timeSelectionStep').style.display = 'none';
    document.getElementById('additionalInfoStep').style.display = 'none';

    // Mostrar o passo selecionado
    if (stepNumber === 1) {
        document.getElementById('dateSelectionStep').style.display = 'block';
    } else if (stepNumber === 2) {
        document.getElementById('timeSelectionStep').style.display = 'block';
        if (selectedDate) {
            generateTimeSlots();
        }
    } else if (stepNumber === 3) {
        document.getElementById('additionalInfoStep').style.display = 'block';
        document.getElementById('confirmButton').disabled = !isAllDataValid();
    }

    currentStep = stepNumber;
}

function canGoToStep(stepNumber) {
    switch (stepNumber) {
        case 1:
            return true;
        case 2:
            return selectedDate !== null;
        case 3:
            return selectedDate !== null && selectedTime !== null;
        default:
            return false;
    }
}

function updateStepIndicators(activeStep) {
    for (let i = 1; i <= 3; i++) {
        const stepElement = document.getElementById(`step${i}`);
        stepElement.classList.remove('active', 'completed');
        
        if (i < activeStep) {
            stepElement.classList.add('completed');
        } else if (i === activeStep) {
            stepElement.classList.add('active');
        }
    }
}

function isAllDataValid() {
    return selectedDate !== null && selectedTime !== null;
}

function addStepClickListeners() {
    for (let i = 1; i <= 3; i++) {
        const stepElement = document.getElementById(`step${i}`);
        stepElement.style.cursor = 'pointer';
        stepElement.addEventListener('click', () => goToStep(i));
    }
}

function confirmAppointment() {
    // ===== VALIDAÇÕES FRONTEND =====
    
    // 1. Validar termos aceitos
    const termsAccepted = document.getElementById('termsAccepted').checked;
    if (!termsAccepted) {
        alert('Por favor, aceite os termos de uso para continuar.');
        return false;
    }
    
    // 2. Validar se o médico foi selecionado
    const idMedico = document.getElementById('inputIdMedico').value;
    if (!idMedico || idMedico === '') {
        alert('Erro: Nenhum médico foi selecionado. Por favor, volte à busca de médicos e selecione um médico.');
        return false;
    }
    
    // 3. Validar se data foi selecionada
    if (!selectedDate) {
        alert('Por favor, selecione uma data para a consulta.');
        return false;
    }
    
    // 4. Validar se horário foi selecionado
    if (!selectedTime) {
        alert('Por favor, selecione um horário para a consulta.');
        return false;
    }
    
    // 5. Validar motivo da consulta
    const consultationReason = document.getElementById('consultationReason').value.trim();
    if (!consultationReason) {
        alert('Por favor, descreva o motivo da consulta.');
        document.getElementById('consultationReason').focus();
        return false;
    }
    
    if (consultationReason.length < 10) {
        alert('O motivo da consulta deve ter pelo menos 10 caracteres.');
        document.getElementById('consultationReason').focus();
        return false;
    }
    
    if (consultationReason.length > 500) {
        alert('O motivo da consulta deve ter no máximo 500 caracteres.');
        document.getElementById('consultationReason').focus();
        return false;
    }
    
    // 6. Validar data não é no passado (double-check)
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    if (selectedDate < hoje) {
        alert('Não é possível agendar consultas para datas passadas.');
        return false;
    }
    
    // 7. Validar que não é domingo
    if (selectedDate.getDay() === 0) {
        alert('Não há atendimento aos domingos. Por favor, selecione outra data.');
        return false;
    }
    
    // ===== PREENCHIMENTO DOS CAMPOS =====
    
    try {
        // Preenche os campos do formulário antes de enviar
        document.getElementById('inputDate').value = selectedDate.toISOString().split('T')[0];
        document.getElementById('inputTime').value = selectedTime;
        document.getElementById('inputQueixa').value = consultationReason;
        
        // Confirmar com o usuário
        const confirmMsg = `Confirmar agendamento para ${selectedDate.toLocaleDateString('pt-BR')} às ${selectedTime}?`;
        if (confirm(confirmMsg)) {
            // Desabilitar botão para evitar duplo clique
            const confirmButton = document.getElementById('confirmButton');
            confirmButton.disabled = true;
            confirmButton.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Processando...';
            
            // Enviar formulário
            document.getElementById('agendarForm').submit();
            return true;
        }
        
    } catch (error) {
        console.error('Erro ao processar agendamento:', error);
        alert('Erro ao processar dados. Tente novamente.');
        return false;
    }
    
    return false;
}

function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
    
    // Configurar evento do botão de confirmação
    document.getElementById('confirmButton').onclick = function(e) {
        e.preventDefault();
        confirmAppointment();
    };
    
    // Adicionar validação em tempo real para o motivo da consulta
    const consultationReason = document.getElementById('consultationReason');
    if (consultationReason) {
        consultationReason.addEventListener('input', function() {
            const value = this.value.trim();
            const charCount = value.length;
            
            // Criar ou atualizar contador de caracteres
            let counter = document.getElementById('char-counter');
            if (!counter) {
                counter = document.createElement('small');
                counter.id = 'char-counter';
                counter.className = 'text-muted';
                this.parentNode.appendChild(counter);
            }
            
            counter.textContent = `${charCount}/500 caracteres`;
            
            // Validação visual
            if (charCount < 10) {
                this.style.borderColor = '#dc3545';
                counter.textContent += ' (mínimo 10)';
                counter.style.color = '#dc3545';
            } else if (charCount > 500) {
                this.style.borderColor = '#dc3545';
                counter.style.color = '#dc3545';
            } else {
                this.style.borderColor = '#198754';
                counter.style.color = '#198754';
            }
        });
    }
});