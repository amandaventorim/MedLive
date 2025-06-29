import sys
import os
from data.model.medico_especialidade_model import MedicoEspecialidade
from data.repo.medico_especialidade_repo import *

class TestMedicoEspecialidadeRepo:
    def test_criar_tabela_medico_especialidade(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_medico_especialidade()
        # Assert
        assert resultado == True, "A criação da tabela 'medico_especialidade' falhou."

    def test_obter_medicos_especialidade_por_pagina(self, test_db):
        # Arrange
        criar_tabela_medico_especialidade()
        for i in range(10):
            medico_especialidade_teste = MedicoEspecialidade(0, 0, "2023-01-01")
            inserir_medico_especialidade(medico_especialidade_teste)
        # Act
        medicos_especialidades1 = obter_medicos_especialidades_por_pagina(1, 10)
        medicos_especialidades2 = obter_medicos_especialidades_por_pagina(2, 4)
        medicos_especialidades3 = obter_medicos_especialidades_por_pagina(3, 4)
        # Assert
        assert len(medicos_especialidades1) == 10, "Deve retornar 10 médicos especialidades na primeira página."
        assert len(medicos_especialidades2) == 4, "Deve retornar 4 médicos especialidades na segunda página."
        assert len(medicos_especialidades3) == 2, "Deve retornar 2 médicos especialidades na terceira página."
        assert medicos_especialidades3[0].idMedicoEspecialidade == 9, "O primeiro médico especialidade da terceira página deve ter ID 9."