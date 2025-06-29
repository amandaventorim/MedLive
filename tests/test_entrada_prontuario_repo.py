import sys
import os
from data.model.entrada_prontuario_model import EntradaProntuario
from data.repo import consulta_repo, entrada_prontuario_repo
from data.repo.entrada_prontuario_repo import *

class TestEntradaProntuarioRepo:
    def test_criar_tabela_entrada_prontuario(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_entrada_prontuario()
        # Assert
        assert resultado == True, "A criação da tabela 'entrada_prontuario' falhou."

    def test_obter_entradas_por_primeira_pagina(self, test_db, lista_entradas_prontuario_exemplo, lista_consultas_exemplo):
        # Arrange
        entrada_prontuario_repo.criar_tabela_entrada_prontuario()
        for entrada in lista_entradas_prontuario_exemplo():
            entrada_prontuario_repo.inserir_entrada_prontuario(entrada)
        consulta_repo.criar_tabela_consulta()
        for consulta in lista_consultas_exemplo():
            consulta_repo.inserir_consulta(consulta)
        # Act
        pagina_entradas = entrada_prontuario_repo.obter_entradas_prontuario_por_pagina(1, 4)
        # Assert
        assert len(pagina_entradas) == 4, "Deve retornar 4 entradas de prontuário na primeira página."
        ids_esperados = [1, 2, 3, 4]
        ids_recebidos = [entrada.idEntradaProntuario for entrada in pagina_entradas]
        assert ids_recebidos == ids_esperados, "Os IDs das entradas de prontuário na primeira página não correspondem aos esperados."
    
    def test_obter_entradas_por_terceira_pagina(self, test_db, lista_entradas_prontuario_exemplo, lista_consultas_exemplo):
        # Arrange
        entrada_prontuario_repo.criar_tabela_entrada_prontuario()
        for entrada in lista_entradas_prontuario_exemplo():
            entrada_prontuario_repo.inserir_entrada_prontuario(entrada)
        consulta_repo.criar_tabela_consulta()
        for consulta in lista_consultas_exemplo():
            consulta_repo.inserir_consulta(consulta)
        # Act
        pagina_entradas = entrada_prontuario_repo.obter_entradas_prontuario_por_pagina(3, 4)
        # Assert
        assert len(pagina_entradas) == 2, "Deve retornar 2 entradas de prontuário na terceira página."
        ids_esperados = [9, 10]
        ids_recebidos = [entrada.idEntradaProntuario for entrada in pagina_entradas]
        assert ids_recebidos == ids_esperados, "Os IDs das entradas de prontuário na terceira página não correspondem aos esperados."
    
    def test_obter_entradas_por_pagina_vazia(self, test_db):
        # Arrange
        entrada_prontuario_repo.criar_tabela_entrada_prontuario()
        consulta_repo.criar_tabela_consulta()
        
        # Act
        pagina_entradas = entrada_prontuario_repo.obter_entradas_prontuario_por_pagina(1, 10)
        # Assert
        assert isinstance(pagina_entradas, list), "A página de entradas de prontuário deve ser uma lista."
        assert len(pagina_entradas) == 0, "A página de entradas de prontuário não deve conter resultados quando a tabela está vazia."