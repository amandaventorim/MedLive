import sys
import os
from data.model.medico_model import Medico
from data.repo import medico_repo
from data.repo.medico_repo import *

class TestMedicoRepo:
    def test_criar_tabela_medico(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_medico()
        # Assert
        assert resultado == True, "A criação da tabela 'medico' falhou."

    def test_obter_medicos_por_primeira_pagina(self, test_db, lista_medicos_exemplo):
        # Arrange
        medico_repo.criar_tabela_medico()