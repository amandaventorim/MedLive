import sys
import os
from data.model.especialidade_model import Especialidade
from data.repo.especialidade_repo import *

class TestEspecialidadeRepo:
    def test_criar_tabela_especialidade(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_especialidade()
        # Assert
        assert resultado == True, "A criação da tabela 'especialidade' falhou."

    def test_obter_especialidades_por_pagina(self, test_db):
        # Arrange
        criar_tabela_especialidade()
        for i in range(10):
            especialidade_teste = Especialidade(0, f"Especialidade {i + 1}", "Descrição da especialidade")
            inserir_especialidade(especialidade_teste)
        # Act
        especialidades1 = obter_especialidades_por_pagina(1, 10)
        especialidades2 = obter_especialidades_por_pagina(2, 4)
        especialidades3 = obter_especialidades_por_pagina(3, 4)
        # Assert
        assert len(especialidades1) == 10, "Deve retornar 10 especialidades na primeira página."
        assert len(especialidades2) == 4, "Deve retornar 4 especialidades na segunda página."
        assert len(especialidades3) == 2, "Deve retornar 2 especialidades na terceira página."
        assert especialidades3[0].idEspecialidade == 9, "A primeira especialidade da terceira página deve ter ID 9."