import sys
import os
from data.model.item_receita_model import ItemReceita
from data.repo.item_receita_repo import *

class TestItemReceitaRepo:
    def test_criar_tabela_item_receita(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_item_receita()
        # Assert
        assert resultado == True, "A criação da tabela 'item_receita' falhou."

    def test_obter_item_receita_por_pagina(self, test_db):
        # Arrange
        criar_tabela_item_receita()
        for i in range(10):
            item_receita_teste = ItemReceita(0, 0, f"Item Receita {i + 1}")
            inserir_item_receita(item_receita_teste)
        # Act
        itens1 = obter_itens_receita_por_pagina(1, 10)
        itens2 = obter_itens_receita_por_pagina(2, 4)
        itens3 = obter_itens_receita_por_pagina(3, 4)
        # Assert
        assert len(itens1) == 10, "Deve retornar 10 itens de receita na primeira página."
        assert len(itens2) == 4, "Deve retornar 4 itens de receita na segunda página."
        assert len(itens3) == 2, "Deve retornar 2 itens de receita na terceira página."
        assert itens3[0].idItemReceita == 9, "O primeiro item de receita da terceira página deve ter ID 9."