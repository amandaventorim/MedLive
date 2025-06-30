import os
import sys
from data.repo.consulta_repo import *
from data.model.consulta_model import Consulta
from data.repo.medico_repo import criar_tabela_medico, inserir_medico
from data.repo.paciente_repo import criar_tabela_paciente, inserir_paciente
from data.repo.usuario_repo import criar_tabela_usuario
from tests.conftest import consulta_exemplo, medico_exemplo, paciente_exemplo

class TestConsultaRepo:
    def test_criar_tabela_consulta(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        # Act
        resultado = criar_tabela_consulta()
        # Assert
        assert resultado == True, "A criação da tabela 'consulta' falhou."

    def test_inserir_consulta(self, test_db, consulta_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        # Act
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        # Assert
        consulta_db = obter_consulta_por_id(id_consulta_inserida)
        assert consulta_db is not None, "A consulta inserida não foi encontrada no banco de dados."
        assert consulta_db.idConsulta == 1, "O ID da consulta inserida deve ser igual a 1"
        assert consulta_db.idMedico == id_medico_inserido, "O ID do médico da consulta inserida está incorreto"
        assert consulta_db.idPaciente == id_paciente_inserido, "O ID do paciente da consulta inserida está incorreto"
        assert consulta_db.dataHora == consulta_exemplo.dataHora, "A data e hora da consulta inserida está incorreta"
        assert consulta_db.queixa == consulta_exemplo.queixa, "A queixa da consulta inserida está incorreta"
        assert consulta_db.conduta == consulta_exemplo.conduta, "A conduta da consulta inserida está incorreta"

    def test_obter_todas_consultas(self, test_db, consulta_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        inserir_consulta(consulta_exemplo)
        consulta_exemplo.dataHora = "2023-01-02"
        inserir_consulta(consulta_exemplo)
        # Act
        consultas = obter_todas_consultas()
        # Assert
        assert len(consultas) == 2, "O número de consultas obtidas não é igual a 2."
        assert consultas[0].idConsulta == 1, "O ID da primeira consulta não é o esperado."
        assert consultas[1].idConsulta == 2, "O ID do segundo consulta não é o esperado."

    def test_obter_consulta_por_id(self, test_db, consulta_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        # Act
        consulta_db = obter_consulta_por_id(id_consulta_inserida)
        # Assert
        assert consulta_db is not None, "A consulta não foi encontrada no banco de dados."
        assert consulta_db.idConsulta == id_consulta_inserida, "O ID da consulta obtida não é o esperado."

    def test_atualizar_consulta(self, test_db, consulta_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        consulta_inserida = obter_consulta_por_id(id_consulta_inserida)
        # Act
        consulta_inserida.dataHora = "2023-01-03"
        consulta_inserida.queixa = "Nova queixa"
        consulta_inserida.conduta = "Nova conduta"
        resultado = atualizar_consulta(consulta_inserida)
        # Assert
        assert resultado == True, "A atualização da consulta falhou."
        consulta_db = obter_consulta_por_id(id_consulta_inserida)
        assert consulta_db.dataHora == "2023-01-03", "A data e hora da consulta não foi alterada corretamente."
        assert consulta_db.queixa == "Nova queixa", "A queixa da consulta não foi alterada corretamente."
        assert consulta_db.conduta == "Nova conduta", "A conduta da consulta não foi alterada corretamente."

    def test_deletar_consulta(self, test_db, consulta_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        # Act
        resultado = deletar_consulta(id_consulta_inserida)
        # Assert
        assert resultado == True, "A exclusão da consulta falhou."
        consulta_db = obter_consulta_por_id(id_consulta_inserida)
        assert consulta_db == None, "A consulta ainda existe no banco de dados após a exclusão."


