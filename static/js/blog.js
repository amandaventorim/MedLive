function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}

// Função para filtrar artigos por categoria
function filtrarArtigos(categoria) {
    const artigos = document.querySelectorAll('.artigo-item');
    const botoes = document.querySelectorAll('.botao-filtro');

    // Atualizar botões ativos
    botoes.forEach(btn => btn.classList.remove('ativo'));
    event.target.classList.add('ativo');

    // Filtrar artigos
    artigos.forEach(artigo => {
        if (categoria === 'todos' || artigo.dataset.categoria === categoria) {
            artigo.style.display = 'block';
            artigo.classList.add('animacao-fade-in');
        } else {
            artigo.style.display = 'none';
        }
    });
}

// Função para pesquisar artigos
function pesquisarArtigos(termo) {
    const artigos = document.querySelectorAll('.artigo-item');
    const termoBusca = termo.toLowerCase();

    artigos.forEach(artigo => {
        const titulo = artigo.querySelector('.titulo-artigo').textContent.toLowerCase();
        const resumo = artigo.querySelector('.resumo-artigo').textContent.toLowerCase();
        const categoria = artigo.querySelector('.categoria-artigo').textContent.toLowerCase();

        if (titulo.includes(termoBusca) || resumo.includes(termoBusca) || categoria.includes(termoBusca)) {
            artigo.style.display = 'block';
        } else {
            artigo.style.display = 'none';
        }
    });
}

// Animações ao carregar a página
document.addEventListener('DOMContentLoaded', function () {
    const elementos = document.querySelectorAll('.animacao-fade-in, .animacao-slide-esquerda');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    elementos.forEach(elemento => {
        elemento.style.opacity = '0';
        elemento.style.transform = 'translateY(20px)';
        elemento.style.transition = 'all 0.6s ease';
        observer.observe(elemento);
    });
});