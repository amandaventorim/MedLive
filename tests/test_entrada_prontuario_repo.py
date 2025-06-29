import sys
import os
from data.model.entrada_prontuario_model import EntradaProntuario
from data.repo.entrada_prontuario_repo import *

class TestEntradaProntuarioRepo:
    def test_criar_tabela_entrada_prontuario(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_entrada_prontuario()
        # Assert
        assert resultado == True, "A criação da tabela 'entrada_prontuario' falhou."

    def test_obter_entradas_por_pagina(self, test_db):
        # Arrange
        criar_tabela_entrada_prontuario()
        for i in range(10):
            entrada_teste = EntradaProntuario(0, 0, "2023-10-01", f"Queixa principal{i+1}", "Alergias", "Solicitações de exames", "Antecedentes familiares", "Fatores de alívio", "Fatores que pioram", "Fatores predecessores")
            inserir_entrada_prontuario(entrada_teste)
        # Act
        entradas1 = obter_entradas_prontuario_por_pagina(1, 10)
        entradas2 = obter_entradas_prontuario_por_pagina(2, 4)
        entradas3 = obter_entradas_prontuario_por_pagina(3, 4)
        # Assert
        assert len(entradas1) == 10, "Deve retornar 10 entradas na primeira página."
        assert len(entradas2) == 4, "Deve retornar 4 entradas na segunda página."
        assert len(entradas3) == 2, "Deve retornar 2 entradas na terceira página."
        assert entradas3[0].idEntradaProntuario == 9, "A primeira entrada da terceira página deve ter ID 9."