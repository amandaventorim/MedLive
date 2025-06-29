import sys
import os
from data.model.consulta_model import Consulta
from data.repo import consulta_repo, medico_repo, paciente_repo
from data.repo.consulta_repo import *

class TestConsultaRepo:
    def test_criar_tabela_consulta(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_consulta()
        # Assert
        assert resultado == True, "A criação da tabela 'consulta' falhou."

    def test_obter_consultas_por_primeira_pagina(self, test_db, lista_consultas_exemplo, lista_pacientes_exemplo, lista_medicos_exemplo):
        # Arrange
        consulta_repo.criar_tabela_consulta()
        for consulta in lista_consultas_exemplo():
            consulta_repo.inserir_consulta(consulta)
        paciente_repo.criar_tabela_paciente()
        for paciente in lista_pacientes_exemplo():
            paciente_repo.inserir_paciente(paciente)
        medico_repo.criar_tabela_medico()
        for medico in lista_medicos_exemplo():
            medico_repo.inserir_medico(medico)
        # Act
        pagina_consultas = consulta_repo.obter_consultas_por_pagina(1, 4)
        # Assert
        assert len(pagina_consultas) == 4, "Deve retornar 4 consultas na primeira página."
        ids_esperados = [1, 2, 3, 4]
        ids_recebidos = [consulta.idConsulta for consulta in pagina_consultas]
        assert ids_recebidos == ids_esperados, "Os IDs das consultas na primeira página não correspondem aos esperados."

    def test_obter_consultas_por_terceira_pagina(self, test_db, lista_consultas_exemplo, lista_pacientes_exemplo, lista_medicos_exemplo):
        # Arrange
        consulta_repo.criar_tabela_consulta()
        for consulta in lista_consultas_exemplo():
            consulta_repo.inserir_consulta(consulta)
        paciente_repo.criar_tabela_paciente()
        for paciente in lista_pacientes_exemplo():
            paciente_repo.inserir_paciente(paciente)
        medico_repo.criar_tabela_medico()
        for medico in lista_medicos_exemplo():
            medico_repo.inserir_medico(medico)
        # Act
        pagina_consultas = consulta_repo.obter_consultas_por_pagina(3, 4)
        # Assert
        assert len(pagina_consultas) == 2, "Deve retornar 2 consultas na terceira página."
        ids_esperados = [9, 10]
        ids_recebidos = [consulta.idConsulta for consulta in pagina_consultas]
        assert ids_recebidos == ids_esperados, "Os IDs das consultas na terceira página não correspondem aos esperados."
    
    def test_obter_consultas_por_pagina_vazia(self, test_db):
        # Arrange
        consulta_repo.criar_tabela_consulta()
        paciente_repo.criar_tabela_paciente()
        medico_repo.criar_tabela_medico()
        # Act
        pagina_consultas = consulta_repo.obter_consultas_por_pagina(1, 10)

        # Assert
        assert isinstance(pagina_consultas, list), "A página de consultas deve ser uma lista."
        assert len(pagina_consultas) == 0, "A página de consultas não deve conter resultados quando a tabela está vazia."