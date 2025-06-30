import os
import sys
from data.repo.item_receita_repo import *
from data.model.item_receita_model import ItemReceita
from data.repo.consulta_repo import criar_tabela_consulta, inserir_consulta
from data.repo.medicamento_repo import criar_tabela_medicamento, inserir_medicamento
from data.repo.medico_repo import criar_tabela_medico, inserir_medico
from data.repo.paciente_repo import criar_tabela_paciente, inserir_paciente
from data.repo.usuario_repo import criar_tabela_usuario
from tests.conftest import item_receita_exemplo, consulta_exemplo, medicamento_exemplo, medico_exemplo, paciente_exemplo, lista_itens_receita_exemplo

class TestItemReceitaRepo:
    def test_criar_tabela_item_receita(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        criar_tabela_medicamento()
        # Act
        resultado = criar_tabela_item_receita()
        # Assert
        assert resultado == True, "A criação da tabela \'item_receita\' falhou."

    def test_inserir_item_receita(self, test_db, item_receita_exemplo, consulta_exemplo, medicamento_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        criar_tabela_medicamento()
        criar_tabela_item_receita()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        id_medicamento_inserido = inserir_medicamento(medicamento_exemplo)
        item_receita_exemplo.idConsulta = id_consulta_inserida
        item_receita_exemplo.idMedicamento = id_medicamento_inserido
        # Act
        resultado = inserir_item_receita(item_receita_exemplo)
        # Assert
        assert resultado == True, "A inserção do item de receita falhou."
        item_db = obter_item_receita_por_id(id_consulta_inserida, id_medicamento_inserido)
        assert item_db is not None, "O item de receita inserido não foi encontrado no banco de dados."
        assert item_db.idConsulta == id_consulta_inserida, "O ID da consulta do item de receita inserido está incorreto."
        assert item_db.idMedicamento == id_medicamento_inserido, "O ID do medicamento do item de receita inserido está incorreto."
        assert item_db.descricao == item_receita_exemplo.descricao, "A descrição do item de receita inserida está incorreta."

    def test_obter_todos_itens_receita(self, test_db, item_receita_exemplo, consulta_exemplo, medicamento_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        criar_tabela_medicamento()
        criar_tabela_item_receita()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        id_medicamento_inserido1 = inserir_medicamento(medicamento_exemplo)
        item_receita_exemplo.idConsulta = id_consulta_inserida
        item_receita_exemplo.idMedicamento = id_medicamento_inserido1
        inserir_item_receita(item_receita_exemplo)
        medicamento_exemplo.nome = "Medicamento 2"
        id_medicamento_inserido2 = inserir_medicamento(medicamento_exemplo)
        item_receita_exemplo.idMedicamento = id_medicamento_inserido2
        inserir_item_receita(item_receita_exemplo)
        # Act
        itens = obter_todos_itens_receita()
        # Assert
        assert len(itens) == 2, "O número de itens de receita obtidos não é igual a 2."
        assert itens[0].idConsulta == id_consulta_inserida, "O ID da consulta do primeiro item de receita não é o esperado."
        assert itens[0].idMedicamento == id_medicamento_inserido1, "O ID do medicamento do primeiro item de receita não é o esperado."
        assert itens[1].idConsulta == id_consulta_inserida, "O ID da consulta do segundo item de receita não é o esperado."
        assert itens[1].idMedicamento == id_medicamento_inserido2, "O ID do medicamento do segundo item de receita não é o esperado."

    def test_obter_itens_receita_por_pagina(self, test_db, lista_itens_receita_exemplo, consulta_exemplo, medico_exemplo, paciente_exemplo, medicamento_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        criar_tabela_medicamento()
        criar_tabela_item_receita()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        for i, item_receita in enumerate(lista_itens_receita_exemplo):
            medicamento_exemplo.nome = f"Medicamento {i}"
            id_medicamento_inserido = inserir_medicamento(medicamento_exemplo)
            item_receita.idConsulta = id_consulta_inserida
            item_receita.idMedicamento = id_medicamento_inserido
            inserir_item_receita(item_receita)
        numero_pagina = 2
        tamanho_pagina = 5
        # Act
        itens = obter_itens_receita_por_pagina(numero_pagina, tamanho_pagina)
        # Assert
        assert len(itens) == tamanho_pagina, "O número de itens de receita obtidos por página não corresponde ao tamanho da página."
        start_index = (numero_pagina - 1) * tamanho_pagina
        for i, item_receita in enumerate(itens):
            esperado = lista_itens_receita_exemplo[start_index + i]
            assert item_receita.idConsulta == esperado.idConsulta, f"O ID da consulta do item de receita {i} obtido não corresponde ao esperado."
            assert item_receita.idMedicamento == esperado.idMedicamento, f"O ID do medicamento do item de receita {i} obtido não corresponde ao esperado."
            assert item_receita.descricao == esperado.descricao, f"A descrição do item de receita {i} obtida não corresponde à esperada."

    def test_obter_item_receita_por_id(self, test_db, item_receita_exemplo, consulta_exemplo, medicamento_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        criar_tabela_medicamento()
        criar_tabela_item_receita()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        id_medicamento_inserido = inserir_medicamento(medicamento_exemplo)
        item_receita_exemplo.idConsulta = id_consulta_inserida
        item_receita_exemplo.idMedicamento = id_medicamento_inserido
        inserir_item_receita(item_receita_exemplo)
        # Act
        item_db = obter_item_receita_por_id(id_consulta_inserida, id_medicamento_inserido)
        # Assert
        assert item_db is not None, "O item de receita não foi encontrado no banco de dados."
        assert item_db.idConsulta == id_consulta_inserida, "O ID da consulta do item de receita obtido não é o esperado."
        assert item_db.idMedicamento == id_medicamento_inserido, "O ID do medicamento do item de receita obtido não é o esperado."

    def test_atualizar_item_receita(self, test_db, item_receita_exemplo, consulta_exemplo, medicamento_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        criar_tabela_medicamento()
        criar_tabela_item_receita()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        id_medicamento_inserido = inserir_medicamento(medicamento_exemplo)
        item_receita_exemplo.idConsulta = id_consulta_inserida
        item_receita_exemplo.idMedicamento = id_medicamento_inserido
        inserir_item_receita(item_receita_exemplo)
        item_inserido = obter_item_receita_por_id(id_consulta_inserida, id_medicamento_inserido)
        # Act
        item_inserido.descricao = "Nova descrição"
        resultado = atualizar_item_receita(item_inserido)
        # Assert
        assert resultado == True, "A atualização do item de receita falhou."
        item_db = obter_item_receita_por_id(id_consulta_inserida, id_medicamento_inserido)
        assert item_db.descricao == "Nova descrição", "A descrição do item de receita não foi alterada corretamente."

    def test_deletar_item_receita(self, test_db, item_receita_exemplo, consulta_exemplo, medicamento_exemplo, medico_exemplo, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        criar_tabela_medicamento()
        criar_tabela_item_receita()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_paciente_inserido = inserir_paciente(paciente_exemplo)
        consulta_exemplo.idMedico = id_medico_inserido
        consulta_exemplo.idPaciente = id_paciente_inserido
        id_consulta_inserida = inserir_consulta(consulta_exemplo)
        id_medicamento_inserido = inserir_medicamento(medicamento_exemplo)
        item_receita_exemplo.idConsulta = id_consulta_inserida
        item_receita_exemplo.idMedicamento = id_medicamento_inserido
        inserir_item_receita(item_receita_exemplo)
        # Act
        resultado = deletar_item_receita(id_consulta_inserida, id_medicamento_inserido)
        # Assert
        assert resultado == True, "A exclusão do item de receita falhou."
        item_db = obter_item_receita_por_id(id_consulta_inserida, id_medicamento_inserido)
        assert item_db == None, "O item de receita ainda existe no banco de dados após a exclusão."




    def test_inserir_item_receita_com_fk_inexistente(self, test_db, item_receita_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_paciente()
        criar_tabela_consulta()
        criar_tabela_medicamento()
        criar_tabela_item_receita()
        item_receita_exemplo.idConsulta = 9999 # ID de consulta inexistente
        item_receita_exemplo.idMedicamento = 9999 # ID de medicamento inexistente
        # Act & Assert
        try:
            inserir_item_receita(item_receita_exemplo)
            assert False, "A inserção de item de receita com FK inexistente deveria falhar."
        except Exception as e:
            assert "FOREIGN KEY constraint failed" in str(e), "Erro de FK esperado não ocorreu."


