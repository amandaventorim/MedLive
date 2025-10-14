function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}

document.querySelectorAll('.cartao-metodo').forEach(cartao => {
    cartao.addEventListener('click', function () {
        // Remover classe ativo de todos
        document.querySelectorAll('.cartao-metodo').forEach(c => c.classList.remove('ativo'));
        // Adicionar classe ativo ao clicado
        this.classList.add('ativo');
    });
});

// Adicionar funcionalidade aos botões de upgrade
document.querySelectorAll('.botao-plano:not(.atual)').forEach(botao => {
    botao.addEventListener('click', function () {
        // Aqui você pode adicionar lógica para abrir modal de upgrade
        console.log('Upgrade de plano solicitado');
    });
});