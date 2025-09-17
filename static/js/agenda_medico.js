function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    navbarNav.classList.toggle('show');
}

function mesAnterior() {
            // Implementar lógica para mês anterior
            console.log('Mês anterior');
        }

        function proximoMes() {
            // Implementar lógica para próximo mês
            console.log('Próximo mês');
        }

        // Adicionar interatividade aos dias do calendário
        document.querySelectorAll('.dia-calendario').forEach(dia => {
            dia.addEventListener('click', function() {
                // Remover seleção anterior
                document.querySelectorAll('.dia-calendario').forEach(d => d.classList.remove('selecionado'));
                // Adicionar seleção ao dia clicado
                this.classList.add('selecionado');
            });
        });

