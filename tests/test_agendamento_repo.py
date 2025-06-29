import sys
import os
from data.model.agendamento_model import Agendamento
from data.repo import agenda_repo, agendamento_repo, paciente_repo
from data.repo.agendamento_repo import *

class TestAgendamentoRepo:
    def test_criar_tabela_agendamento(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_agendamento()
        # Assert
        assert resultado == True, "A criação da tabela 'agendamento' falhou."

    def test_obter_agendamentos_por_primeira_pagina(self, test_db, lista_agendamentos_exemplo, lista_pacientes_exemplo, lista_agendas_exemplo):
        # Arrange
        agendamento_repo.criar_tabela_agendamento()
        for agendamento in lista_agendamentos_exemplo():
            agendamento_repo.inserir_agendamento(agendamento)
        paciente_repo.criar_tabela_paciente()
        for paciente in lista_pacientes_exemplo():
            paciente_repo.inserir_paciente(paciente)
        agenda_repo.criar_tabela_agenda()
        for agenda in lista_agendas_exemplo():
            agenda_repo.inserir_agenda(agenda)
        # Act
        pagina_agendamentos = agendamento_repo.obter_agendamentos_por_pagina(1, 4)
        # Assert
        assert len(pagina_agendamentos) == 4, "Deve retornar 4 agendamentos na primeira página."
        ids_esperados = [1, 2, 3, 4]
        ids_recebidos = [agendamento.idAgendamento for agendamento in pagina_agendamentos]
        assert ids_recebidos == ids_esperados, "Os IDs dos agendamentos na primeira página não correspondem aos esperados."
    
    def test_obter_agendamentos_por_terceira_pagina(self, test_db, lista_agendamentos_exemplo, lista_pacientes_exemplo, lista_agendas_exemplo):
        # Arrange
        agendamento_repo.criar_tabela_agendamento()
        for agendamento in lista_agendamentos_exemplo():
            agendamento_repo.inserir_agendamento(agendamento)
        paciente_repo.criar_tabela_paciente()
        for paciente in lista_pacientes_exemplo():
            paciente_repo.inserir_paciente(paciente)
        agenda_repo.criar_tabela_agenda()
        for agenda in lista_agendas_exemplo():
            agenda_repo.inserir_agenda(agenda)
        # Act
        pagina_agendamentos = agendamento_repo.obter_agendamentos_por_pagina(3, 4)
        # Assert
        assert len(pagina_agendamentos) == 2, "Deve retornar 2 agendamentos na terceira página."
        ids_esperados = [9, 10]
        ids_recebidos = [agendamento.idAgendamento for agendamento in pagina_agendamentos]
        assert ids_recebidos == ids_esperados, "Os IDs dos agendamentos na terceira página não correspondem aos esperados."
    
    def test_obter_agendamentos_por_pagina_vazia(self, test_db):
        # Arrange
        agendamento_repo.criar_tabela_agendamento()
        paciente_repo.criar_tabela_paciente()
        agenda_repo.criar_tabela_agenda()
        # Act
        pagina_agendamentos = agendamento_repo.obter_agendamentos_por_pagina(1, 10)
        # Assert
        assert isinstance(pagina_agendamentos, list), "A página de agendamentos deve ser uma lista."
        assert len(pagina_agendamentos) == 0, "A página de agendamentos não deve conter resultados quando a tabela está vazia."