import sys
import os
from data.model.consulta_model import Consulta
from data.repo.consulta_repo import *

class TestConsultaRepo:
    def test_criar_tabela_consulta(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_consulta()
        # Assert
        assert resultado == True, "A criação da tabela 'consulta' falhou."

    def test_obter_consultas_por_pagina(self, test_db):
        # Arrange
        criar_tabela_consulta()
        for i in range(10):
            consulta_teste = Consulta(0, 0, 0, f"Consulta {i + 1}", "Motivo da consulta exemplo", "Observações da consulta exemplo")
            inserir_consulta(consulta_teste)
        # Act
        consultas1 = obter_consultas_por_pagina(1, 10)
        consultas2 = obter_consultas_por_pagina(2, 4)
        consultas3 = obter_consultas_por_pagina(3, 4)
        # Assert
        assert len(consultas1) == 10, "Deve retornar 10 consultas na primeira página."
        assert len(consultas2) == 4, "Deve retornar 4 consultas na segunda página."
        assert len(consultas3) == 2, "Deve retornar 2 consultas na terceira página."
        assert consultas3[0].idConsulta == 9, "A primeira consulta da terceira página deve ter ID 9."