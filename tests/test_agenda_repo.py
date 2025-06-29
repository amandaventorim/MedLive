import sys
import os
from data.model.agenda_model import Agenda
from data.repo import agenda_repo, medico_repo
from data.repo.agenda_repo import *

class TestAgendaRepo:
    def test_criar_tabela_agenda(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_agenda()
        # Assert
        assert resultado == True, "A criação da tabela 'agenda' falhou."

    def test_obter_agendas_por_primeira_pagina(self, test_db, lista_agendas_exemplo, lista_medicos_exemplo):
        # Arrange
        agenda_repo.criar_tabela_agenda()
        for agenda in lista_agendas_exemplo():
            agenda_repo.inserir_agenda(agenda)
        medico_repo.criar_tabela_medico()
        for medico in lista_medicos_exemplo():
            medico_repo.inserir_medico(medico)
        # Act
        pagina_agendas = agenda_repo.obter_agendas_por_pagina(1, 4)
        # Assert
        assert len(pagina_agendas) == 4, "Deve retornar 4 agendas na primeira página."
        ids_esperados = [1, 2, 3, 4]
        ids_recebidos = [agenda.idAgenda for agenda in pagina_agendas]
        assert ids_recebidos == ids_esperados, "Os IDs das agendas na primeira página não correspondem aos esperados."
    
    def test_obter_agendas_por_terceira_pagina(self, test_db, lista_agendas_exemplo, lista_medicos_exemplo):
        # Arrange
        agenda_repo.criar_tabela_agenda()
        for agenda in lista_agendas_exemplo():
            agenda_repo.inserir_agenda(agenda)
        medico_repo.criar_tabela_medico()
        for medico in lista_medicos_exemplo():
            medico_repo.inserir_medico(medico)
        # Act
        pagina_agendas = agenda_repo.obter_agendas_por_pagina(3, 4)
        # Assert
        assert len(pagina_agendas) == 2, "Deve retornar 2 agendas na terceira página."
        ids_esperados = [9, 10]
        ids_recebidos = [agenda.idAgenda for agenda in pagina_agendas]
        assert ids_recebidos == ids_esperados, "Os IDs das agendas na terceira página não correspondem aos esperados."

    def test_obter_agendas_por_pagina_vazia(self, test_db):
        # Arrange
        agenda_repo.criar_tabela_agenda()
        medico_repo.criar_tabela_medico()
        # Act
        pagina_agendas = agenda_repo.obter_agendas_por_pagina(1, 10)
        # Assert
        assert len(pagina_agendas) == 0, "Deve retornar uma lista vazia quando não houver agendas."