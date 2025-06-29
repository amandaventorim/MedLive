import sys
import os
from data.model.medico_especialidade_model import MedicoEspecialidade
from data.repo import especialidade_repo, medico_especialidade_repo, medico_repo
from data.repo.medico_especialidade_repo import *

class TestMedicoEspecialidadeRepo:
    def test_criar_tabela_medico_especialidade(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_medico_especialidade()
        # Assert
        assert resultado == True, "A criação da tabela 'medico_especialidade' falhou."

    def test_obter_medicos_especialidade_por_primeira_pagina(self, test_db, lista_medico_especialidades_exemplo, lista_especialidades_exemplo, lista_medicos_exemplo):
        # Arrange
        medico_especialidade_repo.criar_tabela_medico_especialidade()
        for medico_especialidade in lista_medico_especialidades_exemplo():
            medico_especialidade_repo.inserir_medico_especialidade(medico_especialidade)
        especialidade_repo.criar_tabela_especialidade()
        for especialidade in lista_especialidades_exemplo():
            especialidade_repo.inserir_especialidade(especialidade)
        medico_repo.criar_tabela_medico()
        for medico in lista_medicos_exemplo():
            medico_repo.inserir_medico(medico)
        # Act
        pagina_medicos_especialidade = medico_especialidade_repo.obter_medicos_especialidades_por_pagina(1, 4)
        # Assert
        assert len(pagina_medicos_especialidade) == 4, "Deve retornar 4 médicos especialidades na primeira página."
        ids_esperados = [1, 2, 3, 4]
        ids_recebidos = [medico_especialidade.idMedicoEspecialidade for medico_especialidade in pagina_medicos_especialidade]
        assert ids_recebidos == ids_esperados, "Os IDs dos médicos especialidades na primeira página não correspondem aos esperados."

    def test_obter_medicos_especialidade_por_terceira_pagina(self, test_db, lista_medico_especialidades_exemplo, lista_especialidades_exemplo, lista_medicos_exemplo):
        # Arrange
        medico_especialidade_repo.criar_tabela_medico_especialidade()
        for medico_especialidade in lista_medico_especialidades_exemplo():
            medico_especialidade_repo.inserir_medico_especialidade(medico_especialidade)
        especialidade_repo.criar_tabela_especialidade()
        for especialidade in lista_especialidades_exemplo():
            especialidade_repo.inserir_especialidade(especialidade)
        medico_repo.criar_tabela_medico()
        for medico in lista_medicos_exemplo():
            medico_repo.inserir_medico(medico)
        # Act
        pagina_medicos_especialidade = medico_especialidade_repo.obter_medicos_especialidades_por_pagina(3, 4)
        # Assert
        assert len(pagina_medicos_especialidade) == 2, "Deve retornar 2 médicos especialidades na terceira página."
        ids_esperados = [9, 10]
        ids_recebidos = [medico_especialidade.idMedicoEspecialidade for medico_especialidade in pagina_medicos_especialidade]
        assert ids_recebidos == ids_esperados, "Os IDs dos médicos especialidades na terceira página não correspondem aos esperados."

    def test_obter_medicos_especialidade_por_pagina_vazia(self, test_db):
        # Arrange
        medico_especialidade_repo.criar_tabela_medico_especialidade()
        especialidade_repo.criar_tabela_especialidade()
        medico_repo.criar_tabela_medico()
        # Act
        pagina_medicos_especialidade = medico_especialidade_repo.obter_medicos_especialidades_por_pagina(1, 10)
        # Assert
        assert isinstance(pagina_medicos_especialidade, list), "A página de médicos especialidades deve ser uma lista."
        assert len(pagina_medicos_especialidade) == 0, "A página de médicos especialidades não deve conter resultados quando a tabela está vazia."