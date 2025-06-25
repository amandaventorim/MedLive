import sys
import os
from data.repo.medicamento_repo import *

class TestMedicamentoRepo:
    def test_criar_tabela_medicamento(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_medicamento()
        # Assert
        assert resultado == True, "A criação da tabela 'medicamento' falhou."

    