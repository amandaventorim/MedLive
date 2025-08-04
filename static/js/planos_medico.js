function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}

function selectPlan(planType, price) {
    if (planType === 'standard') {
        alert('Este é seu plano atual.');
        return;
    }

    if (planType === 'enterprise') {
        alert('Redirecionando para contato com vendas...');
        // In a real application, this would open a contact form or redirect
        return;
    }

    const confirmMessage = `Deseja ${planType === 'basic' ? 'fazer downgrade' : 'fazer upgrade'} para o plano ${planType.charAt(0).toUpperCase() + planType.slice(1)} por R$ ${price}/mês?`;

    if (confirm(confirmMessage)) {
        // Simulate plan change
        alert('Redirecionando para pagamento...');
        // In a real application, this would redirect to payment page
        window.location.href = 'pagamento_plano.html?plan=' + planType + '&price=' + price;
    }
}

function showUpgradeModal() {
    alert('Mostrando opções de upgrade...');
    // In a real application, this would show a modal with upgrade options
}

function showUsageHistory() {
    alert('Mostrando histórico detalhado de uso...');
    // In a real application, this would show detailed usage history
}

function toggleFaq(element) {
    const answer = element.nextElementSibling;
    const icon = element.querySelector('i');

    if (answer.classList.contains('show')) {
        answer.classList.remove('show');
        icon.classList.remove('bi-chevron-up');
        icon.classList.add('bi-chevron-down');
    } else {
        // Close all other FAQs
        document.querySelectorAll('.faq-answer.show').forEach(faq => {
            faq.classList.remove('show');
        });
        document.querySelectorAll('.faq-question i').forEach(i => {
            i.classList.remove('bi-chevron-up');
            i.classList.add('bi-chevron-down');
        });

        // Open clicked FAQ
        answer.classList.add('show');
        icon.classList.remove('bi-chevron-down');
        icon.classList.add('bi-chevron-up');
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', function () {
    // Load current plan data if available
    const planData = JSON.parse(localStorage.getItem('currentPlan') || '{}');

    // Simulate real-time minute updates
    setInterval(() => {
        const minutesElement = document.querySelector('.minutes-display h3');
        if (minutesElement && Math.random() > 0.98) { // 2% chance to decrease
            let currentMinutes = parseInt(minutesElement.textContent);
            currentMinutes = Math.max(0, currentMinutes - 1);
            minutesElement.textContent = currentMinutes + ' min';

            // Update progress bar
            const progressBar = document.querySelector('.minutes-progress-bar');
            const percentage = (currentMinutes / 500) * 100;
            progressBar.style.width = percentage + '%';
        }
    }, 30000); // Check every 30 seconds
});