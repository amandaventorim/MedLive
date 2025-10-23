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
    
    // Aplicar ícones nas especialidades
    aplicarIconesEspecialidades();
});

// Mapeamento de especialidades para ícones do Bootstrap Icons
function getIconeEspecialidade(nomeEspecialidade) {
    const nome = nomeEspecialidade.toLowerCase().trim();
    
    const iconMap = {
        'cardiologia': 'bi-heart-pulse',
        'dermatologia': 'bi-person-check',
        'clínica geral': 'bi-hospital',
        'clinica geral': 'bi-hospital',
        'pediatria': 'bi-emoji-smile',
        'ginecologia': 'bi-gender-female',
        'neurologia': 'bi-hammer',
        'ortopedia': 'bi-bandaid',
        'psiquiatria': 'bi-brain',
        'oftalmologia': 'bi-eye',
        'otorrinolaringologia': 'bi-ear',
        'urologia': 'bi-droplet',
        'gastroenterologia': 'bi-brightness-high',
        'endocrinologia': 'bi-activity',
        'pneumologia': 'bi-lungs',
        'nefrologia': 'bi-water',
        'reumatologia': 'bi-person-arms-up',
        'oncologia': 'bi-shield-plus',
        'hematologia': 'bi-heart',
        'infectologia': 'bi-bug',
        'geriatria': 'bi-person-walking',
        'anestesiologia': 'bi-hourglass-split',
        'radiologia': 'bi-camera',
        'cirurgia geral': 'bi-scissors',
        'medicina do trabalho': 'bi-briefcase'
    };
    
    return iconMap[nome] || 'bi-heart-pulse'; // Ícone padrão
}

function aplicarIconesEspecialidades() {
    const icones = document.querySelectorAll('.esp-icon-dashboard');
    icones.forEach(icone => {
        const nomeEspecialidade = icone.getAttribute('data-especialidade');
        const classIcone = getIconeEspecialidade(nomeEspecialidade);
        icone.className = `bi ${classIcone}`;
    });
}
