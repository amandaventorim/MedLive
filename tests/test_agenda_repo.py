import sys
import os
from data.model.agenda_model import Agenda
from data.repo.agenda_repo import *

class TestAgendaRepo:
    def test_criar_tabela_agenda(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_agenda()
        # Assert
        assert resultado == True, "A criação da tabela 'agenda' falhou."

    def test_obter_agendas_por_pagina(self, test_db):
        # Arrange
        criar_tabela_agenda()
        for i in range(10):
            agenda_teste = Agenda(0, 0, f"Agenda {i + 1}", True)
            inserir_agenda(agenda_teste)
        # Act
        agendas1 = obter_agendas_por_pagina(1, 10)
        agendas2 = obter_agendas_por_pagina(2, 4)
        agendas3 = obter_agendas_por_pagina(3, 4)
        # Assert
        assert len(agendas1) == 10, "Deve retornar 10 agendas na primeira página."
        assert len(agendas2) == 4, "Deve retornar 4 agendas na segunda página."
        assert len(agendas3) == 2, "Deve retornar 2 agendas na terceira página."
        assert agendas3[0].idAgenda == 9, "A primeira agenda da terceira página deve ter ID 9."