function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}

// Função para enviar mensagem
function enviarMensagem(event) {
    event.preventDefault();

    // Simular envio da mensagem
    const botao = event.target.querySelector('.botao-enviar');
    const textoOriginal = botao.innerHTML;

    botao.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Enviando...';
    botao.disabled = true;

    setTimeout(() => {
        botao.innerHTML = '<i class="bi bi-check-circle me-2"></i>Mensagem Enviada!';
        botao.style.background = 'linear-gradient(135deg, #28a745 0%, #20c997 100%)';

        setTimeout(() => {
            botao.innerHTML = textoOriginal;
            botao.disabled = false;
            botao.style.background = '';
            event.target.reset();
        }, 3000);
    }, 2000);
}

// Função para alternar respostas do FAQ
function toggleResposta(numero) {
    const resposta = document.getElementById(`resposta${numero}`);
    const pergunta = event.target;
    const icone = pergunta.querySelector('i');

    // Fechar todas as outras respostas
    document.querySelectorAll('.resposta-faq').forEach(r => {
        if (r !== resposta) {
            r.classList.remove('ativa');
        }
    });

    // Resetar todos os ícones
    document.querySelectorAll('.pergunta-faq i').forEach(i => {
        if (i !== icone) {
            i.className = 'bi bi-plus-circle me-2';
        }
    });

    // Alternar resposta atual
    if (resposta.classList.contains('ativa')) {
        resposta.classList.remove('ativa');
        icone.className = 'bi bi-plus-circle me-2';
    } else {
        resposta.classList.add('ativa');
        icone.className = 'bi bi-dash-circle me-2';
    }
}

// Animações ao carregar a página
document.addEventListener('DOMContentLoaded', function () {
    const elementos = document.querySelectorAll('.animacao-fade-in, .animacao-slide-esquerda, .animacao-slide-direita');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0) translateX(0)';
            }
        });
    });

    elementos.forEach(elemento => {
        elemento.style.opacity = '0';
        elemento.style.transition = 'all 0.6s ease';

        if (elemento.classList.contains('animacao-slide-esquerda')) {
            elemento.style.transform = 'translateX(-30px)';
        } else if (elemento.classList.contains('animacao-slide-direita')) {
            elemento.style.transform = 'translateX(30px)';
        } else {
            elemento.style.transform = 'translateY(20px)';
        }

        observer.observe(elemento);
    });
});