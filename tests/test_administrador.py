import sys
import os
from data.model.administrador_model import Administrador
from data.repo import administrador_repo, usuario_repo
from data.repo.administrador_repo import *

class TestAdministradorRepo:
    def test_criar_tabela_administrador(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_administrador()
        # Assert
        assert resultado == True, "A criação da tabela 'administrador' falhou."

    def test_obter_administradores_por_primeira_pagina(self, test_db, lista_administradores_exemplo, lista_usuarios_exemplo):
        # Arrange
        administrador_repo.criar_tabela_administrador()
        for administrador in lista_administradores_exemplo():
            administrador_repo.inserir_administrador(administrador)
        usuario_repo.criar_tabela_usuario()
        for usuario in lista_usuarios_exemplo():
            usuario_repo.inserir_usuario(usuario)
        
        # Act
        pagina_administradores = administrador_repo.obter_administradores_por_pagina(1, 4)
        
        # Assert
        assert len(pagina_administradores) == 4, "Deve retornar 4 administradores na primeira página."
        nomes_esperados = ["Administrador 01", "Administrador 02", "Administrador 03", "Administrador 04"]
        nomes_recebidos = [admin.nome for admin in pagina_administradores]
        assert nomes_recebidos == nomes_esperados, "Os nomes dos administradores na primeira página não correspondem aos esperados."

    def test_obter_administradores_por_terceira_pagina(self, test_db, lista_administradores_exemplo, lista_usuarios_exemplo):
        # Arrange
        administrador_repo.criar_tabela_administrador()
        for administrador in lista_administradores_exemplo():
            administrador_repo.inserir_administrador(administrador)
        usuario_repo.criar_tabela_usuario()
        for usuario in lista_usuarios_exemplo():
            usuario_repo.inserir_usuario(usuario)
        
        # Act
        pagina_administradores = administrador_repo.obter_administradores_por_pagina(3, 4)
        
        # Assert
        assert len(pagina_administradores) == 2, "Deve retornar 2 administradores na terceira página."
        nomes_esperados = ["Administrador 09", "Administrador 10"]
        nomes_recebidos = [admin.nome for admin in pagina_administradores]
        assert nomes_recebidos == nomes_esperados, "Os nomes dos administradores na terceira página não correspondem aos esperados."
    
    def test_obter_administradores_por_pagina_vazia(self, test_db):
        # Arrange
        administrador_repo.criar_tabela_administrador()
        usuario_repo.criar_tabela_usuario()
        
        # Act
        pagina_administradores = administrador_repo.obter_administradores_por_pagina(1, 10)
        
        # Assert
        assert isinstance(pagina_administradores, list), "A página de administradores deve ser uma lista."
        assert len(pagina_administradores) == 0, "A página de administradores não deve conter resultados quando a tabela está vazia."