import sys
import os
from data.repo import medicamento_repo
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

    def test_obter_medicamento_por_primeira_pagina(self, test_db, lista_medicamentos_exemplo):
        # Arrange
        medicamento_repo.criar_tabela_medicamento()
        for medicamento in lista_medicamentos_exemplo:
            medicamento_repo.inserir_medicamento(medicamento)
        # Act
        pagina_medicamentos = medicamento_repo.obter_medicamentos_por_pagina(1, 4)
        # Assert
        assert len(pagina_medicamentos) == 4, "A primeira consulta deve retornar 4 medicamentos."
        ids_esperados = [1, 2, 3, 4]
        ids_retornados = [med.idMedicamento for med in pagina_medicamentos]
        assert ids_retornados == ids_esperados, "Os IDs dos medicamentos retornados não correspondem aos esperados."

    def test_obter_medicamento_por_terceira_pagina(self, test_db, lista_medicamentos_exemplo):
        # Arrange
        medicamento_repo.criar_tabela_medicamento()
        for medicamento in lista_medicamentos_exemplo:
            medicamento_repo.inserir_medicamento(medicamento)
        # Act
        pagina_medicamentos = medicamento_repo.obter_medicamentos_por_pagina(3, 4)
        # Assert
        assert len(pagina_medicamentos) == 2, "A terceira consulta deve retornar 2 medicamentos."
        ids_esperados = [9, 10]
        ids_retornados = [med.idMedicamento for med in pagina_medicamentos]
        assert ids_retornados == ids_esperados, "Os IDs dos medicamentos retornados não correspondem aos esperados."

    def test_obter_medicamento_por_pagina_com_pagina_vazia(self, test_db):
        # Arrange
        medicamento_repo.criar_tabela_medicamento()
        # Act
        pagina_medicamentos = medicamento_repo.obter_medicamentos_por_pagina(1, 10)
        # Assert
        assert isinstance(pagina_medicamentos, list), "A consulta deve retornar uma lista."
        assert len(pagina_medicamentos) == 0, "A consulta deve retornar uma lista vazia quando não há medicamentos."
        
    


