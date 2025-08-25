let currentStep = 1;
let selectedConsultationType = null;
let selectedPrice = 0;
let selectedDate = null;
let selectedTime = null;
let currentMonth = new Date();

const months = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
];

const timeSlots = [
    '08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
    '11:00', '11:30', '14:00', '14:30', '15:00', '15:30',
    '16:00', '16:30', '17:00', '17:30', '18:00'
];

function initializePage() {
    const selectedDoctor = JSON.parse(localStorage.getItem('selectedDoctor') || '{}');

    if (selectedDoctor.name) {
        document.getElementById('doctorName').textContent = selectedDoctor.name;
        document.getElementById('doctorSpecialty').textContent = selectedDoctor.specialty;
        document.getElementById('doctorCrm').textContent = `${selectedDoctor.crm} • ${selectedDoctor.experience}`;
        document.getElementById('doctorRating').textContent = `${'★'.repeat(Math.floor(selectedDoctor.rating))}${'☆'.repeat(5 - Math.floor(selectedDoctor.rating))} ${selectedDoctor.rating} (${selectedDoctor.reviews} avaliações)`;
        document.getElementById('doctorAvatar').textContent = selectedDoctor.name.split(' ').map(n => n[0]).join('');

        document.getElementById('summaryDoctor').textContent = selectedDoctor.name;
        document.getElementById('summarySpecialty').textContent = selectedDoctor.specialty;
    }

    generateCalendar();
}

function selectConsultationType(type, price) {
    // Remove previous selection
    document.querySelectorAll('.consultation-type-card').forEach(card => {
        card.classList.remove('selected');
    });

    // Add selection to clicked card
    event.currentTarget.classList.add('selected');

    selectedConsultationType = type;
    selectedPrice = price;

    document.getElementById('summaryType').textContent = type === 'video' ? 'Videochamada' : 'Chat';
    document.getElementById('summaryPrice').textContent = `R$ ${price.toFixed(2).replace('.', ',')}`;

    setTimeout(() => {
        nextStep();
    }, 500);
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

        if (dayDate < today) {
            dayElement.classList.add('unavailable');
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

    timeSlotsContainer.innerHTML = '';

    timeSlots.forEach(time => {
        const timeSlot = document.createElement('div');
        timeSlot.className = 'time-slot';
        timeSlot.textContent = time;

        // Randomly make some slots unavailable for demo
        if (Math.random() > 0.7) {
            timeSlot.classList.add('unavailable');
        } else {
            timeSlot.onclick = () => selectTime(time);
        }

        timeSlotsContainer.appendChild(timeSlot);
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
        document.getElementById('consultationTypeStep').style.display = 'none';
        document.getElementById('dateSelectionStep').style.display = 'block';
    } else if (currentStep === 2) {
        document.getElementById('dateSelectionStep').style.display = 'none';
        document.getElementById('timeSelectionStep').style.display = 'block';
        generateTimeSlots();
    } else if (currentStep === 3) {
        document.getElementById('timeSelectionStep').style.display = 'none';
        document.getElementById('additionalInfoStep').style.display = 'block';
        document.getElementById('confirmButton').disabled = false;
    }

    currentStep++;
    if (currentStep <= 4) {
        document.getElementById(`step${currentStep}`).classList.add('active');
    }
}

function confirmAppointment() {
    const termsAccepted = document.getElementById('termsAccepted').checked;

    if (!termsAccepted) {
        alert('Por favor, aceite os termos de uso para continuar.');
        return;
    }

    const appointmentData = {
        doctor: document.getElementById('summaryDoctor').textContent,
        specialty: document.getElementById('summarySpecialty').textContent,
        type: selectedConsultationType,
        date: selectedDate,
        time: selectedTime,
        price: selectedPrice,
        reason: document.getElementById('consultationReason').value,
        symptoms: document.getElementById('symptoms').value
    };

    localStorage.setItem('appointmentData', JSON.stringify(appointmentData));
    window.location.href = '/pagamento';
}

function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}

// Initialize page
document.addEventListener('DOMContentLoaded', initializePage);