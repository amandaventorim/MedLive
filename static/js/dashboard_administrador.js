function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}

// Função para alternar entre as seções do dashboard
function mostrarSecao(secaoNome) {
    // Remove a classe 'active' de todas as seções
    const todasSecoes = document.querySelectorAll('.admin-section');
    todasSecoes.forEach(secao => {
        secao.classList.remove('active');
    });

    // Remove a classe 'active' de todos os botões de tab
    const todosBotoes = document.querySelectorAll('.tab-button');
    todosBotoes.forEach(botao => {
        botao.classList.remove('active');
    });

    // Adiciona a classe 'active' na seção selecionada
    const secaoSelecionada = document.getElementById('secao-' + secaoNome);
    if (secaoSelecionada) {
        secaoSelecionada.classList.add('active');
    }

    // Adiciona a classe 'active' no botão clicado
    // Procura o botão que foi clicado usando event ou procurando pelo onclick
    const botoes = document.querySelectorAll('.tab-button');
    botoes.forEach(botao => {
        if (botao.getAttribute('onclick') && botao.getAttribute('onclick').includes(secaoNome)) {
            botao.classList.add('active');
        }
    });
}

// Quando a página carregar, garante que a primeira seção esteja ativa
document.addEventListener('DOMContentLoaded', function() {
    // Verifica se já existe uma seção ativa, senão ativa a primeira
    const secaoAtiva = document.querySelector('.admin-section.active');
    if (!secaoAtiva) {
        mostrarSecao('medicos');
    }
});
