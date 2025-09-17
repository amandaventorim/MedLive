function editarSecao(secao) {
    console.log('Editando seção:', secao);
    // Aqui você pode implementar a lógica de edição inline
}

// Adicionar funcionalidade aos switches de horário
document.querySelectorAll('.switch-disponibilidade input').forEach(switch_ => {
    switch_.addEventListener('change', function () {
        const horarioItem = this.closest('.horario-item');
        const periodo = horarioItem.querySelector('.horario-periodo');

        if (this.checked) {
            periodo.textContent = '08:00 - 18:00';
            periodo.style.color = '#6c757d';
        } else {
            periodo.textContent = 'Indisponível';
            periodo.style.color = '#dc3545';
        }
    });
});



// Preview de foto de perfil
document.addEventListener('DOMContentLoaded', function() {
    const fotoInput = document.getElementById('foto');
    const fotoPreview = document.querySelector('#modalEditarFoto .foto-usuario');

    if (fotoInput && fotoPreview) {
        fotoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];

            if (file) {
                // Verificar se é uma imagem
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();

                    reader.onload = function(e) {
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
