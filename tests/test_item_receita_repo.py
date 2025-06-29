import sys
import os
from data.model.item_receita_model import ItemReceita
from data.repo import consulta_repo, item_receita_repo, medicamento_repo
from data.repo.item_receita_repo import *

class TestItemReceitaRepo:
    def test_criar_tabela_item_receita(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_item_receita()
        # Assert
        assert resultado == True, "A criação da tabela 'item_receita' falhou."

    def test_obter_item_receita_por_primeira_pagina(self, test_db, lista_itens_receita_exemplo, lista_consultas_exemplo, lista_medicamentos_exemplo):
        # Arrange
        item_receita_repo.criar_tabela_item_receita()
        for item in lista_itens_receita_exemplo():
            item_receita_repo.inserir_item_receita(item)
        consulta_repo.criar_tabela_consulta()
        for consulta in lista_consultas_exemplo():
            consulta_repo.inserir_consulta(consulta)
        medicamento_repo.criar_tabela_medicamento()
        for medicamento in lista_medicamentos_exemplo():
            medicamento_repo.inserir_medicamento(medicamento)

   
        # Act
        pagina_itens = item_receita_repo.obter_itens_receita_por_pagina(1, 4)
        # Assert
        assert len(pagina_itens) == 4, "Deve retornar 4 itens de receita na primeira página."
        ids_esperados = [1, 2, 3, 4]
        ids_recebidos = [item.idItemReceita for item in pagina_itens]
        assert ids_recebidos == ids_esperados, "Os IDs dos itens de receita na primeira página não correspondem aos esperados."

    def test_obter_item_receita_por_terceira_pagina(self, test_db, lista_itens_receita_exemplo, lista_consultas_exemplo, lista_medicamentos_exemplo):
        # Arrange
        item_receita_repo.criar_tabela_item_receita()
        for item in lista_itens_receita_exemplo():
            item_receita_repo.inserir_item_receita(item)
        consulta_repo.criar_tabela_consulta()
        for consulta in lista_consultas_exemplo():
            consulta_repo.inserir_consulta(consulta)
        medicamento_repo.criar_tabela_medicamento()
        for medicamento in lista_medicamentos_exemplo():
            medicamento_repo.inserir_medicamento(medicamento)

        # Act
        pagina_itens = item_receita_repo.obter_itens_receita_por_pagina(3, 4)
        # Assert
        assert len(pagina_itens) == 2, "Deve retornar 2 itens de receita na terceira página."
        ids_esperados = [9, 10]
        ids_recebidos = [item.idItemReceita for item in pagina_itens]
        assert ids_recebidos == ids_esperados, "Os IDs dos itens de receita na terceira página não correspondem aos esperados."
    
    def test_obter_item_receita_por_pagina_vazia(self, test_db):
        # Arrange
        item_receita_repo.criar_tabela_item_receita()
        consulta_repo.criar_tabela_consulta()
        medicamento_repo.criar_tabela_medicamento()
        # Act
        pagina_itens = item_receita_repo.obter_itens_receita_por_pagina(1, 10)
        # Assert
        assert isinstance(pagina_itens, list), "A página de itens de receita deve ser uma lista."
        assert len(pagina_itens) == 0, "A página de itens de receita não deve conter resultados quando a tabela está vazia."