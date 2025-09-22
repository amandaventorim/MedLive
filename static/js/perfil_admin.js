function editarSecao(secao) {
    console.log('Editando seção:', secao);
    // Aqui você pode implementar a lógica de edição inline
}

function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}


// Adicionar funcionalidade aos botões de ação rápida
document.querySelectorAll('.botao-medlive, .botao-secundario').forEach(botao => {
    botao.addEventListener('click', function () {
        if (!this.hasAttribute('data-bs-toggle')) {
            console.log('Ação:', this.textContent.trim());
        }
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);

    if (urlParams.get('foto_sucesso') === '1') {
        // Limpar parâmetro da URL sem mostrar mensagem
        window.history.replaceState({}, document.title, window.location.pathname);
    }

    if (urlParams.get('erro') === 'tipo_invalido') {
        alert('Erro: Tipo de arquivo não permitido. Use apenas JPG, PNG ou WEBP.');
        window.history.replaceState({}, document.title, window.location.pathname);
    }

    if (urlParams.get('erro') === 'arquivo_muito_grande') {
        alert('Erro: Arquivo muito grande. Tamanho máximo: 5MB.');
        window.history.replaceState({}, document.title, window.location.pathname);
    }

    if (urlParams.get('erro') === 'upload_falhou') {
        alert('Erro: Falha no upload. Tente novamente.');
        window.history.replaceState({}, document.title, window.location.pathname);
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const fotoInput = document.getElementById('foto');
    const fotoPreview = document.querySelector('#modalEditarFoto .foto-usuario');

    if (fotoInput && fotoPreview) {
        fotoInput.addEventListener('change', function (e) {
            const file = e.target.files[0];

            if (file) {
                // Verificar se é uma imagem
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();

                    reader.onload = function (e) {
                        // Atualizar preview no modal
                        fotoPreview.src = e.target.result;
                    };

                    reader.readAsDataURL(file);
                } else {
                    alert('Por favor, selecione apenas arquivos de imagem.');
                    fotoInput.value = '';
                }
            }
        });
    }
});

