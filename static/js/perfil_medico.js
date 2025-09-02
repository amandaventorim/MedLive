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