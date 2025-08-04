let selectedPaymentMethod = null;

function initializePage() {
    const appointmentData = JSON.parse(localStorage.getItem('appointmentData') || '{}');

    if (appointmentData.doctor) {
        const consultationType = appointmentData.type === 'video' ? 'Videochamada' : 'Chat';
        document.getElementById('summaryConsultation').textContent = `${consultationType} - ${appointmentData.specialty}`;
        document.getElementById('summaryDoctor').textContent = appointmentData.doctor;

        const dateStr = new Date(appointmentData.date).toLocaleDateString('pt-BR');
        document.getElementById('summaryDateTime').textContent = `${dateStr} às ${appointmentData.time}`;

        const price = appointmentData.price;
        const fee = 5;
        const total = price + fee;

        document.getElementById('consultationPrice').textContent = `R$ ${price.toFixed(2).replace('.', ',')}`;
        document.getElementById('totalPrice').textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
    }
}

function selectPaymentMethod(method) {
    // Remove previous selection
    document.querySelectorAll('.payment-method').forEach(pm => {
        pm.classList.remove('selected');
    });

    // Hide all forms
    document.getElementById('creditCardForm').classList.remove('show');
    document.getElementById('pixQr').classList.remove('show');

    // Add selection to clicked method
    event.currentTarget.classList.add('selected');
    selectedPaymentMethod = method;

    // Show relevant form
    if (method === 'credit') {
        document.getElementById('creditCardForm').classList.add('show');
    } else if (method === 'pix') {
        document.getElementById('pixQr').classList.add('show');
    }

    // Enable pay button
    document.getElementById('payButton').disabled = false;
}

function formatCardNumber(input) {
    let value = input.value.replace(/\s/g, '').replace(/[^0-9]/gi, '');
    let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;

    input.value = formattedValue;

    // Update card display
    const display = document.getElementById('cardNumberDisplay');
    if (value.length > 0) {
        const masked = value.replace(/(.{4})/g, '$1 ').trim();
        const remaining = 16 - value.length;
        const dots = '•'.repeat(remaining);
        display.textContent = masked + ' ' + dots.match(/.{1,4}/g)?.join(' ');
    } else {
        display.textContent = '•••• •••• •••• ••••';
    }
}

function updateCardHolder(input) {
    const display = document.getElementById('cardHolderDisplay');
    display.textContent = input.value.toUpperCase() || 'NOME DO TITULAR';
}

function formatExpiry(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length >= 2) {
        value = value.substring(0, 2) + '/' + value.substring(2, 4);
    }
    input.value = value;

    // Update card display
    const display = document.getElementById('cardExpiryDisplay');
    display.textContent = value || '••/••';
}

function copyPixCode() {
    const pixCode = document.querySelector('.pix-code').textContent;
    navigator.clipboard.writeText(pixCode).then(() => {
        alert('Código PIX copiado para a área de transferência!');
    });
}

function processPayment() {
    if (!selectedPaymentMethod) {
        alert('Por favor, selecione uma forma de pagamento.');
        return;
    }

    // Validate credit card if selected
    if (selectedPaymentMethod === 'credit') {
        const cardNumber = document.getElementById('cardNumber').value;
        const cardHolder = document.getElementById('cardHolder').value;
        const cardExpiry = document.getElementById('cardExpiry').value;
        const cardCvv = document.getElementById('cardCvv').value;

        if (!cardNumber || !cardHolder || !cardExpiry || !cardCvv) {
            alert('Por favor, preencha todos os dados do cartão.');
            return;
        }
    }

    // Hide payment methods and show loading
    document.getElementById('paymentMethods').style.display = 'none';
    document.getElementById('loadingPayment').style.display = 'block';

    // Simulate payment processing
    setTimeout(() => {
        document.getElementById('loadingPayment').style.display = 'none';
        document.getElementById('successAnimation').style.display = 'block';

        // Save appointment to localStorage
        const appointmentData = JSON.parse(localStorage.getItem('appointmentData') || '{}');
        appointmentData.status = 'confirmed';
        appointmentData.paymentMethod = selectedPaymentMethod;
        appointmentData.paymentDate = new Date().toISOString();

        const appointments = JSON.parse(localStorage.getItem('appointments') || '[]');
        appointments.push(appointmentData);
        localStorage.setItem('appointments', JSON.stringify(appointments));

        // Clear appointment data
        localStorage.removeItem('appointmentData');
        localStorage.removeItem('selectedDoctor');
    }, 3000);
}

function goToDashboard() {
    window.location.href = 'minhas_consultas.html';
}

function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}

// Initialize page
document.addEventListener('DOMContentLoaded', initializePage);