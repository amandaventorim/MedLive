import os
import sys
from data.repo.entrada_prontuario_repo import *
from data.model.entrada_prontuario_model import EntradaProntuario
from data.repo.consulta_repo import criar_tabela_consulta, inserir_consulta
from data.repo.medico_repo import criar_tabela_medico, inserir_medico
from data.repo.paciente_repo import criar_tabela_paciente, inserir_paciente
from data.repo.usuario_repo import criar_tabela_usuario
from tests.conftest import entrada_prontuario_exemplo, consulta_exemplo, medico_exemplo, paciente_exemplo

class TestEntradaProntuarioRepo:
    def test_criar_tabela_entrada_prontuario(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        # Act
        resultado = criar_tabela_entrada_prontuario()
        # Assert
        assert resultado == True, "A criação da tabela 'entrada_prontuario' falhou."

    def test_inserir_entrada_prontuario(self, test_db, entrada_prontuario_exemplo, consulta_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        criar_tabela_entrada_prontuario()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        entrada_prontuario_exemplo.idConsulta = id_consulta_inserida
        # Act
        id_entrada_inserida = inserir_entrada_prontuario(entrada_prontuario_exemplo)
        # Assert
        entrada_db = obter_entrada_prontuario_por_id(id_entrada_inserida)
        assert entrada_db is not None, "A entrada de prontuário inserida não foi encontrada no banco de dados."
        assert entrada_db.idProntuario == 1, "O ID da entrada de prontuário inserida deve ser igual a 1"
        assert entrada_db.idConsulta == id_consulta_inserida, "O ID da consulta da entrada de prontuário inserida está incorreto"
        assert entrada_db.data == entrada_prontuario_exemplo.data, "A data da entrada de prontuário inserida está incorreta"
        assert entrada_db.queixaPrincipal == entrada_prontuario_exemplo.queixaPrincipal, "A queixa principal da entrada de prontuário inserida está incorreta"

    def test_obter_todas_entradas_prontuario(self, test_db, entrada_prontuario_exemplo, consulta_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        criar_tabela_entrada_prontuario()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        entrada_prontuario_exemplo.idConsulta = id_consulta_inserida
        inserir_entrada_prontuario(entrada_prontuario_exemplo)
        entrada_prontuario_exemplo.data = "2023-01-02"
        inserir_entrada_prontuario(entrada_prontuario_exemplo)
        # Act
        entradas = obter_todas_entradas_prontuario()
        # Assert
        assert len(entradas) == 2, "O número de entradas de prontuário obtidas não é igual a 2."
        assert entradas[0].idProntuario == 1, "O ID da primeira entrada de prontuário não é o esperado."
        assert entradas[1].idProntuario == 2, "O ID da segunda entrada de prontuário não é o esperado."

    def test_obter_entrada_prontuario_por_id(self, test_db, entrada_prontuario_exemplo, consulta_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        criar_tabela_entrada_prontuario()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        entrada_prontuario_exemplo.idConsulta = id_consulta_inserida
        id_entrada_inserida = inserir_entrada_prontuario(entrada_prontuario_exemplo)
        # Act
        entrada_db = obter_entrada_prontuario_por_id(id_entrada_inserida)
        # Assert
        assert entrada_db is not None, "A entrada de prontuário não foi encontrada no banco de dados."
        assert entrada_db.idProntuario == id_entrada_inserida, "O ID da entrada de prontuário obtida não é o esperado."

    def test_atualizar_entrada_prontuario(self, test_db, entrada_prontuario_exemplo, consulta_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        criar_tabela_entrada_prontuario()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        entrada_prontuario_exemplo.idConsulta = id_consulta_inserida
        id_entrada_inserida = inserir_entrada_prontuario(entrada_prontuario_exemplo)
        entrada_inserida = obter_entrada_prontuario_por_id(id_entrada_inserida)
        # Act
        entrada_inserida.data = "2023-01-03"
        entrada_inserida.queixaPrincipal = "Nova queixa principal"
        resultado = atualizar_entrada_prontuario(entrada_inserida)
        # Assert
        assert resultado == True, "A atualização da entrada de prontuário falhou."
        entrada_db = obter_entrada_prontuario_por_id(id_entrada_inserida)
        assert entrada_db.data == "2023-01-03", "A data da entrada de prontuário não foi alterada corretamente."
        assert entrada_db.queixaPrincipal == "Nova queixa principal", "A queixa principal da entrada de prontuário não foi alterada corretamente."

    def test_deletar_entrada_prontuario(self, test_db, entrada_prontuario_exemplo, consulta_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        criar_tabela_entrada_prontuario()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        entrada_prontuario_exemplo.idConsulta = id_consulta_inserida
        id_entrada_inserida = inserir_entrada_prontuario(entrada_prontuario_exemplo)
        # Act
        resultado = deletar_entrada_prontuario(id_entrada_inserida)
        # Assert
        assert resultado == True, "A exclusão da entrada de prontuário falhou."
        entrada_db = obter_entrada_prontuario_por_id(id_entrada_inserida)
        assert entrada_db == None, "A entrada de prontuário ainda existe no banco de dados após a exclusão."


