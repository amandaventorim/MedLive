import sys
import os
from data.model.medico_model import Medico
from data.repo.medico_repo import *

class TestMedicoRepo:
    def test_criar_tabela_medico(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_medico()
        # Assert
        assert resultado == True, "A criação da tabela 'medico' falhou."

    def test_obter_medicos_por_pagina(self, test_db):
        # Arrange
        criar_tabela_medico()
        for i in range(10):
            medico_teste = Medico(0, f"CRM-{i + 1:03d}", "Ativo")
            inserir_usuario_medico(medico_teste)
        # Act
        medicos1 = obter_medicos_por_pagina(1, 10)
        medicos2 = obter_medicos_por_pagina(2, 4)
        medicos3 = obter_medicos_por_pagina(3, 4)
        # Assert
        assert len(medicos1) == 10, "Deve retornar 10 médicos na primeira página."
        assert len(medicos2) == 4, "Deve retornar 4 médicos na segunda página."
        assert len(medicos3) == 2, "Deve retornar 2 médicos na terceira página."
        assert medicos3[0].idMedico == 9, "O primeiro médico da terceira página deve ter ID 9."