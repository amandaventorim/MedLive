import os
import sys
from data.repo.agendamento_repo import *
from data.model.agendamento_model import Agendamento
from data.repo.paciente_repo import criar_tabela_paciente, inserir_paciente
from data.repo.agenda_repo import criar_tabela_agenda, inserir_agenda
from data.repo.medico_repo import criar_tabela_medico, inserir_medico
from data.repo.usuario_repo import criar_tabela_usuario
from tests.conftest import agendamento_exemplo, paciente_exemplo, agenda_exemplo, medico_exemplo

class TestAgendamentoRepo:
    def test_criar_tabela_agendamento(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_agenda()
        # Act
        resultado = criar_tabela_agendamento()
        # Assert
        assert resultado == True, "A criação da tabela 'agendamento' falhou."

    def test_inserir_agendamento(self, test_db, agendamento_exemplo, paciente_exemplo, agenda_exemplo, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_agenda()
        criar_tabela_agendamento()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        agenda_exemplo.idMedico = id_medico_inserido
        id_agenda_inserida = inserir_agenda(agenda_exemplo)
        agendamento_exemplo.idPaciente = id_paciente_inserido
        agendamento_exemplo.idAgendamento = id_agenda_inserida
        # Act
        id_agendamento_inserido = inserir_agendamento(agendamento_exemplo)
        # Assert
        agendamento_db = obter_agendamento_por_id(id_agendamento_inserido)
        assert agendamento_db is not None, "O agendamento inserido não foi encontrado no banco de dados."
        assert agendamento_db.idAgendamento == id_agenda_inserida, "O ID do agendamento inserido deve ser igual ao ID da agenda."
        assert agendamento_db.idPaciente == id_paciente_inserido, "O ID do paciente do agendamento inserido está incorreto."
        assert agendamento_db.status == agendamento_exemplo.status, "O status do agendamento inserido está incorreto."
        assert agendamento_db.dataAgendamento == agendamento_exemplo.dataAgendamento, "A data de agendamento inserida está incorreta."

    def test_obter_todos_agendamentos(self, test_db, agendamento_exemplo, paciente_exemplo, agenda_exemplo, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_agenda()
        criar_tabela_agendamento()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        agenda_exemplo.idMedico = id_medico_inserido
        id_agenda_inserida1 = inserir_agenda(agenda_exemplo)
        agendamento_exemplo.idPaciente = id_paciente_inserido
        agendamento_exemplo.idAgendamento = id_agenda_inserida1
        inserir_agendamento(agendamento_exemplo)
        agenda_exemplo.dataHora = "2023-01-02"
        id_agenda_inserida2 = inserir_agenda(agenda_exemplo)
        agendamento_exemplo.idAgendamento = id_agenda_inserida2
        inserir_agendamento(agendamento_exemplo)
        # Act
        agendamentos = obter_todos_agendamentos()
        # Assert
        assert len(agendamentos) == 2, "O número de agendamentos obtidos não é igual a 2."
        assert agendamentos[0].idAgendamento == id_agenda_inserida1, "O ID do primeiro agendamento não é o esperado."
        assert agendamentos[1].idAgendamento == id_agenda_inserida2, "O ID do segundo agendamento não é o esperado."

    def test_obter_agendamentos_por_pagina(self, test_db, paciente_exemplo, agenda_exemplo, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_agenda()
        criar_tabela_agendamento()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        for i in range(1, 11):
            agenda_exemplo.idMedico = id_medico_inserido
            id_agenda_inserida = inserir_agenda(agenda_exemplo)
            agendamento = Agendamento(idAgendamento=id_agenda_inserida, idPaciente=id_paciente_inserido, status=f"status {i}", dataAgendamento=f"2023-01-{i:02d}")
            inserir_agendamento(agendamento)
        numero_pagina = 2
        tamanho_pagina = 5
        # Act
        agendamentos = obter_agendamentos_por_pagina(numero_pagina, tamanho_pagina)
        # Assert
        assert len(agendamentos) == tamanho_pagina, "O número de agendamentos obtidos por página não corresponde ao tamanho da página."
        start_index = (numero_pagina - 1) * tamanho_pagina
        for i, agendamento in enumerate(agendamentos):
            esperado_status = f"status {start_index + i + 1}"
            esperado_data = f"2023-01-{start_index + i + 1:02d}"
            assert agendamento.status == esperado_status, f"O status do agendamento {i} obtido não corresponde ao esperado."
            assert agendamento.dataAgendamento == esperado_data, f"A data do agendamento {i} obtido não corresponde à esperada."

    def test_obter_agendamento_por_id(self, test_db, agendamento_exemplo, paciente_exemplo, agenda_exemplo, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_agenda()
        criar_tabela_agendamento()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        agenda_exemplo.idMedico = id_medico_inserido
        id_agenda_inserida = inserir_agenda(agenda_exemplo)
        agendamento_exemplo.idPaciente = id_paciente_inserido
        agendamento_exemplo.idAgendamento = id_agenda_inserida
        id_agendamento_inserido = inserir_agendamento(agendamento_exemplo)
        # Act
        agendamento_db = obter_agendamento_por_id(id_agendamento_inserido)
        # Assert
        assert agendamento_db is not None, "O agendamento não foi encontrado no banco de dados."
        assert agendamento_db.idAgendamento == id_agendamento_inserido, "O ID do agendamento obtido não é o esperado."

    def test_atualizar_agendamento(self, test_db, agendamento_exemplo, paciente_exemplo, agenda_exemplo, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_agenda()
        criar_tabela_agendamento()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        agenda_exemplo.idMedico = id_medico_inserido
        id_agenda_inserida = inserir_agenda(agenda_exemplo)
        agendamento_exemplo.idPaciente = id_paciente_inserido
        agendamento_exemplo.idAgendamento = id_agenda_inserida
        id_agendamento_inserido = inserir_agendamento(agendamento_exemplo)
        agendamento_inserido = obter_agendamento_por_id(id_agendamento_inserido)
        # Act
        agendamento_inserido.status = "Concluído"
        agendamento_inserido.dataAgendamento = "2023-01-03"
        resultado = atualizar_agendamento(agendamento_inserido)
        # Assert
        assert resultado == True, "A atualização do agendamento falhou."
        agendamento_db = obter_agendamento_por_id(id_agendamento_inserido)
        assert agendamento_db.status == "Concluído", "O status do agendamento não foi alterado corretamente."
        assert agendamento_db.dataAgendamento == "2023-01-03", "A data de agendamento não foi alterada corretamente."

    def test_deletar_agendamento(self, test_db, agendamento_exemplo, paciente_exemplo, agenda_exemplo, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_agenda()
        criar_tabela_agendamento()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        agenda_exemplo.idMedico = id_medico_inserido
        id_agenda_inserida = inserir_agenda(agenda_exemplo)
        agendamento_exemplo.idPaciente = id_paciente_inserido
        agendamento_exemplo.idAgendamento = id_agenda_inserida
        id_agendamento_inserido = inserir_agendamento(agendamento_exemplo)
        # Act
        resultado = deletar_agendamento(id_agendamento_inserido)
        # Assert
        assert resultado == True, "A exclusão do agendamento falhou."
        agendamento_db = obter_agendamento_por_id(id_agendamento_inserido)
        assert agendamento_db == None, "O agendamento ainda existe no banco de dados após a exclusão."




    def test_inserir_agendamento_com_fk_inexistente(self, test_db, agendamento_exemplo, medico_exemplo, paciente_exemplo, agenda_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_agenda()
        criar_tabela_agendamento()

        id_medico_inserido = inserir_medico(medico_exemplo)
        inserir_paciente(paciente_exemplo)
        agenda_exemplo.idMedico = id_medico_inserido
        id_agenda_inserida = inserir_agenda(agenda_exemplo)
        agendamento_exemplo.idPaciente = 9999 #não existe
        agendamento_exemplo.idAgendamento = id_agenda_inserida
        # Act & Assert
        try:
            inserir_agendamento(agendamento_exemplo)
            assert False, "A inserção de agendamento com FK inexistente deveria falhar."
        except Exception as e:
            assert "FOREIGN KEY constraint failed" in str(e), "Erro de FK esperado não ocorreu."


