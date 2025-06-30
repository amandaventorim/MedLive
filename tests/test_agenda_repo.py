import os
import sys
from data.repo.agenda_repo import *
from data.model.agenda_model import Agenda
from data.repo.medico_repo import criar_tabela_medico, inserir_medico
from data.repo.usuario_repo import criar_tabela_usuario
from tests.conftest import agenda_exemplo, medico_exemplo

class TestAgendaRepo:
    def test_criar_tabela_agenda(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        # Act
        resultado = criar_tabela_agenda()
        # Assert
        assert resultado == True, "A criação da tabela 'agenda' falhou."

    def test_inserir_agenda(self, test_db, agenda_exemplo, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_agenda()
        id_medico_inserido = inserir_medico(medico_exemplo)
        agenda_exemplo.idMedico = id_medico_inserido
        # Act
        id_agenda_inserida = inserir_agenda(agenda_exemplo)
        # Assert
        agenda_db = obter_agenda_por_id(id_agenda_inserida)
        assert agenda_db is not None, "A agenda inserida não foi encontrada no banco de dados."
        assert agenda_db.idAgenda == 1, "O ID da agenda inserida deve ser igual a 1"
        assert agenda_db.idMedico == id_medico_inserido, "O ID do médico da agenda inserida está incorreto"
        assert agenda_db.dataHora == agenda_exemplo.dataHora, "A data e hora da agenda inserida está incorreta"
        assert agenda_db.disponivel == agenda_exemplo.disponivel, "O status de disponibilidade da agenda inserida está incorreto"

    def test_obter_todas_agendas(self, test_db, agenda_exemplo, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_agenda()
        id_medico_inserido = inserir_medico(medico_exemplo)
        agenda_exemplo.idMedico = id_medico_inserido
        inserir_agenda(agenda_exemplo)
        agenda_exemplo.dataHora = "2023-01-02"
        inserir_agenda(agenda_exemplo)
        # Act
        agendas = obter_todas_agendas()
        # Assert
        assert len(agendas) == 2, "O número de agendas obtidas não é igual a 2."
        assert agendas[0].idAgenda == 1, "O ID da primeira agenda não é o esperado."
        assert agendas[1].idAgenda == 2, "O ID da segunda agenda não é o esperado."

    def test_obter_agendas_por_pagina(self, test_db, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_agenda()
        id_medico_inserido = inserir_medico(medico_exemplo)
        for i in range(1, 11):
            agenda = Agenda(0, id_medico_inserido, f"2023-01-{i:02d}", True)
            inserir_agenda(agenda)
        numero_pagina = 2
        tamanho_pagina = 5
        # Act
        agendas = obter_agendas_por_pagina(numero_pagina, tamanho_pagina)
        # Assert
        assert len(agendas) == tamanho_pagina, "O número de agendas obtidas por página não corresponde ao tamanho da página."
        start_index = (numero_pagina - 1) * tamanho_pagina
        for i, agenda in enumerate(agendas):
            esperado_data = f"2023-01-{start_index + i + 1:02d}"
            assert agenda.dataHora == esperado_data, f"A data da agenda {i} obtida não corresponde à esperada."

    def test_obter_agenda_por_id(self, test_db, agenda_exemplo, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_agenda()
        id_medico_inserido = inserir_medico(medico_exemplo)
        agenda_exemplo.idMedico = id_medico_inserido
        id_agenda_inserida = inserir_agenda(agenda_exemplo)
        # Act
        agenda_db = obter_agenda_por_id(id_agenda_inserida)
        # Assert
        assert agenda_db is not None, "A agenda não foi encontrada no banco de dados."
        assert agenda_db.idAgenda == id_agenda_inserida, "O ID da agenda obtida não é o esperado."

    def test_atualizar_agenda(self, test_db, agenda_exemplo, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_agenda()
        id_medico_inserido = inserir_medico(medico_exemplo)
        agenda_exemplo.idMedico = id_medico_inserido
        id_agenda_inserida = inserir_agenda(agenda_exemplo)
        agenda_inserida = obter_agenda_por_id(id_agenda_inserida)
        # Act
        agenda_inserida.dataHora = "2023-01-03"
        agenda_inserida.disponivel = False
        resultado = atualizar_agenda(agenda_inserida)
        # Assert
        assert resultado == True, "A atualização da agenda falhou."
        agenda_db = obter_agenda_por_id(id_agenda_inserida)
        assert agenda_db.dataHora == "2023-01-03", "A data e hora da agenda não foi alterada corretamente."
        assert agenda_db.disponivel == False, "O status de disponibilidade da agenda não foi alterado corretamente."

    def test_deletar_agenda(self, test_db, agenda_exemplo, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_agenda()
        id_medico_inserido = inserir_medico(medico_exemplo)
        agenda_exemplo.idMedico = id_medico_inserido
        id_agenda_inserida = inserir_agenda(agenda_exemplo)
        # Act
        resultado = deletar_agenda(id_agenda_inserida)
        # Assert
        assert resultado == True, "A exclusão da agenda falhou."
        agenda_db = obter_agenda_por_id(id_agenda_inserida)
        assert agenda_db == None, "A agenda ainda existe no banco de dados após a exclusão."



    def test_inserir_agenda_com_fk_inexistente(self, test_db, agenda_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_agenda()
        agenda_exemplo.idMedico = 9999 # ID de médico inexistente
        # Act & Assert
        try:
            inserir_agenda(agenda_exemplo)
            assert False, "A inserção de agenda com FK inexistente deveria falhar."
        except Exception as e:
            assert "FOREIGN KEY constraint failed" in str(e), "Erro de FK esperado não ocorreu."


