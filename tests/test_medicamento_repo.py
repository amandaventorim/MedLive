import sys
import os
from data.repo.medicamento_repo import *
from data.model.medicamento_model import Medicamento

class TestMedicamentoRepo:
    def test_criar_tabela_medicamento(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_medicamento()
        # Assert
        assert resultado == True, "A criação da tabela 'medicamento' falhou."

    
    def test_inserir_medicamento(self, test_db):
        # Arrange
        criar_tabela_medicamento()
        medicamento_teste = Medicamento(0, "Medicamento Teste")
        # Act
        id_medicamento_inserido = inserir_medicamento(medicamento_teste)
        # Assert
        medicamento_db = obter_medicamento_por_id(id_medicamento_inserido)
        assert medicamento_db is not None, "O medicamento inserido não foi encontrado no banco de dados."
        assert medicamento_db.idMedicamento == 1, "O ID do medicamento inserido deve ser igual a 1"
        assert medicamento_db.nome == "Medicamento Teste", "O nome do medicamento inserido deve ser igual ao nome inserido"


    def test_atualizar_medicamento(self, test_db):
        # Arrange
        criar_tabela_medicamento()
        medicamento_teste = Medicamento(0, "Medicamento Teste")
        id_medicamento_inserido = inserir_medicamento(medicamento_teste)
        medicamento_inserido = obter_medicamento_por_id(id_medicamento_inserido)
        # Act
        medicamento_inserido.nome = "Medicamento Atualizado"
        resultado = atualizar_medicamento(medicamento_inserido)
        # Assert
        assert resultado == True, "A alteração do medicamento falhou."
        medicamento_db = obter_medicamento_por_id(id_medicamento_inserido)
        assert medicamento_db.nome == "Medicamento Atualizado", "O nome do medicamento não foi alterado corretamente."


    def test_deletar_medicamento(self, test_db):
        # Arrange
        criar_tabela_medicamento()
        medicamento_teste = Medicamento(0, "Medicamento Teste")
        id_medicamento_inserido = inserir_medicamento(medicamento_teste)
        # Act
        resultado = deletar_medicamento(id_medicamento_inserido)
        # Assert
        assert resultado == True, "A exclusão do medicamento falhou."
        medicamento_deletado = obter_medicamento_por_id(id_medicamento_inserido)
        assert medicamento_deletado == None, "O medicamento não foi excluído corretamente."

    def test_obter_medicamento_por_id(self, test_db):
        # Arrange
        criar_tabela_medicamento()
        medicamento_teste = Medicamento(0, "Medicamento Teste")
        id_medicamento_inserido = inserir_medicamento(medicamento_teste)
        # Act
        medicamento_db = obter_medicamento_por_id(id_medicamento_inserido)
        # Assert
        assert medicamento_db is not None, "O medicamento não foi encontrado no banco de dados."
        assert medicamento_db.idMedicamento == id_medicamento_inserido, "O ID do medicamento obtido não corresponde ao ID inserido."
        assert medicamento_db.nome == "Medicamento Teste", "O nome do medicamento obtido não corresponde ao nome inserido."

    def test_obter_todos_medicamentos(self, test_db):
        # Arrange
        criar_tabela_medicamento()
        for i in range(2):
            medicamento_teste = Medicamento(0, f"Medicamento Teste {i + 1}")
            inserir_medicamento(medicamento_teste)
        # Act
        medicamentos_db = obter_todos_medicamentos()
        # Assert
        assert len(medicamentos_db) >= 2, "A quantidade de medicamentos obtidos não é maior ou igual a 2."

    def test_obter_medicamento_por_pagina(self, test_db):
        # Arrange
        criar_tabela_medicamento()
        for i in range(10):
            medicamento_teste = Medicamento(0, f"Medicamento Teste {i + 1}")
            inserir_medicamento(medicamento_teste)
        # Act
        medicamentos_db = obter_medicamento_por_pagina(1, 2)
        # Assert
        assert len(medicamentos_db) == 2, "A quantidade de medicamentos obtidos na página não é igual a 2."
        assert medicamentos_db[0].nome == "Medicamento Teste 1", "O primeiro medicamento da página não é o esperado."
        assert medicamentos_db[1].nome == "Medicamento Teste 2", "O segundo medicamento da página não é o esperado."

    


