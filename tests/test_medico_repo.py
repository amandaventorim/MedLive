import sys
import os
from data.model.medico_model import Medico
from data.repo import medico_repo, usuario_repo
from data.repo.medico_repo import *

class TestMedicoRepo:
    def test_criar_tabela_medico(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_medico()
        # Assert
        assert resultado == True, "A criação da tabela 'medico' falhou."

    def test_obter_medicos_por_primeira_pagina(self, test_db, lista_medicos_exemplo, lista_usuarios_exemplo):
        # Arrange
        medico_repo.criar_tabela_medico()
        for medico in lista_medicos_exemplo():
            medico_repo.inserir_medico(medico)
        usuario_repo.criar_tabela_usuario()
        for usuario in lista_usuarios_exemplo():
            usuario_repo.inserir_usuario(usuario)
        # Act
        pagina_medicos = medico_repo.obter_medicos_por_pagina(1, 4)
        # Assert
        assert len(pagina_medicos) == 4, "Deve retornar 4 médicos na primeira página."
        nomes_esperados = ["Medico 01", "Medico 02", "Medico 03", "Medico 04"]
        nomes_recebidos = [medico.nome for medico in pagina_medicos]
        assert nomes_recebidos == nomes_esperados, "Os nomes dos médicos na primeira página não correspondem aos esperados."
    
    def test_obter_medicos_por_terceira_pagina(self, test_db, lista_medicos_exemplo, lista_usuarios_exemplo):
        # Arrange
        medico_repo.criar_tabela_medico()
        for medico in lista_medicos_exemplo():
            medico_repo.inserir_medico(medico)
        usuario_repo.criar_tabela_usuario()
        for usuario in lista_usuarios_exemplo():
            usuario_repo.inserir_usuario(usuario)
        # Act
        pagina_medicos = medico_repo.obter_medicos_por_pagina(3, 4)
        # Assert
        assert len(pagina_medicos) == 2, "Deve retornar 2 médicos na terceira página."
        nomes_esperados = ["Medico 09", "Medico 10"]
        nomes_recebidos = [medico.nome for medico in pagina_medicos]
        assert nomes_recebidos == nomes_esperados, "Os nomes dos médicos na terceira página não correspondem aos esperados."

    def test_obter_medicos_por_pagina_vazia(self, test_db):
        # Arrange
        medico_repo.criar_tabela_medico()
        usuario_repo.criar_tabela_usuario()
        # Act
        pagina_medicos = medico_repo.obter_medicos_por_pagina(1, 10)
        # Assert
        assert isinstance(pagina_medicos, list), "A página de médicos deve ser uma lista."
        assert len(pagina_medicos) == 0, "A página de médicos não deve conter resultados quando a tabela está vazia."