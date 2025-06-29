import sys
import os
from data.model.agendamento_model import Agendamento
from data.repo.agendamento_repo import *

class TestAgendamentoRepo:
    def test_criar_tabela_agendamento(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_agendamento()
        # Assert
        assert resultado == True, "A criação da tabela 'agendamento' falhou."

    def test_obter_agendamentos_por_pagina(self, test_db):
        # Arrange
        criar_tabela_agendamento()
        for i in range(10):
            agendamento_teste = Agendamento(0, 0, f"Agendamento {i + 1}", "2023-01-01")
            inserir_agendamento(agendamento_teste)
        # Act
        agendamentos1 = obter_agendamentos_por_pagina(1, 10)
        agendamentos2 = obter_agendamentos_por_pagina(2, 4)
        agendamentos3 = obter_agendamentos_por_pagina(3, 4)
        # Assert
        assert len(agendamentos1) == 10, "Deve retornar 10 agendamentos na primeira página."
        assert len(agendamentos2) == 4, "Deve retornar 4 agendamentos na segunda página."
        assert len(agendamentos3) == 2, "Deve retornar 2 agendamentos na terceira página."
        assert agendamentos3[0].idAgendamento == 9, "O primeiro agendamento da terceira página deve ter ID 9."