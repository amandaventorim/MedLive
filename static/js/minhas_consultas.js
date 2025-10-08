// Arquivo limpo - apenas funcionalidades reais para consultas

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar interações com consultas reais do backend
    initializeConsultationInteractions();
    
    // Configurar filtros apenas se houver consultas
    const consultationsList = document.getElementById('consultationsList');
    if (consultationsList && consultationsList.children.length > 0) {
        initializeFilters();
    }
});

// Função para inicializar interações com consultas
function initializeConsultationInteractions() {
    // Botões de cancelar consulta
    document.querySelectorAll('.btn-cancelar[data-consulta-id]').forEach(button => {
        button.addEventListener('click', function() {
            const consultaId = this.getAttribute('data-consulta-id');
            cancelConsultation(consultaId);
        });
    });
    
    // Botões de detalhes
    document.querySelectorAll('.btn-azul-claro[data-consulta-id]').forEach(button => {
        button.addEventListener('click', function() {
            const consultaId = this.getAttribute('data-consulta-id');
            viewDetails(consultaId);
        });
    });
    
    // Botões de entrar na consulta
    document.querySelectorAll('.btn-join[data-consulta-id]').forEach(button => {
        button.addEventListener('click', function() {
            const consultaId = this.getAttribute('data-consulta-id');
            joinConsultation(consultaId);
        });
    });
    
    // Botões de reagendar
    document.querySelectorAll('.btn-verde[data-consulta-id]').forEach(button => {
        button.addEventListener('click', function() {
            const consultaId = this.getAttribute('data-consulta-id');
            rescheduleConsultation(consultaId);
        });
    });
}

// Função para entrar na sala de consulta
function joinConsultation(id) {
    window.location.href = '/sala_consulta?id=' + id;
}

// Função para cancelar consulta
function cancelConsultation(id) {
    if (confirm('Tem certeza que deseja cancelar esta consulta?')) {
        fetch('/cancelar_consulta/' + id, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.sucesso) {
                alert('Consulta cancelada com sucesso!');
                location.reload();
            } else {
                alert('Erro ao cancelar consulta: ' + data.erro);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao cancelar consulta');
        });
    }
}

// Função para ver detalhes da consulta
function viewDetails(id) {
    window.location.href = '/detalhes_consulta/' + id;
}

// Função para reagendar consulta
function rescheduleConsultation(id) {
    window.location.href = '/agendar_consulta?reagendar=' + id;
}

// Função para agendar novamente (para consultas canceladas/concluídas)
function bookAgain(id) {
    window.location.href = '/agendar_consulta';
}

// Funções de filtro para as consultas reais
function initializeFilters() {
    const allConsultations = Array.from(document.querySelectorAll('.consultation-card'));
    
    // Função global para filtrar por status
    window.filterConsultations = function(status) {
        // Atualizar aba ativa
        document.querySelectorAll('.filter-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        event.target.classList.add('active');
        
        // Mostrar/ocultar consultas baseado no status
        let visibleCount = 0;
        allConsultations.forEach(card => {
            if (status === 'all' || card.classList.contains(status)) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Verificar se há consultas visíveis
        checkEmptyState(visibleCount);
    };
    
    // Função global para buscar consultas
    window.searchConsultations = function() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        let visibleCount = 0;
        
        allConsultations.forEach(card => {
            const doctorName = card.querySelector('h5')?.textContent.toLowerCase() || '';
            const crm = card.querySelector('.text-secondary')?.textContent.toLowerCase() || '';
            
            if (doctorName.includes(searchTerm) || crm.includes(searchTerm)) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        checkEmptyState(visibleCount);
    };
    
    // Função global para filtrar por especialidade
    window.filterBySpecialty = function() {
        const specialty = document.getElementById('specialtyFilter').value;
        let visibleCount = 0;
        
        if (specialty === '') {
            allConsultations.forEach(card => {
                card.style.display = 'block';
                visibleCount++;
            });
        } else {
            allConsultations.forEach(card => {
                const cardSpecialty = card.querySelector('.text-secondary')?.textContent || '';
                if (cardSpecialty.includes(specialty)) {
                    card.style.display = 'block';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });
        }
        
        checkEmptyState(visibleCount);
    };
    
    // Função global para limpar filtros
    window.clearFilters = function() {
        document.getElementById('searchInput').value = '';
        document.getElementById('specialtyFilter').value = '';
        
        // Reset para aba 'all'
        document.querySelectorAll('.filter-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        const firstTab = document.querySelector('.filter-tab');
        if (firstTab) firstTab.classList.add('active');
        
        // Mostrar todas as consultas
        allConsultations.forEach(card => {
            card.style.display = 'block';
        });
        
        checkEmptyState(allConsultations.length);
    };
}

// Função para verificar estado vazio
function checkEmptyState(visibleCount) {
    const emptyState = document.getElementById('emptyState');
    if (emptyState) {
        if (visibleCount === 0) {
            emptyState.style.display = 'block';
        } else {
            emptyState.style.display = 'none';
        }
    }
}

// Função para alternar menu mobile
function toggleMobileMenu() {
    const navbarNav = document.getElementById('navbarNav');
    if (navbarNav) {
        navbarNav.classList.toggle('show');
    }
}