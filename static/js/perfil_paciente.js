function editarSecao(secao) {
    console.log('Editando seção:', secao);
    // Aqui você pode implementar a lógica de edição inline
}

// Adicionar funcionalidade aos botões de ação rápida
document.querySelectorAll('.botao-medlive, .botao-secundario').forEach(botao => {
    botao.addEventListener('click', function () {
        if (!this.hasAttribute('data-bs-toggle')) {
            console.log('Ação:', this.textContent.trim());
        }
    });
});