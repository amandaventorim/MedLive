import sys
import os
from data.model.especialidade_model import Especialidade
from data.repo import especialidade_repo
from data.repo.especialidade_repo import *

class TestEspecialidadeRepo:
    def test_criar_tabela_especialidade(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_especialidade()
        # Assert
        assert resultado == True, "A criação da tabela 'especialidade' falhou."

    def test_obter_especialidades_por_primeira_pagina(self, test_db, lista_especialidades_exemplo):
        # Arrange
        especialidade_repo.criar_tabela_especialidade()
        for especialidade in lista_especialidades_exemplo():
            especialidade_repo.inserir_especialidade(especialidade)
        # Act
        pagina_especialidades = especialidade_repo.obter_especialidades_por_pagina(1, 4)
        # Assert
        assert len(pagina_especialidades) == 4, "Deve retornar 4 especialidades na primeira página."
        ids_esperados = [1, 2, 3, 4]
        ids_recebidos = [especialidade.idEspecialidade for especialidade in pagina_especialidades]
        assert ids_recebidos == ids_esperados, "Os IDs das especialidades na primeira página não correspondem aos esperados."

    def test_obter_especialidades_por_terceira_pagina(self, test_db, lista_especialidades_exemplo):
        # Arrange
        especialidade_repo.criar_tabela_especialidade()
        for especialidade in lista_especialidades_exemplo():
            especialidade_repo.inserir_especialidade(especialidade)
        # Act
        pagina_especialidades = especialidade_repo.obter_especialidades_por_pagina(3, 4)
        # Assert
        assert len(pagina_especialidades) == 2, "Deve retornar 2 especialidades na terceira página."
        ids_esperados = [9, 10]
        ids_recebidos = [especialidade.idEspecialidade for especialidade in pagina_especialidades]
        assert ids_recebidos == ids_esperados, "Os IDs das especialidades na terceira página não correspondem aos esperados."

    def test_obter_especialidades_por_pagina_vazia(self, test_db):
        # Arrange
        especialidade_repo.criar_tabela_especialidade()
        # Act
        pagina_especialidades = especialidade_repo.obter_especialidades_por_pagina(1, 10)
        # Assert
        assert isinstance(pagina_especialidades, list), "A página de especialidades deve ser uma lista."
        assert len(pagina_especialidades) == 0, "A página de especialidades não deve conter resultados quando a tabela está vazia."