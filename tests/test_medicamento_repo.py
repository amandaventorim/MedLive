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
        medicamento_db = obter_medicamento_por_id(id_medicamento_inserido)
        assert medicamento_db is None, "O medicamento não foi excluído corretamente."

